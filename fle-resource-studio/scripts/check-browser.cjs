const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

(async () => {
  const root = path.resolve(__dirname, '..');
  const out = path.resolve(process.argv[2] || 'browser-evidence');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(pathToFileURL(path.join(root, 'reports/studio.html')).href);
    const themes = ['meubles', 'taches', 'routine', 'paysages', 'ecocitoyen'];
    let count = 0;
    for (const theme of themes) for (const support of ['guided', 'model', 'independent']) for (const lang of ['fr', 'es', 'en']) {
      await page.selectOption('#theme', theme);
      await page.selectOption('#support', support);
      await page.selectOption('#language', lang);
      const content = await page.locator('#content').innerText();
      if (!content.includes('Je peux') || content.length < 500) throw Error('Incomplete variant ' + theme);
      count++;
    }
    await page.selectOption('#theme', 'meubles');
    await page.selectOption('#support', 'guided');
    await page.selectOption('#language', 'es');
    const downloadEvent = page.waitForEvent('download');
    await page.click('#download');
    const download = await downloadEvent;
    const target = path.join(out, 'exported-kit.json');
    await download.saveAs(target);
    const kit = JSON.parse(fs.readFileSync(target));
    if (kit.theme !== 'meubles' || kit.support !== 'guided' || kit.aid_language !== 'es') throw Error('Incorrect export');
    await page.screenshot({ path: path.join(out, 'studio-desktop.png'), fullPage: true });
    await page.setViewportSize({ width: 390, height: 844 });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
    if (overflow) throw Error('Horizontal overflow at 390px');
    await page.screenshot({ path: path.join(out, 'studio-mobile.png'), fullPage: true });
    await page.setViewportSize({ width: 1280, height: 900 });
    const printed = [];
    for (const theme of themes) {
      await page.goto(pathToFileURL(path.join(root, 'kits', theme, 'kit.html')).href);
      await page.emulateMedia({ media: 'print' });
      for (const cls of ['.teacher', '.answers']) {
        const visible = await page.locator(cls).evaluateAll(es => es.some(e => getComputedStyle(e).display !== 'none'));
        if (visible) throw Error('Teacher or answers visible in print');
      }
      const pdf = await page.pdf({ path: path.join(out, theme + '-A4.pdf'), format: 'A4', printBackground: true });
      const pages = (pdf.toString('latin1').match(/\/Type\s*\/Page\b/g) || []).length;
      if (pages !== 2) throw Error(theme + ': expected 2 A4 pages, got ' + pages);
      if (theme === 'meubles') await page.screenshot({ path: path.join(out, 'meubles-print.png'), fullPage: true });
      printed.push(theme);
    }
    if (errors.length) throw Error(errors.join('\n'));
    fs.writeFileSync(path.join(out, 'browser-validation.json'), JSON.stringify({ checkedAt: new Date().toISOString(), browser: await browser.version(), variants: count, jsonExport: true, mobileOverflow: false, printTeacherAndAnswersHidden: true, pdfs: printed, pageErrors: errors, humanVisualReview: 'pending', speechAndPhysicalPrinting: 'not tested' }, null, 2));
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exit(1); });
