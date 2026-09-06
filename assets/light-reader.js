(() => {
  const titleNode = document.querySelector('[data-light-title]');
  const numberNode = document.querySelector('[data-light-number]');
  const proseNode = document.querySelector('[data-light-prose]');
  const tocNode = document.querySelector('[data-light-toc]');
  const statusNode = document.querySelector('[data-light-status]');
  const bottomNode = document.querySelector('[data-light-bottom]');
  const switchNode = document.querySelector('[data-light-switch]');
  const jumpForm = document.querySelector('[data-light-jump]');
  const jumpInput = document.querySelector('#light-chapter');

  const params = new URLSearchParams(location.search);
  const requested = Number(params.get('chapter') || '');
  const lightHref = (chapter) => `light.html?chapter=${chapter}`;
  const setStatus = (text) => { if (statusNode) statusNode.textContent = text; };

  const parsePublishedIndex = (html) => {
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const chapters = [];
    doc.querySelectorAll('#books a[href*="chapters/"]').forEach((a) => {
      const match = /chapters\/(\d+)\.html/.exec(a.getAttribute('href') || '');
      if (!match) return;
      const number = Number(match[1]);
      const title = (a.querySelector('.title')?.textContent || '').trim();
      if (Number.isInteger(number) && number > 0 && title) chapters.push({ number, title });
    });
    return chapters.sort((a, b) => a.number - b.number);
  };

  const setNav = (chapter, published) => {
    const numbers = new Set(published.map((item) => item.number));
    const prev = chapter.number > 1 && numbers.has(chapter.number - 1) ? chapter.number - 1 : null;
    const next = numbers.has(chapter.number + 1) ? chapter.number + 1 : (chapter.number === 155 ? 156 : null);
    for (const node of document.querySelectorAll('[data-light-prev],[data-light-prev-bottom]')) {
      node.hidden = !prev;
      if (prev) node.href = lightHref(prev);
    }
    for (const node of document.querySelectorAll('[data-light-next],[data-light-next-bottom]')) {
      node.hidden = !next;
      if (next) node.href = lightHref(next);
    }
  };

  const renderPublished = async (chapter) => {
    const path = `chapters/${String(chapter.number).padStart(3, '0')}.html`;
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Could not load Chapter ${chapter.number}.`);
    const sourceHtml = await response.text();
    const doc = new DOMParser().parseFromString(sourceHtml, 'text/html');
    const source = doc.querySelector('.prose');
    if (!source) throw new Error(`Chapter ${chapter.number} could not be read.`);
    source.querySelectorAll('figure,script,img').forEach((node) => node.remove());
    proseNode.innerHTML = source.innerHTML;
  };

  const renderModeSwitch = (chapter) => {
    if (!switchNode) return;
    switchNode.innerHTML = '';
    switchNode.hidden = false;
    const a = document.createElement('a');
    a.href = `chapters/${String(chapter.number).padStart(3, '0')}.html`;
    a.textContent = 'Illustrated Reader →';
    switchNode.appendChild(a);
  };

  const showChapter = async (published, chapter) => {
    tocNode.hidden = true;
    proseNode.hidden = false;
    bottomNode.hidden = false;
    numberNode.textContent = `TEXT READER · CHAPTER ${chapter.number}`;
    titleNode.textContent = chapter.title;
    document.title = `Chapter ${chapter.number}: ${chapter.title} — Peg-Leg Greg Text Reader`;
    jumpInput.value = chapter.number;
    setNav(chapter, published);
    renderModeSwitch(chapter);
    setStatus('Text-only reading · no chapter illustrations');
    await renderPublished(chapter);
    try { localStorage.setItem('plg:lastLightChapter', String(chapter.number)); } catch (_) {}
  };

  const showMissing = (number) => {
    tocNode.hidden = true;
    proseNode.hidden = true;
    bottomNode.hidden = true;
    if (switchNode) switchNode.hidden = true;
    numberNode.textContent = 'TEXT READER';
    titleNode.textContent = 'CHAPTER UNAVAILABLE';
    setStatus(`Chapter ${number} is not available in this reading mode yet. Use the Text Reader chapter list to continue.`);
  };

  jumpForm?.addEventListener('submit', (event) => {
    event.preventDefault();
    const number = Number(jumpInput.value);
    if (Number.isInteger(number) && number > 0) location.href = lightHref(number);
  });

  if (!Number.isInteger(requested) || requested < 1) {
    location.replace('light/index.html');
    return;
  }

  fetch('index.html', { cache: 'no-store' })
    .then((response) => {
      if (!response.ok) throw new Error('Could not load the chapter list.');
      return response.text();
    })
    .then(async (indexHtml) => {
      const published = parsePublishedIndex(indexHtml);
      const chapter = published.find((item) => item.number === requested);
      if (!chapter) return showMissing(requested);
      await showChapter(published, chapter);
    })
    .catch((error) => setStatus(error.message || 'Could not initialize the Text Reader.'));
})();
