#!/usr/bin/env node
/*
 * MOTOR DE CARROSSEL — um comando gera tudo.
 *
 *   node carrossel/gerar.js carrossel/carrosseis/<pasta>/roteiro.json
 *
 * Saída (na pasta do roteiro):
 *   01.png … NN.png   slides finais 1080×1350
 *   capa/capa.png     capa gerada (quando o roteiro tem "capa")
 *   previa.jpg        UMA imagem com todos os slides (é a única que precisa ser conferida)
 * No terminal: um relatório curto com problemas encontrados (ou "OK").
 */
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const MIME = { ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp" };
const IMG_KEYS = ["foto", "pessoa", "recorte", "imagem", "imagem2", "logo"];
const toData = (p) => `data:${MIME[path.extname(p).toLowerCase()] || "image/jpeg"};base64,${fs.readFileSync(p).toString("base64")}`;

function inline(obj, baseDir, avisos) {
  for (const k of IMG_KEYS) {
    const v = obj[k];
    if (!v || typeof v !== "string" || /^(https?:|data:)/.test(v)) continue;
    const p = path.resolve(baseDir, v);
    if (!fs.existsSync(p)) { avisos.push(`imagem não encontrada: ${v}`); obj[k] = ""; continue; }
    obj[k] = toData(p);
  }
}

(async () => {
  const input = process.argv[2];
  if (!input) { console.error("Uso: node carrossel/gerar.js <roteiro.json>"); process.exit(1); }
  const jsonPath = path.resolve(input), dir = path.dirname(jsonPath);
  const data = JSON.parse(fs.readFileSync(jsonPath, "utf8"));
  const avisos = [];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });

  // 1) CAPA (opcional): gerada pelo motor de capa e inserida como slide 1
  if (data.capa) {
    const spec = JSON.parse(JSON.stringify(data.capa)); inline(spec, dir, avisos);
    await page.goto("file://" + path.join(__dirname, "capa-motor.html"));
    const r = await page.evaluate(s => window.loadCapa(s), spec);
    (r.avisos || []).forEach(a => avisos.push(a));
    fs.mkdirSync(path.join(dir, "capa"), { recursive: true });
    await (await page.$(".c")).screenshot({ path: path.join(dir, "capa", "capa.png") });
    if (!data.slides.length || data.slides[0].tipo !== "pronta" || data.slides[0].foto !== "capa/capa.png")
      data.slides.unshift({ tipo: "pronta", foto: "capa/capa.png" });
  }

  // 2) SLIDES
  inline(data.marca || {}, dir, avisos);
  data.slides.forEach(s => inline(s, dir, avisos));
  await page.goto("file://" + path.join(__dirname, "index.html") + "?render=1");
  await page.evaluate(() => { try { localStorage.clear(); } catch (e) {} });
  await page.evaluate(d => window.loadCarrossel(d), data);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);

  // 3) AUDITORIA automática (regras + transbordos + margens)
  const aud = await page.evaluate(() => {
    const out = [...document.querySelectorAll("#checks .err, #checks .warn")].map(e => e.textContent.trim());
    document.querySelectorAll(".slide").forEach((sl, i) => {
      const n = i + 1, body = sl.querySelector(".body");
      if (body && body.scrollHeight - body.clientHeight > 12) out.push(`slide ${n}: conteúdo passa da área em ${body.scrollHeight - body.clientHeight}px (corte texto/desenho)`);
      sl.querySelectorAll(".ttl,.st,.txt,.ex,.gancho,.ctt,.cta").forEach(e => {
        const r = e.getBoundingClientRect(), s = sl.getBoundingClientRect();
        if (r.right - s.left > 1080 - 60 || r.left - s.left < 60) out.push(`slide ${n}: elemento "${e.className}" fora da margem`);
      });
      const g = sl.querySelector(".gancho"); if (g && g.getBoundingClientRect().height > 70) out.push(`slide ${n}: gancho quebrou em 2 linhas (encurte)`);
    });
    return out;
  });
  aud.forEach(a => avisos.push(a));

  // 4) EXPORTA
  const slides = await page.$$(".slide");
  for (let i = 0; i < slides.length; i++) await slides[i].screenshot({ path: path.join(dir, String(i + 1).padStart(2, "0") + ".png") });

  // 5) PRÉVIA única (4 por linha, leve)
  const files = slides.map((_, i) => path.join(dir, String(i + 1).padStart(2, "0") + ".png"));
  const cols = 4, tw = 270, th = 338, gap = 8, rows = Math.ceil(files.length / cols);
  await page.setViewportSize({ width: cols * (tw + gap) + gap, height: rows * (th + gap) + gap });
  await page.setContent(`<body style="margin:0;background:#777;display:flex;flex-wrap:wrap;gap:${gap}px;padding:${gap}px">${files.map(f => `<img src="${toData(f)}" style="width:${tw}px;height:${th}px">`).join("")}</body>`);
  await page.waitForTimeout(200);
  await page.screenshot({ path: path.join(dir, "previa.jpg"), type: "jpeg", quality: 70, fullPage: true });
  await browser.close();

  // 6) RELATÓRIO curto
  const rel = path.relative(process.cwd(), dir);
  console.log(`${slides.length} slides → ${rel}/  ·  prévia: ${rel}/previa.jpg`);
  console.log(avisos.length ? avisos.map(a => "  ! " + a).join("\n") : "  OK — nenhum problema encontrado");
})();
