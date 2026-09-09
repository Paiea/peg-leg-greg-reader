(() => {
  'use strict';

  function setText(id, value) {
    const node = document.getElementById(id);
    if (node) node.textContent = value;
  }

  function setHref(id, href) {
    const node = document.getElementById(id);
    if (node) node.href = href;
  }

  function chapterLabel(chapter) {
    return `Chapter ${chapter.display_number} · ${chapter.title}`;
  }

  async function bootHome() {
    if (!window.R2Site) return;

    try {
      const project = await window.R2Site.loadProject();
      const chapters = await Promise.all(project.chapters.map(window.R2Site.loadChapter));
      if (!chapters.length) return;

      const first = chapters[0];
      const current = chapters.find(chapter => chapter.chapter_id === project.current_chapter) || chapters.at(-1);
      const written = chapters.filter(chapter => chapter.written?.status === 'published');
      const audio = chapters.filter(chapter => chapter.audio?.status === 'published');
      const latestWritten = written.at(-1);
      const latestAudio = audio.at(-1);

      setHref('r2-start-listen', window.R2Site.chapterHref(first.chapter_id, '#listen'));
      setHref('r2-start-read', window.R2Site.chapterHref(first.chapter_id, '#read'));

      const availability = [];
      if (latestWritten) availability.push(`Read through Chapter ${latestWritten.display_number}`);
      if (latestAudio) availability.push(`Listen through Chapter ${latestAudio.display_number}`);
      setText('r2-home-availability', availability.join(' · ') || `${chapters.length} chapters in the run`);

      if (latestAudio) {
        setText('r2-listen-title', `${audio.length} audio ${audio.length === 1 ? 'chapter' : 'chapters'} available`);
        setText('r2-listen-detail', `Currently through ${chapterLabel(latestAudio)}.`);
        setHref('r2-listen-link', window.R2Site.chapterHref(first.chapter_id, '#listen'));
      } else {
        setText('r2-listen-title', 'Audio is being built');
        setText('r2-listen-detail', 'The written run is available while audio catches up.');
        setText('r2-listen-link', 'Browse chapters');
        setHref('r2-listen-link', 'chapters/');
      }

      if (latestWritten) {
        setText('r2-read-title', `${written.length} written ${written.length === 1 ? 'chapter' : 'chapters'} available`);
        setText('r2-read-detail', `Currently through ${chapterLabel(latestWritten)}.`);
        setHref('r2-read-link', window.R2Site.chapterHref(first.chapter_id, '#read'));
      }

      setText('r2-current-number', `Chapter ${current.display_number}`);
      setText('r2-current-title', current.title);
      setText('r2-current-teaser', current.teaser || 'The newest chapter in the active second run.');
      setHref('r2-current-read', window.R2Site.chapterHref(current.chapter_id, '#read'));

      const currentListen = document.getElementById('r2-current-listen');
      if (currentListen && current.audio?.status === 'published') {
        currentListen.hidden = false;
        currentListen.href = window.R2Site.chapterHref(current.chapter_id, '#listen');
      }
    } catch (error) {
      setText('r2-home-availability', 'Start with Chapter 1.');
      console.error(error);
    }
  }

  bootHome();
})();
