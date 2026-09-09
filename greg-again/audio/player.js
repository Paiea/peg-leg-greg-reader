(async () => {
  const chapterList = document.getElementById('chapter-list');

  function formatDuration(seconds) {
    const total = Math.round(Number(seconds) || 0);
    const minutes = Math.floor(total / 60);
    const remainder = String(total % 60).padStart(2, '0');
    return `${minutes}:${remainder}`;
  }

  function renderChapter(chapter) {
    const card = document.createElement('article');
    card.className = 'player-card chapter-card';

    const heading = document.createElement('h2');
    heading.className = 'chapter';
    heading.textContent = `Chapter ${chapter.number} · ${chapter.title}`;

    const meta = document.createElement('p');
    meta.className = 'chapter-meta';
    meta.textContent = formatDuration(chapter.duration_seconds);

    const audio = document.createElement('audio');
    audio.controls = true;
    audio.preload = 'metadata';
    audio.src = chapter.audio_src;
    audio.setAttribute('aria-label', `Play Chapter ${chapter.number}: ${chapter.title}`);

    card.append(heading, meta, audio);
    return card;
  }

  try {
    const response = await fetch('manifest.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`manifest ${response.status}`);
    const manifest = await response.json();

    chapterList.replaceChildren();
    manifest.chapters.forEach((chapter) => chapterList.append(renderChapter(chapter)));
  } catch (error) {
    chapterList.textContent = 'Audio chapters are temporarily unavailable.';
    console.error(error);
  }
})();
