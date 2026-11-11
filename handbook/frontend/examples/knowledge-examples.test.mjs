import test from 'node:test';
import assert from 'node:assert/strict';

function deferred() {
  let resolve, reject;
  const promise = new Promise((yes, no) => { resolve = yes; reject = no; });
  return { promise, resolve, reject };
}

test('object spread keeps the nested identity from the teaching example', () => {
  const original = { message: { text: '旧答案' } };
  const draft = { ...original };
  draft.message.text = '新答案';
  assert.equal(original.message.text, '新答案');
  assert.equal(original.message, draft.message);
});

test('copying the modified path preserves the historical value', () => {
  const original = { message: { text: '旧答案' } };
  const draft = { ...original, message: { ...original.message, text: '新答案' } };
  assert.equal(original.message.text, '旧答案');
  assert.notEqual(original.message, draft.message);
});

test('var callbacks share the final loop binding', () => {
  const jobs = [];
  for (var index = 0; index < 3; index++) jobs.push(() => index);
  assert.deepEqual(jobs.map(run => run()), [3, 3, 3]);
});

test('let callbacks preserve independent per-iteration bindings', () => {
  const jobs = [];
  for (let index = 0; index < 3; index++) jobs.push(() => index);
  assert.deepEqual(jobs.map(run => run()), [0, 1, 2]);
});

test('a rejected race does not cancel a later successful underlying operation', async () => {
  const work = deferred();
  const timeout = deferred();
  let commits = 0;
  const operation = work.promise.then(() => { commits++; });
  const outer = Promise.race([operation, timeout.promise]);
  timeout.reject(new Error('timeout'));
  await assert.rejects(outer, /timeout/);
  assert.equal(commits, 0);
  work.resolve();
  await operation;
  assert.equal(commits, 1);
});

test('Promise.all rejection does not cancel other already-started inputs', async () => {
  const first = deferred();
  const second = deferred();
  let finished = false;
  const remaining = second.promise.then(() => { finished = true; });
  const all = Promise.all([first.promise, remaining]);
  first.reject(new Error('first failed'));
  await assert.rejects(all, /first failed/);
  second.resolve();
  await remaining;
  assert.equal(finished, true);
});
