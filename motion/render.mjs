// Renders intro.html frame-by-frame (deterministic, beat-locked) and muxes with build/music.wav.
// usage (run inside the intro folder): [HTML=shorts.html] node ../render.mjs [out.mp4] [--preview t1,t2,...]
// canvas size (16:9 or 9:16) is read from the page's <canvas>.
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { execSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';

// playwright: local install first, then the global one (cloud containers ship it globally)
let chromium;
try { ({ chromium } = await import('playwright')); }
catch { const g = process.env.PW_ROOT || execSync('npm root -g').toString().trim(); ({ chromium } = await import(pathToFileURL(path.join(g, 'playwright', 'index.mjs')).href)); }

const FF = process.env.FFMPEG || 'ffmpeg';
const out = process.argv[2] || 'build/shiny-peace-intro.mp4';
const previewArg = process.argv.indexOf('--preview');
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.addInitScript(() => { window.__RENDER_MODE__ = true; });
// serve over http (file:// images would taint the canvas and block frame export)
const root = path.resolve('..'), MIME = { '.html': 'text/html', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2', '.wav': 'audio/wav' };
const server = http.createServer(async (req, res) => {
  const f = path.join(root, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!f.startsWith(root)) { res.writeHead(403).end(); return; }
  try { res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' }).end(await readFile(f)); }
  catch { res.writeHead(404).end(); }
}).listen(0, '127.0.0.1');
await new Promise(r => server.once('listening', r));
await page.goto(`http://127.0.0.1:${server.address().port}/${path.basename(process.cwd())}/${process.env.HTML || 'intro.html'}`);
const size = await page.evaluate(() => { const c = document.getElementById('c'); return { width: c.width, height: c.height }; });
await page.setViewportSize(size);
await page.evaluate(async () => { await document.fonts.load('900 100px Archivo'); await document.fonts.load('700 20px JBMono'); await document.fonts.ready; if (window.READY) await window.READY; });

const grab = t => page.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/png').split(',')[1]; }, t);

if (previewArg > 0) {
  for (const t of process.argv[previewArg + 1].split(',').map(Number)) writeFileSync(`build/prev_${t.toFixed(2)}.png`, Buffer.from(await grab(t), 'base64'));
} else {
  const { DUR, FPS } = await page.evaluate(() => ({ DUR: window.DUR, FPS: window.FPS }));
  const n = Math.round(DUR * FPS);
  const ff = spawn(FF, ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-i', 'build/music.wav',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-maxrate', '12M', '-bufsize', '24M', '-pix_fmt', 'yuv420p',  // cap keeps 15s under ~25MB even with snow/grain
    '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = 0; f < n; f++) {
    const buf = Buffer.from(await grab(f / FPS), 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 60 === 0) console.log(`frame ${f}/${n}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log('wrote', out);
}
await browser.close();
server.close();
