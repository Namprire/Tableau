import fs from 'node:fs/promises';
import path from 'node:path';

const endpoint = process.env.CDP_ENDPOINT ?? 'http://127.0.0.1:9223/json';
const outputDir = path.resolve('docs/media');
const targets = await fetch(endpoint).then((response) => response.json());
const target = targets.find((item) => item.type === 'page');

if (!target?.webSocketDebuggerUrl) {
  throw new Error(`No debuggable page found at ${endpoint}`);
}

await fs.mkdir(outputDir, { recursive: true });

const socket = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => {
  socket.addEventListener('open', resolve, { once: true });
  socket.addEventListener('error', reject, { once: true });
});

let nextId = 0;
const pending = new Map();

socket.addEventListener('message', ({ data }) => {
  const message = JSON.parse(data);
  if (!message.id || !pending.has(message.id)) return;
  const { resolve, reject } = pending.get(message.id);
  pending.delete(message.id);
  if (message.error) reject(new Error(message.error.message));
  else resolve(message.result);
});

function command(method, params = {}) {
  const id = ++nextId;
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject });
    socket.send(JSON.stringify({ id, method, params }));
  });
}

const wait = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

async function evaluate(expression) {
  return command('Runtime.evaluate', {
    expression,
    awaitPromise: true,
    returnByValue: true
  });
}

async function capture(name, selector, offset = 0) {
  await evaluate(`(() => {
    const node = document.querySelector(${JSON.stringify(selector)});
    if (!node) throw new Error('Missing selector: ${selector}');
    const reduceMotion = document.createElement('style');
    reduceMotion.textContent = '* { animation-duration: 0s !important; transition-duration: 0s !important; }';
    document.head.appendChild(reduceMotion);
    const top = node.getBoundingClientRect().top + window.scrollY + ${offset};
    window.scrollTo({ top, behavior: 'instant' });
  })()`);
  await wait(650);
  const { data } = await command('Page.captureScreenshot', {
    format: 'png',
    captureBeyondViewport: false
  });
  await fs.writeFile(path.join(outputDir, `${name}.png`), Buffer.from(data, 'base64'));
}

await command('Page.enable');
await command('Runtime.enable');
await command('Emulation.setDeviceMetricsOverride', {
  width: 1440,
  height: 1000,
  deviceScaleFactor: 1,
  mobile: false
});

await evaluate("window.scrollTo({ top: 0, behavior: 'instant' })");
await wait(500);
await capture('hero', 'main', 0);
await capture('quiz', '.quiz-shell', -90);
await capture('evidence', '#exposure-story', 1800);
await capture('workday', '.workday-scrolly', 1600);
await capture('handoff', '#handoff-simulation', -80);
await evaluate("document.querySelector('#handoff-simulation .run')?.click()");
await wait(2300);
await capture('handoff-result', '#handoff-simulation', -80);
await capture('comparison', '.contrast', -80);
await capture('explorer', '#explore', 80);

socket.close();
console.log(`Captured README media in ${outputDir}`);
