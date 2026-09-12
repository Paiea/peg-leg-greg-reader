(() => {
  'use strict';

  const params = new URLSearchParams(window.location.search);
  const chapterId = params.get('id') || 'r2-ch001';

  function chapterFile(id) {
    return id.replace(/^r2-/, '');
  }

  async function loadChapter(id) {
    const response = await fetch(`data/chapters/${chapterFile(id)}.json`);
    if (!response.ok) throw new Error(`Could not load chapter ${id}`);
    return response.json();
  }

  async function loadChapterArt() {
    try {
      const response = await fetch('data/chapter-art.json', { cache: 'no-store' });
      if (!response.ok) return {};
      return response.json();
    } catch {
      return {};
    }
  }

  function setText(id, value) {
    const node = document.getElementById(id);
    if (node) node.textContent = value || '';
  }

  function renderAudio(chapter) {
    const slot = document.getElementById('audio-slot');
    slot.replaceChildren();
    if (chapter.audio?.status !== 'published' || !chapter.audio.path) {
      const note = document.createElement('p');
      note.className = 'empty-note';
      note.textContent = 'Audio version coming soon.';
      slot.appendChild(note);
      return;
    }
    const audio = document.createElement('audio');
    audio.controls = true;
    audio.preload = 'metadata';
    audio.src = chapter.audio.path;
    audio.setAttribute('aria-label', `${chapter.title} audio rendition`);
    slot.appendChild(audio);
  }

  function stripInternalPrelude(markdown) {
    const normalized = markdown.replace(/\r\n/g, '\n');
    const marker = '\n---\n';
    const index = normalized.indexOf(marker);
    return (index >= 0 ? normalized.slice(index + marker.length) : normalized).trim();
  }

  function appendParagraphs(target, text) {
    const blocks = text.split(/\n\s*\n/).map(block => block.trim()).filter(Boolean);
    for (const block of blocks) {
      const node = document.createElement(block.startsWith('## ') ? 'h2' : 'p');
      node.textContent = block.startsWith('## ') ? block.slice(3).trim() : block.replace(/\n/g, ' ');
      target.appendChild(node);
    }
  }

  async function renderWritten(chapter) {
    const slot = document.getElementById('written-slot');
    slot.replaceChildren();
    if (chapter.written?.status !== 'published' || !chapter.written.path) {
      const note = document.createElement('p');
      note.className = 'empty-note';
      note.textContent = 'Written rendition coming soon.';
      slot.appendChild(note);
      return;
    }
    try {
      const response = await fetch(chapter.written.path);
      if (!response.ok) throw new Error('Written rendition could not be loaded');
      appendParagraphs(slot, stripInternalPrelude(await response.text()));
    } catch (error) {
      const note = document.createElement('p');
      note.className = 'error-note';
      note.textContent = 'Written rendition could not be loaded right now.';
      slot.appendChild(note);
      console.error(error);
    }
  }

  function openWrittenFromHash() {
    if (location.hash === '#read') {
      const details = document.getElementById('read');
      if (details) details.open = true;
    }
  }

  function makeFigure(image, chapter, className = '') {
    const figure = document.createElement('figure');
    figure.className = `chapter-figure ${className}`.trim();
    const img = document.createElement('img');
    img.src = image.path;
    img.alt = image.alt || `${chapter.title} illustration`;
    img.loading = className.includes('anchor') ? 'eager' : 'lazy';
    figure.appendChild(img);
    if (image.caption) {
      const caption = document.createElement('figcaption');
      caption.textContent = image.caption;
      figure.appendChild(caption);
    }
    return figure;
  }

  function imagesForChapter(chapter, chapterArt) {
    if (Array.isArray(chapter.images) && chapter.images.length) return chapter.images;
    return chapterArt[chapter.chapter_id] || [];
  }

  function renderImages(chapter, chapterArt) {
    const images = imagesForChapter(chapter, chapterArt);
    const anchorSlot = document.getElementById('anchor-image-slot');
    const section = document.getElementById('chapter-art-section');
    const supportGrid = document.getElementById('support-art-grid');
    anchorSlot.replaceChildren();
    supportGrid.replaceChildren();
    section.hidden = true;
    const anchor = images.find(image => image.role === 'anchor');
    if (anchor) anchorSlot.appendChild(makeFigure(anchor, chapter, 'anchor'));
    const supporting = images.filter(image => image !== anchor);
    if (supporting.length) {
      supportGrid.append(...supporting.map(image => makeFigure(image, chapter)));
      section.hidden = false;
    }
  }

  function renderNavigation(chapter) {
    const prev = document.getElementById('prev-chapter');
    const next = document.getElementById('next-chapter');
    if (chapter.navigation?.previous) {
      prev.href = `chapter.html?id=${encodeURIComponent(chapter.navigation.previous)}`;
      prev.hidden = false;
    }
    if (chapter.navigation?.next) {
      next.href = `chapter.html?id=${encodeURIComponent(chapter.navigation.next)}`;
      next.hidden = false;
    }
  }

  async function boot() {
    try {
      const [chapter, chapterArt] = await Promise.all([
        loadChapter(chapterId),
        loadChapterArt(),
      ]);
      document.title = `Chapter ${chapter.display_number}: ${chapter.title} — R2`;
      setText('chapter-kicker', `R2 · Chapter ${chapter.display_number}`);
      setText('chapter-title', chapter.title);
      setText('chapter-teaser', chapter.teaser);
      renderAudio(chapter);
      await renderWritten(chapter);
      renderImages(chapter, chapterArt);
      renderNavigation(chapter);
      openWrittenFromHash();
    } catch (error) {
      setText('chapter-title', 'Chapter unavailable');
      setText('chapter-teaser', 'This chapter could not be loaded right now.');
      document.getElementById('audio-slot').replaceChildren();
      document.getElementById('written-slot').replaceChildren();
      console.error(error);
    }
  }

  window.addEventListener('hashchange', openWrittenFromHash);
  boot();
})();
