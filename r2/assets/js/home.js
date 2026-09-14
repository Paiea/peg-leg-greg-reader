(() => {
  'use strict';

  async function fetchJson(path) {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`Could not load ${path} (${response.status})`);
    return response.json();
  }

  function chapterFile(id) {
    return id.replace(/^r2-/, '');
  }

  function chapterHref(id, hash = '') {
    return `chapter.html?id=${encodeURIComponent(id)}${hash}`;
  }

  function formatDuration(seconds) {
    if (!Number.isFinite(Number(seconds))) return '';
    const total = Math.round(Number(seconds));
    const minutes = Math.floor(total / 60);
    const remaining = String(total % 60).padStart(2, '0');
    return `${minutes}:${remaining}`;
  }

  function publishedWritten(chapter) {
    return chapter?.written?.status === 'published';
  }

  function publishedAudio(chapter) {
    return chapter?.audio?.status === 'published';
  }

  function renderCurrent(target, chapter) {
    const wrap = document.createElement('div');

    const eyebrow = document.createElement('p');
    eyebrow.className = 'eyebrow';
    eyebrow.textContent = `Chapter ${chapter.display_number}`;

    const title = document.createElement('h3');
    title.className = 'current-card-title';
    const link = document.createElement('a');
    link.href = chapterHref(chapter.chapter_id);
    link.textContent = chapter.title;
    title.appendChild(link);

    const meta = document.createElement('p');
    meta.className = 'current-card-meta';
    meta.textContent = chapter.audio?.status === 'published'
      ? `Audio available · ${formatDuration(chapter.audio.duration_seconds)}`
      : 'Current written frontier';

    const copy = document.createElement('p');
    copy.className = 'current-card-copy';
    copy.textContent = chapter.teaser || 'The active frontier of R2.';

    const actions = document.createElement('div');
    actions.className = 'current-card-actions';
    if (publishedAudio(chapter)) {
      const listen = document.createElement('a');
      listen.className = 'button button-primary';
      listen.href = chapterHref(chapter.chapter_id, '#listen');
      listen.textContent = 'Listen here';
      actions.appendChild(listen);
    }
    if (publishedWritten(chapter)) {
      const read = document.createElement('a');
      read.className = 'text-link current-read-link';
      read.href = chapterHref(chapter.chapter_id, '#read');
      read.textContent = 'Written rendition →';
      actions.appendChild(read);
    }

    wrap.append(eyebrow, title, meta, copy, actions);
    target.replaceChildren(wrap);
  }

  async function boot() {
    const summary = document.getElementById('availability-summary');
    const currentTarget = document.getElementById('current-chapter');

    try {
      const project = await fetchJson('data/project.json');
      const chapters = await Promise.all((project.chapters || []).map(id => fetchJson(`data/chapters/${chapterFile(id)}.json`)));
      const ordered = chapters.slice().sort((a, b) => (a.display_number || 0) - (b.display_number || 0));

      const latestAudio = ordered.filter(publishedAudio).slice(-1)[0] || null;
      const latestWritten = ordered.filter(publishedWritten).slice(-1)[0] || ordered.slice(-1)[0] || null;
      const currentId = project.current_chapter || latestWritten?.chapter_id || ordered.slice(-1)[0]?.chapter_id;
      const current = ordered.find(ch => ch.chapter_id === currentId) || ordered.slice(-1)[0];

      const readLabel = latestWritten ? `Written through Chapter ${latestWritten.display_number}` : 'Written frontier unavailable';
      const listenLabel = latestAudio ? `Listen through Chapter ${latestAudio.display_number}` : 'Audio coming soon';
      if (summary) summary.textContent = `${listenLabel} · ${readLabel}`;

      if (current && currentTarget) renderCurrent(currentTarget, current);
    } catch (error) {
      console.error(error);
      if (summary) summary.textContent = 'Chapter availability could not be loaded right now.';
      if (currentTarget) currentTarget.innerHTML = '<p class="error-note">Current chapter could not be loaded right now.</p>';
    }
  }

  boot();
})();
