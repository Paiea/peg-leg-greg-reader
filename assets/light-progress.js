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

/* Progressive enhancement for the book-first home-page IA. The generated
   contents remain complete and crawlable; this only changes the default
   presentation while the generator-owned markup catches up with main. */
(() => {
  const home = document.querySelector('main.home');
  const contents = document.querySelector('#chapters, #books');
  if (!home || !contents) return;

  contents.id = 'books';
  contents.setAttribute('aria-labelledby', 'books-heading');

  const section = contents.closest('.home-chapters');
  const kicker = section?.querySelector('.home-section-head .home-kicker');
  const heading = section?.querySelector('.home-section-head h2');
  if (kicker) kicker.textContent = 'The novel';
  if (heading) {
    heading.id = 'books-heading';
    heading.textContent = 'Books';
  }

  document.querySelectorAll('.reader-book[open], .reader-act[open]').forEach((node) => node.removeAttribute('open'));

  const actions = home.querySelector('.home-actions');
  if (!actions) return;
  actions.replaceChildren();
  const links = [
    ['Begin Reading', 'chapters/001.html', 'start primary-action'],
    ['Text Reader', 'light/index.html', 'secondary-action'],
    ['Illustrated Reader', '#books', 'secondary-action'],
    ['Illustrations', 'art.html', 'tertiary-action'],
  ];
  for (const [label, href, className] of links) {
    const link = document.createElement('a');
    link.textContent = label;
    link.href = href;
    link.className = className;
    actions.append(link);
  }
})();
