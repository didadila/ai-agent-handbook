import test from 'node:test';
import assert from 'node:assert/strict';
import { applyEvent, createDataStream, createScopeGate, decodeEvent,
  initialState, requestCancel, restoreSnapshot } from './workbench-core.mjs';

const event = (seq, type = 'text.delta', extra = {}) =>
  ({ schema_version: 1, run_id: 'run-A', seq, type, text: '好', ...extra });
const encode = text => new TextEncoder().encode(text);
const frame = value => `data: ${JSON.stringify(value)}\r\n\r\n`;
function consume(chunks) {
  let state = initialState('run-A');
  const stream = createDataStream(raw => { state = applyEvent(state, JSON.parse(raw)); });
  for (const chunk of chunks) stream.push(chunk);
  stream.finish();
  return state;
}

test('all two-part byte boundaries preserve UTF-8, CRLF and event order', () => {
  const bytes = encode(frame(event(1)) + frame(event(2, 'run.completed')));
  for (let split = 0; split <= bytes.length; split++) {
    assert.deepEqual(consume([bytes.slice(0, split), bytes.slice(split)]),
      { run_id: 'run-A', last_seq: 2, status: 'completed', cancel_requested: false,
        text: '好', approval: null });
  }
});

test('one-byte chunks and repeated delivery apply each sequence once', () => {
  const bytes = encode(frame(event(1)) + frame(event(1)) + frame(event(2)));
  const state = consume(Array.from(bytes, (_, index) => bytes.slice(index, index + 1)));
  assert.equal(state.text, '好好'); // 相同文字、不同 seq 都保留。
  assert.equal(state.last_seq, 2);
});

test('multiline data, comments, LF and lone CR follow frame boundaries', () => {
  const values = [];
  const stream = createDataStream(value => values.push(value));
  stream.push(encode(': heartbeat\r\rdata: first\ndata: second\n\ndata: third\r\r'));
  stream.finish();
  assert.deepEqual(values, ['first\nsecond', 'third']);
});

test('EOF discards an incomplete frame and never marks completion', () => {
  const state = consume([encode(frame(event(1)) + 'data: ' + JSON.stringify(event(2, 'run.completed')))]);
  assert.equal(state.status, 'running');
  assert.equal(state.last_seq, 1);
});

test('a gap cannot mutate the already applied projection', () => {
  const state = applyEvent(initialState('run-A'), event(1));
  assert.throws(() => applyEvent(state, event(3)), /SEQUENCE_GAP/);
  assert.equal(state.text, '好');
  assert.equal(state.last_seq, 1);
});

test('replay after restoring projection and cursor does not duplicate text', () => {
  const saved = JSON.stringify(applyEvent(initialState('run-A'), event(1)));
  let state = restoreSnapshot(saved);
  state = applyEvent(state, event(1));
  state = applyEvent(state, event(2));
  assert.equal(state.text, '好好');
  assert.equal(state.last_seq, 2);
});

test('snapshot restores a waiting approval and rejects malformed snapshots', () => {
  const state = applyEvent(initialState('run-A'), event(1, 'approval.required',
    { approval_id: 'approval-1', revision: 3 }));
  assert.deepEqual(restoreSnapshot(JSON.stringify(state)), state);
  assert.throws(() => restoreSnapshot(JSON.stringify({ ...state, approval: null })), /INVALID_SNAPSHOT/);
  assert.throws(() => restoreSnapshot(JSON.stringify({ ...state, last_seq: '1' })), /INVALID_SNAPSHOT/);
});

test('valid foreign run events cannot change current run', () => {
  const state = initialState('run-A');
  assert.equal(applyEvent(state, event(1, 'text.delta', { run_id: 'run-B' })), state);
});

test('unknown event, unsupported version and invalid payload are rejected', () => {
  assert.throws(() => decodeEvent(event(1, 'future.event')), /UNKNOWN_EVENT/);
  assert.throws(() => decodeEvent(event(1, 'text.delta', { schema_version: 2 })), /UNSUPPORTED_VERSION/);
  assert.throws(() => decodeEvent(event('1')), /INVALID_IDENTITY/);
  assert.throws(() => decodeEvent(event(1, 'text.delta', { text: 5 })), /INVALID_TEXT/);
  assert.throws(() => decodeEvent(event(1, 'approval.required')), /INVALID_APPROVAL/);
});

test('cancel intent becomes terminal only after a server event', () => {
  let state = requestCancel(initialState('run-A'));
  assert.equal(state.status, 'running');
  assert.equal(state.cancel_requested, true);
  assert.equal(state.last_seq, 0);
  state = applyEvent(state, event(1, 'run.cancelled'));
  assert.equal(state.status, 'cancelled');
  assert.equal(state.cancel_requested, false);
});

test('completion can win a cancellation race without pretending rollback', () => {
  let state = requestCancel(initialState('run-A'));
  state = applyEvent(state, event(1, 'run.completed'));
  assert.equal(state.status, 'completed');
  assert.equal(state.cancel_requested, false);
  assert.equal(requestCancel(state), state);
});

test('terminal replay is harmless, new events after terminal are rejected', () => {
  const state = applyEvent(initialState('run-A'), event(1, 'run.completed'));
  assert.equal(applyEvent(state, event(1, 'run.completed')), state);
  assert.throws(() => applyEvent(state, event(2)), /EVENT_AFTER_TERMINAL/);
});

test('old query result cannot pass the current scope gate', async () => {
  const gate = createScopeGate();
  const first = gate.advance();
  let finish;
  const oldRequest = new Promise(resolve => { finish = resolve; });
  const second = gate.advance();
  const shown = [];
  if (gate.accepts(second)) shown.push('new');
  const oldCommit = oldRequest.then(value => { if (gate.accepts(first)) shown.push(value); });
  finish('old');
  await oldCommit;
  assert.deepEqual(shown, ['new']);
});

test('oversized unfinished frame cannot grow without a bound', () => {
  const stream = createDataStream(() => {}, { maxFrameChars: 12 });
  assert.throws(() => stream.push(encode('data: ' + 'x'.repeat(20))), /FRAME_TOO_LARGE/);
});

test('invalid UTF-8 is rejected instead of silently changing business data', () => {
  const stream = createDataStream(() => {});
  assert.throws(() => stream.push(new Uint8Array([0xff])), TypeError);
});

test('a finished transport cannot accept new data', () => {
  const stream = createDataStream(() => {});
  stream.finish();
  assert.throws(() => stream.push(encode('data: later\n\n')), /STREAM_ENDED/);
});

test('cancel intent preserves the last authoritative waiting-approval state', () => {
  const waiting = applyEvent(initialState('run-A'), event(1, 'approval.required',
    { approval_id: 'approval-1', revision: 3 }));
  const pending = requestCancel(waiting);
  assert.equal(pending.status, 'waiting_approval');
  assert.equal(pending.cancel_requested, true);
  assert.deepEqual(pending.approval, waiting.approval);
  assert.deepEqual(restoreSnapshot(JSON.stringify(pending)), pending);
});

test('snapshot cannot combine a running/terminal state with contradictory approval or intent', () => {
  const state = initialState('run-A');
  assert.throws(() => restoreSnapshot(JSON.stringify({ ...state,
    approval: { id: 'approval-1', revision: 1 } })), /INVALID_SNAPSHOT/);
  assert.throws(() => restoreSnapshot(JSON.stringify({ ...state,
    status: 'completed', cancel_requested: true })), /INVALID_SNAPSHOT/);
  assert.throws(() => restoreSnapshot(JSON.stringify({ ...state,
    cancel_requested: 'yes' })), /INVALID_SNAPSHOT/);
});

test('a BOM and an empty data field follow the documented data-frame subset', () => {
  const seen = [];
  const stream = createDataStream(raw => seen.push(raw));
  stream.push(encode('\uFEFFdata:\n\n'));
  stream.finish();
  assert.deepEqual(seen, ['']);
});

test('over-limit frames are rejected even when the delimiter arrives in the same chunk', () => {
  const stream = createDataStream(() => {}, { maxFrameChars: 12 });
  assert.throws(() => stream.push(encode('data: ' + 'x'.repeat(20) + '\n\n')), /FRAME_TOO_LARGE/);
});
