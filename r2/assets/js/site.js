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

  async function loadChapterArt() {
    try {
      return await fetchJson('data/chapter-art.json');
    } catch {
      return {};
    }
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

  function formatDuration(seconds) {
    if (!Number.isFinite(seconds)) return '';
    const minutes = Math.floor(seconds / 60);
    const remaining = Math.round(seconds % 60).toString().padStart(2, '0');
    return `${minutes}:${remaining}`;
  }

  function imagesForChapter(chapter, chapterArt) {
    if (Array.isArray(chapter.images) && chapter.images.length) return chapter.images;
    return chapterArt[chapter.chapter_id] || [];
  }

  function makeChapterCard(chapter) {
    const article = document.createElement('article');
    article.className = 'chapter-card';

    const meta = document.createElement('p');
    meta.className = 'eyebrow';
    meta.textContent = `Chapter ${chapter.display_number}`;

    const title = document.createElement('h2');
    const link = document.createElement('a');
    link.href = chapterHref(chapter.chapter_id);
    link.textContent = chapter.title;
    title.appendChild(link);

    const teaser = document.createElement('p');
    teaser.textContent = chapter.teaser || '';

    const availability = document.createElement('div');
    availability.className = 'chapter-availability';

    if (chapter.audio?.status === 'published') {
      const listen = document.createElement('a');
      listen.className = 'chapter-action-listen';
      listen.href = chapterHref(chapter.chapter_id, '#listen');
      listen.textContent = `Listen${chapter.audio.duration_seconds ? ` · ${formatDuration(chapter.audio.duration_seconds)}` : ''}`;
      availability.appendChild(listen);
    }

    const read = document.createElement('a');
    read.className = 'chapter-action-read';
    read.href = chapterHref(chapter.chapter_id, '#read');
    read.textContent = chapter.written?.status === 'published' ? 'Read written rendition' : 'Open chapter';
    availability.appendChild(read);

    article.append(meta, title, teaser, availability);
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
      target.replaceChildren(...chapters.map(makeChapterCard));
    } catch (error) {
      target.innerHTML = '<p class="error-note">Chapters could not be loaded right now.</p>';
      console.error(error);
    }
  }

  async function bootGallery(targetId = 'gallery-grid', recentOnly = false) {
    const target = document.getElementById(targetId);
    if (!target) return;

    try {
      const [project, chapterArt] = await Promise.all([loadProject(), loadChapterArt()]);
      const chapters = await Promise.all(project.chapters.map(loadChapter));
      const entries = chapters.flatMap(chapter => imagesForChapter(chapter, chapterArt).map(image => ({ image, chapter })));
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

  window.R2Site = { loadProject, loadChapter, loadChapterArt, chapterHref };
})();
