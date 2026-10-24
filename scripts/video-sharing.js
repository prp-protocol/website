// WhatsApp links and native disclosure controls work without JavaScript.
document.querySelectorAll('[data-copy-link]').forEach(button => {
  button.hidden = false;
  button.addEventListener('click', async () => {
    const pt = document.documentElement.lang.toLowerCase().startsWith('pt');
    const status = button.parentElement.querySelector('.share-status');
    try {
      await navigator.clipboard.writeText(button.dataset.copyLink);
      status.textContent = pt ? 'Link copiado.' : 'Link copied.';
    } catch {
      status.textContent = pt ? 'Copie este link: ' : 'Copy this link: ';
      const input = document.createElement('input');
      input.readOnly = true; input.value = button.dataset.copyLink;
      input.setAttribute('aria-label', pt ? 'Link do vídeo' : 'Video link');
      status.append(input); input.focus(); input.select();
    }
  });
});
function revealFragment() {
  let id;
  try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
  const target = document.getElementById(id);
  if (!target) return;
  let details = target.closest('details');
  while (details) { details.open = true; details = details.parentElement.closest('details'); }
  if (target.closest('.video-details')) target.scrollIntoView();
}
window.addEventListener('hashchange', revealFragment);
revealFragment();
let printState;
window.addEventListener('beforeprint', () => {
  printState = [...document.querySelectorAll('.video-details')].map(el => [el, el.open]);
  printState.forEach(([el]) => { el.open = true; });
});
window.addEventListener('afterprint', () => printState?.forEach(([el, open]) => { el.open = open; }));
