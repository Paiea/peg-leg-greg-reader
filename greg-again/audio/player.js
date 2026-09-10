(async () => {
  const chapterList = document.getElementById('chapter-list');
  const availability = document.getElementById('availability-summary');
  const heroImage = document.querySelector('.listen-hero-image');
  const startListening = document.getElementById('hero-listen-start');

  function formatDuration(seconds) {
    const total = Math.round(Number(seconds) || 0);
    const minutes = Math.floor(total / 60);
    const remainder = String(total % 60).padStart(2, '0');
    return `${minutes}:${remainder}`;
  }

  function stableId(chapter) {
    const explicit = chapter.id || chapter.chapter_id || chapter.audio_id;
    if (typeof explicit === 'string' && /^ga-\d{3}$/.test(explicit)) return explicit;
    return `ga-${String(chapter.number).padStart(3, '0')}`;
  }

  function orderedPlayable(chapters) {
    return (Array.isArray(chapters) ? chapters : [])
      .slice()
      .sort((a, b) => Number(a.number) - Number(b.number));
  }

  function availabilityLabel(playable) {
    if (!playable.length) return 'No playable chapters yet · Written reference available';

    const numbers = playable
      .map((chapter) => Number(chapter.number))
      .filter((number) => Number.isInteger(number) && number > 0);
    const latest = numbers[numbers.length - 1];
    const available = new Set(numbers);
    const missing = [];

    for (let number = 1; number <= latest; number += 1) {
      if (!available.has(number)) missing.push(number);
    }

    const count = `${playable.length} playable chapter${playable.length === 1 ? '' : 's'}`;
    if (!missing.length) {
      return `${count} · through Chapter ${latest} · Written reference available`;
    }

    return `${count} · latest Chapter ${latest} · ${missing.length} audio gap${missing.length === 1 ? '' : 's'} · Written reference available`;
  }

  function writtenReferenceHref(chapter) {
    const writtenId = `r2-ch${String(chapter.number).padStart(3, '0')}`;
    return `../../r2/chapter.html?id=${encodeURIComponent(writtenId)}#read`;
  }

  async function loadOptionalPresentation() {
    try {
      const response = await fetch('presentation.json', { cache: 'no-store' });
      if (!response.ok) return { hero: null, chapters: {} };
      const payload = await response.json();
      return {
        hero: payload.hero || null,
        chapters: payload.chapters || {},
      };
    } catch (error) {
      console.warn('Presentation metadata unavailable.', error);
      return { hero: null, chapters: {} };
    }
  }

  function applyHeroPresentation(hero) {
    if (!heroImage || !hero || !hero.image_src) return;

    const fallbackSrc = heroImage.getAttribute('src');
    const fallbackAlt = heroImage.getAttribute('alt') || '';
    const probe = new Image();

    probe.onload = () => {
      heroImage.src = hero.image_src;
      heroImage.alt = hero.alt || fallbackAlt;
    };

    probe.onerror = () => {
      heroImage.src = fallbackSrc;
      heroImage.alt = fallbackAlt;
    };

    probe.src = hero.image_src;
  }

  function renderChapter(chapter, presentation = {}) {
    const id = stableId(chapter);
    const card = document.createElement('article');
    card.className = 'player-card chapter-card';
    card.id = id;
    card.dataset.chapterId = id;

    if (presentation.image_src) {
      const art = document.createElement('img');
      art.className = 'chapter-art';
      art.src = presentation.image_src;
      art.alt = presentation.alt || '';
      art.loading = 'lazy';
      art.addEventListener('error', () => art.remove(), { once: true });
      card.append(art);
    }

    const copy = document.createElement('div');
    copy.className = 'chapter-card-copy';

    const number = document.createElement('p');
    number.className = 'chapter-number';
    number.textContent = `Chapter ${chapter.number}`;

    const heading = document.createElement('h3');
    heading.className = 'chapter';
    const headingLink = document.createElement('a');
    headingLink.href = `#${id}`;
    headingLink.textContent = chapter.title;
    headingLink.setAttribute('aria-label', `Link to Chapter ${chapter.number}: ${chapter.title}`);
    heading.append(headingLink);

    copy.append(number, heading);

    if (presentation.quote) {
      const quote = document.createElement('blockquote');
      quote.className = 'chapter-quote';
      quote.textContent = presentation.quote;
      copy.append(quote);
    }

    const meta = document.createElement('p');
    meta.className = 'chapter-meta';
    meta.textContent = formatDuration(chapter.duration_seconds);

    const audio = document.createElement('audio');
    audio.controls = true;
    audio.preload = 'metadata';
    audio.src = chapter.audio_src;
    audio.setAttribute('aria-label', `Play Chapter ${chapter.number}: ${chapter.title}`);

    const links = document.createElement('div');
    links.className = 'chapter-card-links';

    const writtenReference = document.createElement('a');
    writtenReference.href = writtenReferenceHref(chapter);
    writtenReference.textContent = 'Written reference';
    writtenReference.setAttribute('aria-label', `Open written reference for Chapter ${chapter.number}: ${chapter.title}`);
    links.append(writtenReference);

    copy.append(meta, audio, links);
    card.append(copy);
    return card;
  }

  try {
    const [manifestResponse, presentation] = await Promise.all([
      fetch('manifest.json', { cache: 'no-store' }),
      loadOptionalPresentation(),
    ]);

    if (!manifestResponse.ok) throw new Error(`manifest ${manifestResponse.status}`);
    const manifest = await manifestResponse.json();
    const playable = orderedPlayable(manifest.chapters);

    applyHeroPresentation(presentation.hero);

    if (startListening && playable.length) {
      startListening.href = `#${stableId(playable[0])}`;
    }

    if (availability) {
      availability.textContent = availabilityLabel(playable);
    }

    chapterList.replaceChildren();
    playable.forEach((chapter) => {
      const id = stableId(chapter);
      chapterList.append(renderChapter(chapter, presentation.chapters[id] || {}));
    });

    if (window.location.hash) {
      const targetId = decodeURIComponent(window.location.hash.slice(1));
      const target = document.getElementById(targetId);
      if (target) requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
    }
  } catch (error) {
    chapterList.textContent = 'Audio chapters are temporarily unavailable.';
    if (availability) availability.textContent = 'Listening shelf temporarily unavailable.';
    console.error(error);
  }
})();
