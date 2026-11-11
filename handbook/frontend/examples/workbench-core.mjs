// 教学核心：data-only SSE 子集 + 连续序号投影。无网络、DOM 或业务执行能力。
export function decodeEvent(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('INVALID_EVENT');
  }
  if (value.schema_version !== 1) throw new Error('UNSUPPORTED_VERSION');
  if (typeof value.run_id !== 'string' || value.run_id.length === 0 ||
      !Number.isSafeInteger(value.seq) || value.seq < 1) {
    throw new Error('INVALID_IDENTITY');
  }
  switch (value.type) {
    case 'text.delta':
      if (typeof value.text !== 'string') throw new Error('INVALID_TEXT');
      break;
    case 'approval.required':
      if (typeof value.approval_id !== 'string' || !value.approval_id ||
          !Number.isSafeInteger(value.revision) || value.revision < 1) {
        throw new Error('INVALID_APPROVAL');
      }
      break;
    case 'run.completed':
    case 'run.failed':
    case 'run.cancelled':
      break;
    default:
      throw new Error('UNKNOWN_EVENT');
  }
  return value;
}

export function initialState(run_id) {
  if (typeof run_id !== 'string' || !run_id) throw new Error('INVALID_RUN');
  return { run_id, last_seq: 0, status: 'running', cancel_requested: false,
    text: '', approval: null };
}

const terminal = new Set(['completed', 'failed', 'cancelled']);

export function applyEvent(state, input) {
  const event = decodeEvent(input);
  if (event.run_id !== state.run_id) return state;
  if (event.seq <= state.last_seq) return state;
  if (event.seq !== state.last_seq + 1) throw new Error('SEQUENCE_GAP');
  if (terminal.has(state.status)) throw new Error('EVENT_AFTER_TERMINAL');
  const next = { ...state, last_seq: event.seq };
  if (event.type === 'text.delta') next.text += event.text;
  else if (event.type === 'approval.required') {
    next.status = 'waiting_approval';
    next.approval = { id: event.approval_id, revision: event.revision };
  } else {
    next.status = event.type.slice(4);
    next.cancel_requested = false;
    next.approval = null;
  }
  return next;
}

export function requestCancel(state) {
  // 本地意图不是服务端终态，不推进 seq，也不执行任何外部动作。
  return terminal.has(state.status) ? state : { ...state, cancel_requested: true };
}

export function restoreSnapshot(raw) {
  const value = JSON.parse(raw);
  const statuses = new Set(['running', 'waiting_approval', ...terminal]);
  if (!value || typeof value.run_id !== 'string' || !value.run_id ||
      !Number.isSafeInteger(value.last_seq) || value.last_seq < 0 ||
      typeof value.text !== 'string' || typeof value.cancel_requested !== 'boolean' ||
      !statuses.has(value.status)) {
    throw new Error('INVALID_SNAPSHOT');
  }
  const approval = value.approval;
  if (approval !== null && (!approval || typeof approval.id !== 'string' || !approval.id ||
      !Number.isSafeInteger(approval.revision) || approval.revision < 1)) {
    throw new Error('INVALID_SNAPSHOT');
  }
  if ((value.status === 'waiting_approval') !== (approval !== null) ||
      (terminal.has(value.status) && value.cancel_requested)) throw new Error('INVALID_SNAPSHOT');
  return { run_id: value.run_id, last_seq: value.last_seq, status: value.status,
    cancel_requested: value.cancel_requested,
    text: value.text, approval: approval === null ? null : { ...approval } };
}

export function createScopeGate() {
  let generation = 0;
  return {
    advance: () => ++generation,
    accepts: token => token === generation,
  };
}

export function createDataStream(onData, { maxFrameChars = 65536 } = {}) {
  // 使用场景限定为 data: JSON 帧。event/id/retry 不实现，游标来自 JSON 的 seq。
  if (!Number.isSafeInteger(maxFrameChars) || maxFrameChars < 1) throw new Error('INVALID_LIMIT');
  const decoder = new TextDecoder('utf-8', { fatal: true });
  let pending = '';
  let scanFrom = 0;
  let data = [];
  let frameChars = 0;
  let ended = false;
  function line(text) {
    frameChars += text.length;
    if (frameChars > maxFrameChars) throw new Error('FRAME_TOO_LARGE');
    if (text === '') {
      const payload = data.length ? data.join('\n') : null;
      data = [];
      frameChars = 0;
      if (payload !== null) onData(payload);
      return;
    }
    if (text.startsWith(':')) return;
    const colon = text.indexOf(':');
    const field = colon < 0 ? text : text.slice(0, colon);
    let value = colon < 0 ? '' : text.slice(colon + 1);
    if (value.startsWith(' ')) value = value.slice(1);
    if (field === 'data') data.push(value);
  }
  function drain(final) {
    let start = 0;
    let index = scanFrom;
    for (; index < pending.length; index++) {
      const char = pending[index];
      if (char !== '\n' && char !== '\r') continue;
      if (char === '\r' && index === pending.length - 1 && !final) break;
      line(pending.slice(start, index));
      if (char === '\r' && pending[index + 1] === '\n') index++;
      start = index + 1;
    }
    pending = pending.slice(start);
    // 未结束的长行只扫描新到字节，避免逐字节输入时反复扫描旧前缀。
    scanFrom = index - start;
    if (frameChars + pending.length > maxFrameChars) throw new Error('FRAME_TOO_LARGE');
  }
  return {
    push(bytes) {
      if (ended) throw new Error('STREAM_ENDED');
      pending += decoder.decode(bytes, { stream: true });
      drain(false);
    },
    finish() {
      if (ended) throw new Error('STREAM_ENDED');
      ended = true;
      pending += decoder.decode();
      drain(true);
      // 没有空行结束的末帧按 SSE 规则不派发；EOF 不制造业务完成事件。
      pending = '';
      data = [];
    },
  };
}
