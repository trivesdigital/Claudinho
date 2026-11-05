#!/usr/bin/env node
/*
 * Exporta um roteiro de carrossel (.json) para PNGs 1080x1350 sem abrir o navegador.
 *
 *   node carrossel/exportar.js carrossel/exemplos/marca-pessoal.json [pasta-de-saida]
 *
 * Fotos no JSON podem ser URL (https://...) ou caminho local relativo ao próprio .json
 * (ex.: "fotos/capa.jpg"). Requer Playwright (npm i playwright).
 */
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const MIME = { ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp" };
const IMG_KEYS = ["foto", "recorte", "imagem", "imagem2", "logo"];

function inlineImages(obj, baseDir) {
  for (const k of IMG_KEYS) {
    const v = obj[k];
    if (!v || typeof v !== "string" || /^(https?:|data:)/.test(v)) continue;
    const p = path.resolve(baseDir, v);
    if (!fs.existsSync(p)) { console.warn(`  ! imagem não encontrada: ${v}`); obj[k] = ""; continue; }
    const mime = MIME[path.extname(p).toLowerCase()] || "image/jpeg";
    obj[k] = `data:${mime};base64,${fs.readFileSync(p).toString("base64")}`;
  }
}

(async () => {
  const input = process.argv[2];
  if (!input) { console.error("Uso: node carrossel/exportar.js roteiro.json [saida]"); process.exit(1); }
  const jsonPath = path.resolve(input);
  const data = JSON.parse(fs.readFileSync(jsonPath, "utf8"));
  const baseDir = path.dirname(jsonPath);
  inlineImages(data.marca || {}, baseDir);
  data.slides.forEach(s => inlineImages(s, baseDir));

  const outDir = path.resolve(process.argv[3] || path.join(__dirname, "saida", path.basename(jsonPath, ".json")));
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await page.goto("file://" + path.join(__dirname, "index.html") + "?render=1");
  await page.evaluate(() => { try { localStorage.clear(); } catch (e) {} });
  const n = await page.evaluate(d => window.loadCarrossel(d), data);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);

  const problems = await page.evaluate(() => [...document.querySelectorAll("#checks .err")].map(e => e.textContent));
  problems.forEach(p => console.warn("  ! " + p));

  const slides = await page.$$(".slide");
  for (let i = 0; i < slides.length; i++) {
    const file = path.join(outDir, String(i + 1).padStart(2, "0") + ".png");
    await slides[i].screenshot({ path: file });
    console.log("  ✓ " + path.relative(process.cwd(), file));
  }
  await browser.close();
  console.log(`\n${n} slides exportados em ${outDir}`);
})();
