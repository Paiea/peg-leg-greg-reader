(() => {
  const target = document.querySelector('[data-light-continue]');
  if (!target) return;

  let chapter = null;
  const latest = Number(target.dataset.latestChapter || '');
  try { chapter = Number(localStorage.getItem('plg:lastLightChapter') || ''); } catch (_) {}

  if (!Number.isInteger(chapter) || chapter < 1) return;
  if (!Number.isInteger(latest) || latest < 1 || chapter > latest) return;

  const link = document.createElement('a');
  link.href = `../light.html?chapter=${chapter}`;
  link.textContent = `Continue reading · Chapter ${chapter}`;
  target.replaceChildren(link);
  target.hidden = false;
})();
