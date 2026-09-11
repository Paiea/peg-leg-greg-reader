(async () => {
  'use strict';

  const chapterList = document.getElementById('chapter-list');
  const continueListening = document.getElementById('continue-listening');
  const chapterSearch = document.getElementById('chapter-search');
  const lengthFilter = document.getElementById('length-filter');
  const chapterCount = document.getElementById('chapter-count');
  const progressKey = 'r2-audio-library-progress:v1';

  let chapters = [];
  let activeAudio = null;
  let saveTimer = null;

  function formatDuration(seconds) {
    const total = Math.max(0, Math.round(Number(seconds) || 0));
    const minutes = Math.floor(total / 60);
    const remainder = String(total % 60).padStart(2, '0');
    return `${minutes}:${remainder}`;
  }

  function chapterId(number) {
    return `r2-ch${String(number).padStart(3, '0')}`;
  }

  function readProgress() {
    try {
      const stored = localStorage.getItem(progressKey);
      if (!stored) return null;
      const parsed = JSON.parse(stored);
      const number = Number(parsed.number);
      const currentTime = Number(parsed.currentTime);
      if (!Number.isFinite(number) || !Number.isFinite(currentTime) || currentTime < 0) return null;
      return { number, currentTime };
    } catch {
      return null;
    }
  }

  function writeProgress(number, currentTime) {
    try {
      localStorage.setItem(progressKey, JSON.stringify({
        number: Number(number),
        currentTime: Math.max(0, Number(currentTime) || 0),
      }));
    } catch {
      // Browsers may block storage. Playback still works without persistence.
    }
  }

  function saveProgressSoon(chapter, audio) {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => writeProgress(chapter.number, audio.currentTime), 180);
  }

  function stopOtherAudio(nextAudio) {
    if (activeAudio && activeAudio !== nextAudio) activeAudio.pause();
    activeAudio = nextAudio;
  }

  function writtenHref(chapter) {
    return `../../r2/chapter.html?id=${chapterId(chapter.number)}`;
  }

  function renderContinueListening() {
    const progress = readProgress();
    const chapter = progress && chapters.find((item) => Number(item.number) === progress.number);

    if (!chapter) {
      const first = chapters[0];
      if (!first) {
        continueListening.hidden = true;
        return;
      }
      continueListening.hidden = false;
      continueListening.innerHTML = `
        <div class="continue-copy">
          <p class="eyebrow">Start the story</p>
          <h2>Chapter ${String(first.number).padStart(3, '0')} · ${escapeHtml(first.title)}</h2>
          <p>No homework. Just headphones.</p>
        </div>
        <a class="continue-action" href="#chapter-${first.number}">Start listening ↓</a>
      `;
      return;
    }

    continueListening.hidden = false;
    continueListening.innerHTML = `
      <div class="continue-copy">
        <p class="eyebrow">Continue listening</p>
        <h2>Chapter ${String(chapter.number).padStart(3, '0')} · ${escapeHtml(chapter.title)}</h2>
        <p>${formatDuration(progress.currentTime)} into ${formatDuration(chapter.duration_seconds)}</p>
      </div>
      <button class="continue-action" type="button" data-resume="${chapter.number}">Resume ▶</button>
    `;

    const button = continueListening.querySelector('[data-resume]');
    button?.addEventListener('click', () => {
      const audio = document.querySelector(`[data-audio-number="${chapter.number}"]`);
      if (!audio) return;
      audio.currentTime = Math.min(progress.currentTime, Math.max(0, (audio.duration || chapter.duration_seconds || 0) - 1));
      stopOtherAudio(audio);
      audio.play().catch(() => {});
      document.getElementById(`chapter-${chapter.number}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  }

  function escapeHtml(value) {
    return String(value ?? '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function renderChapter(chapter) {
    const card = document.createElement('article');
    card.className = 'player-card chapter-card';
    card.id = `chapter-${chapter.number}`;
    card.dataset.search = `${chapter.number} ${chapter.title}`.toLowerCase();
    card.dataset.duration = String(Number(chapter.duration_seconds) || 0);

    const visual = document.createElement('div');
    visual.className = 'chapter-visual';
    if (chapter.image_src) {
      const image = document.createElement('img');
      image.src = chapter.image_src;
      image.alt = '';
      image.loading = 'lazy';
      image.addEventListener('error', () => image.remove());
      visual.append(image);
    }
    const visualNumber = document.createElement('span');
    visualNumber.className = 'chapter-visual-number';
    visualNumber.textContent = String(chapter.number).padStart(3, '0');
    visual.append(visualNumber);

    const body = document.createElement('div');
    body.className = 'chapter-card-body';

    const kicker = document.createElement('p');
    kicker.className = 'chapter-kicker';
    kicker.textContent = `Chapter ${String(chapter.number).padStart(3, '0')}`;

    const heading = document.createElement('h3');
    heading.className = 'chapter';
    heading.textContent = chapter.title;

    const meta = document.createElement('p');
    meta.className = 'chapter-meta';
    meta.textContent = formatDuration(chapter.duration_seconds);

    const audio = document.createElement('audio');
    audio.controls = true;
    audio.preload = 'metadata';
    audio.src = chapter.audio_src;
    audio.dataset.audioNumber = String(chapter.number);
    audio.setAttribute('aria-label', `Play Chapter ${chapter.number}: ${chapter.title}`);
    audio.addEventListener('play', () => stopOtherAudio(audio));
    audio.addEventListener('timeupdate', () => saveProgressSoon(chapter, audio));
    audio.addEventListener('ended', () => writeProgress(chapter.number, 0));

    const progress = readProgress();
    if (progress?.number === Number(chapter.number) && progress.currentTime > 3) {
      audio.addEventListener('loadedmetadata', () => {
        if (audio.duration && progress.currentTime < audio.duration - 1) audio.currentTime = progress.currentTime;
      }, { once: true });
    }

    const actions = document.createElement('div');
    actions.className = 'chapter-actions';
    const written = document.createElement('a');
    written.href = writtenHref(chapter);
    written.className = 'written-link';
    written.textContent = 'Written rendition →';
    actions.append(written);

    body.append(kicker, heading, meta, audio, actions);
    card.append(visual, body);
    return card;
  }

  function durationMatches(chapter, filter) {
    const seconds = Number(chapter.duration_seconds) || 0;
    if (filter === 'short') return seconds < 12 * 60;
    if (filter === 'medium') return seconds >= 12 * 60 && seconds <= 16 * 60;
    if (filter === 'long') return seconds > 16 * 60;
    return true;
  }

  function filteredChapters() {
    const query = (chapterSearch?.value || '').trim().toLowerCase();
    const length = lengthFilter?.value || 'all';
    return chapters.filter((chapter) => {
      const haystack = `${chapter.number} ${chapter.title}`.toLowerCase();
      return (!query || haystack.includes(query)) && durationMatches(chapter, length);
    });
  }

  function renderShelf() {
    const visible = filteredChapters();
    chapterList.replaceChildren();
    visible.forEach((chapter) => chapterList.append(renderChapter(chapter)));
    if (!visible.length) {
      const empty = document.createElement('p');
      empty.className = 'empty-state';
      empty.textContent = 'No chapters match that search.';
      chapterList.append(empty);
    }
    chapterCount.textContent = `${visible.length} of ${chapters.length} audio chapters`;
  }

  try {
    const response = await fetch('manifest.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`manifest ${response.status}`);
    const manifest = await response.json();
    chapters = Array.isArray(manifest.chapters)
      ? manifest.chapters.filter((chapter) => chapter && chapter.audio_src)
      : [];

    renderContinueListening();
    renderShelf();
    chapterSearch?.addEventListener('input', renderShelf);
    lengthFilter?.addEventListener('change', renderShelf);
  } catch (error) {
    continueListening.hidden = true;
    chapterList.textContent = 'Audio chapters are temporarily unavailable.';
    chapterCount.textContent = '';
    console.error(error);
  }
})();
