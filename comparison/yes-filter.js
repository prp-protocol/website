/* Progressive enhancement: verdicts remain in the server-rendered table. */
(() => {
  'use strict';
  const table = document.querySelector('table.matrix');
  if (!table || table.dataset.yesFilterReady) return;
  const columns = Array.from(table.querySelectorAll('thead th[id^="col-"]'));
  const rows = Array.from(table.querySelectorAll('tbody tr')).filter(row => row.querySelector('td'));
  const entries = rows.map(row => {
    const heading = row.querySelector('th[scope="row"]');
    const id = (row.id || heading?.id || '').replace(/^row-/, '');
    const cells = Array.from(row.querySelectorAll('td'));
    return {row, heading, id, cells};
  });
  // A changed renderer must not produce a partially functioning filter.
  if (!columns.length || !entries.length || entries.some(r => !r.heading || !r.id || r.cells.length !== columns.length)) return;

  const wrap = table.closest('.wrap') || table.parentElement;
  const panel = document.createElement('div');
  panel.className = 'yes-filter-panel';
  const instructions = document.createElement('p');
  instructions.id = 'yes-filter-help';
  instructions.textContent = 'Select “Require Yes” on any criterion to show only stacks with Yes on every selected row. No and Pending do not match. Other rows remain visible for comparison.';
  const result = document.createElement('p');
  result.className = 'yes-filter-result';
  result.setAttribute('role', 'status');
  result.setAttribute('aria-live', 'polite');
  result.setAttribute('aria-atomic', 'true');
  const reset = document.createElement('button');
  reset.type = 'button';
  reset.textContent = 'Clear filters';
  const empty = document.createElement('p');
  empty.className = 'yes-filter-empty';
  empty.textContent = 'No stack matches every selected criterion. Uncheck a requirement or clear the filters.';
  empty.hidden = true;
  panel.append(instructions, reset, result, empty);
  wrap.before(panel);

  const groups = Array.from(table.querySelectorAll('tbody th[colspan]'));
  const originalSpans = groups.map(th => th.colSpan);
  const columnLinks = columns.map(th => Array.from(document.querySelectorAll('a[href="#' + th.id + '"]')));
  for (const entry of entries) {
    const label = document.createElement('label');
    label.className = 'yes-filter-toggle';
    const input = document.createElement('input');
    input.type = 'checkbox';
    input.id = 'require-yes-' + entry.id;
    input.setAttribute('aria-label', 'Require Yes for ' + entry.id);
    input.setAttribute('aria-describedby', instructions.id);
    label.append(input, document.createTextNode('Require Yes'));
    entry.heading.append(label);
    entry.input = input;
    input.addEventListener('change', update);
  }

  function update() {
    const required = entries.filter(entry => entry.input.checked);
    const matches = columns.map((_, i) => required.every(entry => entry.cells[i].classList.contains('Y')));
    const count = matches.filter(Boolean).length;
    columns.forEach((heading, i) => {
      heading.hidden = !matches[i];
      entries.forEach(entry => { entry.cells[i].hidden = !matches[i]; });
      columnLinks[i].forEach(link => { link.hidden = !matches[i]; });
    });
    groups.forEach((th, i) => { th.colSpan = required.length ? count + 1 : originalSpans[i]; });
    table.classList.toggle('yes-filter-active', required.length > 0);
    result.textContent = count + ' of ' + columns.length + ' stacks shown. ' +
      (required.length ? 'Required Yes: ' + required.map(entry => entry.id).join(', ') + '.' : 'No filters selected.');
    empty.hidden = count !== 0;
    // Keep the button enabled so keyboard focus is retained after clearing.
  }
  reset.addEventListener('click', () => {
    entries.forEach(entry => { entry.input.checked = false; });
    update();
  });
  table.dataset.yesFilterReady = 'true';
  update();
})();
