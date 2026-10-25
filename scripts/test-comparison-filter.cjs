// Website-owned Chromium check of actual local/public HTML, no injected UI fixture.
const fs = require('fs');
const path = require('path');
const {spawn} = require('child_process');
const [htmlPath, dataPath, outputDir] = process.argv.slice(2);
if (!outputDir) throw Error('Usage: node tools/test_comparison_yes_filter.cjs HTML DATA_JSON OUTPUT_DIR');
fs.mkdirSync(outputDir, {recursive: true});
const data = JSON.parse(fs.readFileSync(dataPath));
const criteria = data.criteria || data.rows.map(r => ({id: r[0]}));
const columns = data.columns.map(c => ({id: c.id || c[0]}));
const verdicts = Object.fromEntries(data.cells.map(c => [c.id || c.feature + '-' + c.stack, c.status]));
const targetURL = /^https?:/.test(htmlPath) ? htmlPath : 'file://' + path.resolve(htmlPath);
const browser = spawn('chromium', ['--headless', '--no-sandbox', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--remote-debugging-pipe', '--user-data-dir=' + path.resolve(outputDir, 'browser-profile')], {stdio: ['ignore', 'ignore', 'ignore', 'pipe', 'pipe']});
let nextId = 0, buffer = '', session;
const pending = new Map();
browser.stdio[4].on('data', chunk => {
  buffer += chunk.toString();
  let end;
  while ((end = buffer.indexOf('\0')) >= 0) {
    const message = JSON.parse(buffer.slice(0, end)); buffer = buffer.slice(end + 1);
    if (pending.has(message.id)) { const callback = pending.get(message.id); pending.delete(message.id); message.error ? callback.reject(Error(JSON.stringify(message.error))) : callback.resolve(message.result); }
  }
});
function send(method, params = {}, scoped = true) {
  return new Promise((resolve, reject) => {
    const id = ++nextId; pending.set(id, {resolve, reject});
    browser.stdio[3].write(JSON.stringify({id, method, params, ...(scoped && session ? {sessionId: session} : {})}) + '\0');
  });
}
async function evaluate(expression) {
  const r = await send('Runtime.evaluate', {expression, returnByValue: true, awaitPromise: true});
  if (r.exceptionDetails) throw Error(JSON.stringify(r.exceptionDetails));
  return r.result.value;
}
function assert(condition, message) { if (!condition) throw Error(message); }
const timeout = setTimeout(() => { browser.kill(); process.exit(2); }, 55000);
(async () => {
  const target = await send('Target.createTarget', {url: 'about:blank'}, false);
  session = (await send('Target.attachToTarget', {targetId: target.targetId, flatten: true}, false)).sessionId;
  await send('Page.enable');
  await send('Page.navigate', {url: targetURL});
  await evaluate('new Promise(resolve => { const timer = setInterval(() => { if (document.querySelector("[data-yes-filter-ready]")) {clearInterval(timer);resolve(true);} }, 25); })');
  const originalLinks = await evaluate('Array.from(document.querySelectorAll(".matrix td a")).map(a => a.getAttribute("href"))');
  async function select(ids) {
    await evaluate(`(() => { const selected = ${JSON.stringify(ids)}; const inputs = document.querySelectorAll('.yes-filter-toggle input'); inputs.forEach(i => i.checked = selected.includes(i.id.replace('require-yes-', ''))); inputs[0].dispatchEvent(new Event('change', {bubbles:true})); })()`);
    const actual = await evaluate('Array.from(document.querySelectorAll(".matrix thead th[id^=col-]")).filter(h => !h.hidden).map(h => h.id.slice(4))');
    const expected = columns.filter(c => ids.every(id => verdicts[id + '-' + c.id] === 'Y')).map(c => c.id);
    assert(JSON.stringify(actual) === JSON.stringify(expected), 'Wrong matches for ' + ids);
    assert(await evaluate(`document.querySelector('.yes-filter-result').textContent.startsWith('${expected.length} of ${columns.length} stacks shown.')`), 'Live result count');
    assert(await evaluate(`Array.from(document.querySelectorAll('.matrix tbody tr')).filter(r=>r.querySelector('td')).every(r=>!r.hidden && getComputedStyle(r).display!=='none')`), 'Criterion rows remain accessible');
    assert(await evaluate(`Array.from(document.querySelectorAll('.matrix tbody tr')).filter(r => r.querySelector('td')).every(r => Array.from(r.querySelectorAll('td')).filter(c => !c.hidden).length === ${expected.length})`), 'Header/cell alignment');
    assert(await evaluate(`Array.from(document.querySelectorAll('.matrix tbody th[colspan]')).every(th => th.colSpan === ${expected.length + 1})`), 'Rowgroup span alignment');
    return expected;
  }
  let tested = 0;
  for (const width of [1440, 390]) {
    await send('Emulation.setDeviceMetricsOverride', {width, height: 900, deviceScaleFactor: 1, mobile: false});
    assert(await evaluate('innerWidth')===width, 'Actual viewport width');
    assert(await evaluate('document.documentElement.scrollWidth <= innerWidth'), 'No page-wide overflow');
    await select([]);
    assert(await evaluate('document.querySelectorAll(".matrix th[scope=row]").length')===criteria.length,'All criterion rows retained');
    for(const fraction of [0,.5,1]) {
      await evaluate(`document.querySelector('.wrap').scrollLeft=(document.querySelector('.wrap').scrollWidth-document.querySelector('.wrap').clientWidth)*${fraction}`);
      assert(await evaluate('document.querySelector(".wrap").scrollLeft>=0'),'Horizontal scroll');
    }
    await evaluate('document.querySelector(".wrap").scrollLeft=0');
    for (const r of criteria) { await select([r.id]); tested++; }
    await select(['F01', 'E01']);
    await select(criteria.map(r => r.id));
    assert(await evaluate('!document.querySelector(".yes-filter-empty").hidden'), 'Expected empty-state message');
    await evaluate('document.querySelector(".yes-filter-panel button").focus();document.querySelector(".yes-filter-panel button").click()');
    assert(await evaluate('document.activeElement===document.querySelector(".yes-filter-panel button")'),'Reset focus retained');
    assert(await evaluate('document.querySelectorAll(".yes-filter-toggle input:checked").length === 0'), 'Reset checkboxes');
    await select([]);
    const first = criteria[0].id;
    await evaluate(`document.getElementById('require-yes-${first}').focus()`);
    await send('Input.dispatchKeyEvent', {type: 'keyDown', key: ' ', code: 'Space', windowsVirtualKeyCode: 32});
    await send('Input.dispatchKeyEvent', {type: 'keyUp', key: ' ', code: 'Space', windowsVirtualKeyCode: 32});
    assert(await evaluate(`document.getElementById('require-yes-${first}').checked`), 'Space key must toggle');
    assert(await evaluate(`document.activeElement.id === 'require-yes-${first}'`), 'Focus must remain on checkbox');
    await select(['F01', 'E01']);
    await evaluate('document.querySelector(".yes-filter-panel").scrollIntoView()');
    const shot = await send('Page.captureScreenshot', {format: 'png'});
    fs.writeFileSync(path.join(outputDir, 'filter-' + width + '.png'), Buffer.from(shot.data, 'base64'));
    await send('Emulation.setEmulatedMedia', {media: 'print'});
    assert(await evaluate('getComputedStyle(document.querySelector(".yes-filter-toggle")).display === "none"'), 'Print hides controls');
    assert(await evaluate('getComputedStyle(document.querySelector(".yes-filter-result")).display !== "none"'), 'Print retains selection summary');
    await send('Emulation.setEmulatedMedia', {media: ''});
    await select([]);
  }
  assert(JSON.stringify(originalLinks) === JSON.stringify(await evaluate('Array.from(document.querySelectorAll(".matrix td a")).map(a => a.getAttribute("href"))')), 'Evidence links changed');
  await send('Emulation.setScriptExecutionDisabled', {value: true});
  await send('Page.reload');
  // DOM parsing remains available to CDP even with page scripts disabled.
  await new Promise(resolve => setTimeout(resolve, 400));
  assert(await evaluate(`document.querySelectorAll('.yes-filter-toggle').length === 0 && Array.from(document.querySelectorAll('.matrix thead th[id^=col-]')).filter(h => !h.hidden).length === ${columns.length}`), 'Static no-JavaScript fallback');
  const report = {status: 'PASS', targetURL, revision: data.revision, singleCriterionCases: tested, viewportWidths: [1440, 390], allCriteriaEmptyState: true, conjunction: true, keyboardSpaceAndFocus: true, reset: true, unchangedEvidenceLinks: originalLinks.length, printControlsHidden: true, noScriptFallback: true, rowgroupSpans: true};
  fs.writeFileSync(path.join(outputDir, 'validation.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report));
})().catch(error => { console.error(error); process.exitCode = 1; }).finally(() => { clearTimeout(timeout); browser.kill(); });
