(() => {
  'use strict';

  const page = document.body.dataset.page || 'home';
  const rootPrefix = page === 'home' ? '' : '../';

  async function fetchJson(path) {
    const response = await fetch(`${rootPrefix}${path}`);
    if (!response.ok) {
      throw new Error(`Could not load ${path} (${response.status})`);
    }
    return response.json();
  }

  async function loadProject() {
    return fetchJson('data/project.json');
  }

  function chapterFile(id) {
    return id.replace(/^r2-/, '');
  }

  async function loadChapter(id) {
    return fetchJson(`data/chapters/${chapterFile(id)}.json`);
  }

  function chapterHref(id, hash = '') {
    return `${rootPrefix}chapter.html?id=${encodeURIComponent(id)}${hash}`;
  }

  function audioShelfHref(chapter) {
    const audioId = `ga-${String(chapter.display_number).padStart(3, '0')}`;
    return `${rootPrefix}../greg-again/audio/#${audioId}`;
  }

  function formatDuration(seconds) {
    if (!Number.isFinite(Number(seconds))) return '';
    const total = Math.round(Number(seconds));
    const minutes = Math.floor(total / 60);
    const remaining = String(total % 60).padStart(2, '0');
    return `${minutes}:${remaining}`;
  }

  function makeChapterRow(chapter) {
    const article = document.createElement('article');
    article.className = 'chapter-row';

    const main = document.createElement('div');
    main.className = 'chapter-row-main';

    const number = document.createElement('p');
    number.className = 'chapter-number';
    number.textContent = String(chapter.display_number).padStart(2, '0');

    const body = document.createElement('div');
    const title = document.createElement('h3');
    const titleLink = document.createElement('a');
    titleLink.href = chapterHref(chapter.chapter_id);
    titleLink.textContent = chapter.title;
    title.appendChild(titleLink);

    const meta = document.createElement('p');
    meta.className = 'chapter-meta';
    const bits = [];
    if (chapter.written?.status === 'published') bits.push('Written available');
    if (chapter.audio?.status === 'published') bits.push(`Audio ${formatDuration(chapter.audio.duration_seconds)}`);
    if (!bits.length) bits.push('Open chapter');
    meta.textContent = bits.join(' · ');
    body.append(title, meta);

    main.append(number, body);

    const actions = document.createElement('div');
    actions.className = 'chapter-row-actions';
    if (chapter.audio?.status === 'published') {
      const listen = document.createElement('a');
      listen.className = 'text-link';
      listen.href = audioShelfHref(chapter);
      listen.textContent = 'Listen';
      actions.appendChild(listen);
    }

    const read = document.createElement('a');
    read.className = 'text-link';
    read.href = chapterHref(chapter.chapter_id, '#read');
    read.textContent = chapter.written?.status === 'published' ? 'Read' : 'Open';
    actions.appendChild(read);

    article.append(main, actions);
    return article;
  }

  function makeGalleryFigure(image, chapter) {
    const figure = document.createElement('figure');
    figure.className = 'gallery-card';

    const link = document.createElement('a');
    link.href = chapterHref(chapter.chapter_id);

    const img = document.createElement('img');
    img.src = `${rootPrefix}${image.path}`;
    img.alt = image.alt || `${chapter.title} illustration`;
    img.loading = 'lazy';
    link.appendChild(img);

    const caption = document.createElement('figcaption');
    caption.textContent = image.caption || `Chapter ${chapter.display_number} · ${chapter.title}`;

    figure.append(link, caption);
    return figure;
  }

  async function bootChapterList() {
    const target = document.getElementById('chapter-list');
    if (!target) return;

    try {
      const project = await loadProject();
      const chapters = await Promise.all(project.chapters.map(loadChapter));
      target.replaceChildren(...chapters.map(makeChapterRow));
    } catch (error) {
      target.innerHTML = '<p class="error-note">Chapters could not be loaded right now.</p>';
      console.error(error);
    }
  }

  async function bootGallery(targetId = 'gallery-grid', recentOnly = false) {
    const target = document.getElementById(targetId);
    if (!target) return;

    try {
      const project = await loadProject();
      const chapters = await Promise.all(project.chapters.map(loadChapter));
      const entries = chapters.flatMap(chapter => (chapter.images || []).map(image => ({ image, chapter })));
      const selected = recentOnly ? entries.slice(-6).reverse() : entries;

      if (!selected.length) return;
      target.replaceChildren(...selected.map(({ image, chapter }) => makeGalleryFigure(image, chapter)));
    } catch (error) {
      target.innerHTML = '<p class="error-note">Art could not be loaded right now.</p>';
      console.error(error);
    }
  }

  if (page === 'chapters') bootChapterList();
  if (page === 'gallery') bootGallery();
  if (page === 'home') bootGallery('recent-art-grid', true);

  window.R2Site = { loadProject, loadChapter, chapterHref, audioShelfHref };
})();
