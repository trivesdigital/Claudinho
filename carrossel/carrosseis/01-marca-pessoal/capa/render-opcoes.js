const { chromium } = require("playwright"); const path = require("path");
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const v of ["a","b","cc"]) {
    await p.goto("file://" + path.join(__dirname, "opcoes.html") + "?v=" + v);
    await p.waitForSelector("body[data-ok]"); await p.waitForTimeout(250);
    await (await p.$(".c")).screenshot({ path: path.join(__dirname, `opcao-${v==="cc"?"c":v}.png`) });
  }
  await b.close(); console.log("ok");
})();
