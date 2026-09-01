(() => {
  const target = document.querySelector('[data-light-continue]');
  if (!target) return;
  let chapter = null;
  try { chapter = Number.parseInt(localStorage.getItem('plg:lastLightChapter') || '', 10); } catch (_) {}
  if (!chapter || chapter < 1) return;
  const link = document.createElement('a');
  link.href = `../light.html?chapter=${chapter}`;
  link.textContent = `Continue reading · Chapter ${chapter}`;
  target.replaceChildren(link);
  target.hidden = false;
})();
