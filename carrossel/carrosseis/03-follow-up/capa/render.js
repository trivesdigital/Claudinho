const { chromium } = require("playwright"); const path = require("path");
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto("file://" + path.join(__dirname, "capa.html")); await p.evaluate(() => document.fonts.ready); await p.waitForSelector('body[data-ok]'); await p.waitForTimeout(200);
  await (await p.$(".c")).screenshot({ path: path.join(__dirname, "capa.png") }); await b.close(); console.log("ok");
})();
