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
    if (publishedWritten(chapter)) bits.push('Written available');
    if (publishedAudio(chapter)) bits.push(`Audio ${formatDuration(chapter.audio.duration_seconds)}`);
    if (!bits.length) bits.push('Open chapter');
    meta.textContent = bits.join(' · ');
    body.append(title, meta);

    main.append(number, body);

    const actions = document.createElement('div');
    actions.className = 'chapter-row-actions';
    if (publishedAudio(chapter)) {
      const listen = document.createElement('a');
      listen.className = 'text-link';
      listen.href = chapterHref(chapter.chapter_id, '#listen');
      listen.textContent = 'Listen';
      actions.appendChild(listen);
    }
    const read = document.createElement('a');
    read.className = 'text-link';
    read.href = chapterHref(chapter.chapter_id, '#read');
    read.textContent = publishedWritten(chapter) ? 'Read' : 'Open';
    actions.appendChild(read);

    article.append(main, actions);
    return article;
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
    const read = document.createElement('a');
    read.className = 'button';
    read.href = chapterHref(chapter.chapter_id, '#read');
    read.textContent = publishedWritten(chapter) ? 'Read here' : 'Open chapter';
    actions.appendChild(read);

    wrap.append(eyebrow, title, meta, copy, actions);
    target.replaceChildren(wrap);
  }

  async function boot() {
    const summary = document.getElementById('availability-summary');
    const currentTarget = document.getElementById('current-chapter');
    const listTarget = document.getElementById('chapter-list');
    const readLink = document.getElementById('hero-read');

    try {
      const project = await fetchJson('data/project.json');
      const chapters = await Promise.all((project.chapters || []).map(id => fetchJson(`data/chapters/${chapterFile(id)}.json`)));
      const ordered = chapters.slice().sort((a, b) => (a.display_number || 0) - (b.display_number || 0));

      const firstWritten = ordered.find(ch => publishedWritten(ch) || ch.written?.status !== 'unavailable') || ordered[0];
      const latestAudio = ordered.filter(publishedAudio).slice(-1)[0] || null;
      const latestWritten = ordered.filter(publishedWritten).slice(-1)[0] || ordered.slice(-1)[0] || null;
      const currentId = project.current_chapter || latestWritten?.chapter_id || ordered.slice(-1)[0]?.chapter_id;
      const current = ordered.find(ch => ch.chapter_id === currentId) || ordered.slice(-1)[0];

      if (firstWritten && readLink) readLink.href = chapterHref(firstWritten.chapter_id, '#read');

      const readLabel = latestWritten ? `Read through Chapter ${latestWritten.display_number}` : 'Read frontier unavailable';
      const listenLabel = latestAudio ? `Listen through Chapter ${latestAudio.display_number}` : 'Audio coming soon';
      summary.textContent = `${listenLabel} · ${readLabel}`;

      if (current) renderCurrent(currentTarget, current);

      const frag = document.createDocumentFragment();
      ordered.forEach(chapter => frag.appendChild(makeChapterRow(chapter)));
      listTarget.replaceChildren(frag);
    } catch (error) {
      console.error(error);
      if (summary) summary.textContent = 'Chapter availability could not be loaded right now.';
      if (currentTarget) currentTarget.innerHTML = '<p class="error-note">Current chapter could not be loaded right now.</p>';
      if (listTarget) listTarget.innerHTML = '<p class="error-note">Chapter list could not be loaded right now.</p>';
    }
  }

  boot();
})();
