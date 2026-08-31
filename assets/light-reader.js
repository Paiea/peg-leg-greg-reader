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
  const manuscriptPath = 'state/manuscript/Peg_Leg_Greg_Running_Manuscript.md';
  const recoveredPath = 'state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md';

  const params = new URLSearchParams(location.search);
  const requested = Number.parseInt(params.get('chapter') || '', 10);

  const setStatus = (text) => { if (statusNode) statusNode.textContent = text; };
  const lightHref = (chapter) => `light.html?chapter=${chapter}`;

  const parsePublishedIndex = (html) => {
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const chapters = [];
    doc.querySelectorAll('#chapters a[href*="chapters/"]').forEach((a) => {
      const match = /chapters\/(\d+)\.html/.exec(a.getAttribute('href') || '');
      if (!match) return;
      const number = Number.parseInt(match[1], 10);
      const title = (a.querySelector('.title')?.textContent || '').trim();
      if (number && title) chapters.push({ number, title, source: 'published' });
    });
    return chapters;
  };

  const parseManuscript = (markdown, source = 'manuscript') => {
    const text = markdown.replace(/\r\n?/g, '\n');
    const heading = /^# CHAPTER (\d+)\s*$/gm;
    const found = [];
    let match;
    while ((match = heading.exec(text))) {
      const number = Number.parseInt(match[1], 10);
      const start = match.index + match[0].length;
      const next = /^# CHAPTER \d+\s*$/gm;
      next.lastIndex = start;
      const nextMatch = next.exec(text);
      const end = nextMatch ? nextMatch.index : text.length;
      const chunk = text.slice(start, end).replace(/^-{20,}\s*$/gm, '').trim();
      const titleMatch = /^##\s+(.+)\s*$/m.exec(chunk);
      if (!titleMatch) continue;
      const title = titleMatch[1].trim();
      const body = chunk.slice(titleMatch.index + titleMatch[0].length).trim();
      found.push({ number, title, body, source });
    }
    return found;
  };

  const addTocLabel = (text) => {
    const label = document.createElement('div');
    label.className = 'light-toc-label';
    label.textContent = text;
    tocNode.appendChild(label);
  };

  const addTocChapter = (chapter) => {
    const a = document.createElement('a');
    a.href = lightHref(chapter.number);
    const num = document.createElement('span');
    num.className = 'num';
    num.textContent = String(chapter.number).padStart(2, '0');
    const title = document.createElement('span');
    title.className = 'title';
    title.textContent = chapter.title;
    a.append(num, title);
    tocNode.appendChild(a);
  };

  const renderToc = (available) => {
    tocNode.innerHTML = '';
    const published = available.filter((chapter) => chapter.source === 'published').sort((a, b) => a.number - b.number);
    const recovered = available.filter((chapter) => chapter.source === 'recovered').sort((a, b) => a.number - b.number);
    const forward = available.filter((chapter) => chapter.source === 'manuscript').sort((a, b) => a.number - b.number);

    if (forward.length) {
      addTocLabel('CURRENT MANUSCRIPT · NEWEST FIRST');
      [...forward].reverse().forEach(addTocChapter);
    }

    if (recovered.length) {
      addTocLabel('RECOVERED EXACT PROSE · CHAPTERS 156–219');
      recovered.forEach(addTocChapter);
    }

    if (published.length) {
      addTocLabel('ILLUSTRATED-EDITION PROSE · TEXT ONLY');
      published.forEach(addTocChapter);
    }
  };

  const setNav = (available, current) => {
    const byNumber = new Map(available.map((chapter) => [chapter.number, chapter]));
    const prev = byNumber.get(current - 1) || null;
    const next = byNumber.get(current + 1) || null;
    for (const node of document.querySelectorAll('[data-light-prev],[data-light-prev-bottom]')) {
      node.hidden = !prev;
      if (prev) node.href = lightHref(prev.number);
    }
    for (const node of document.querySelectorAll('[data-light-next],[data-light-next-bottom]')) {
      node.hidden = !next;
      if (next) node.href = lightHref(next.number);
    }
  };

  const renderPublished = async (chapter) => {
    const path = `chapters/${String(chapter.number).padStart(3, '0')}.html`;
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Could not load Chapter ${chapter.number}.`);
    const html = await response.text();
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const source = doc.querySelector('.prose');
    if (!source) throw new Error(`Chapter ${chapter.number} prose could not be read.`);
    source.querySelectorAll('figure,script').forEach((node) => node.remove());
    proseNode.innerHTML = source.innerHTML;
  };

  const renderManuscript = (chapter) => {
    proseNode.innerHTML = '';
    const blocks = chapter.body.split(/\n\s*\n+/).map((block) => block.trim()).filter(Boolean);
    for (const block of blocks) {
      if (/^-{20,}$/.test(block)) continue;
      const p = document.createElement('p');
      p.textContent = block;
      proseNode.appendChild(p);
    }
  };

  const renderModeSwitch = (chapter) => {
    if (!switchNode) return;
    switchNode.innerHTML = '';
    switchNode.hidden = false;
    if (chapter.source === 'published') {
      const a = document.createElement('a');
      a.href = `chapters/${String(chapter.number).padStart(3, '0')}.html`;
      a.textContent = 'View this chapter in the illustrated reader →';
      switchNode.appendChild(a);
    } else {
      const a = document.createElement('a');
      a.href = 'latest.html';
      a.textContent = chapter.source === 'recovered' ? 'View latest manuscript index →' : 'View latest manuscript index →';
      switchNode.appendChild(a);
    }
  };

  const renderCurrentShortcut = (forward) => {
    if (!switchNode || !forward.length) return;
    const latest = forward[forward.length - 1];
    switchNode.innerHTML = '';
    switchNode.hidden = false;
    const a = document.createElement('a');
    a.href = lightHref(latest.number);
    a.textContent = `Read current manuscript: Chapter ${latest.number} — ${latest.title} →`;
    switchNode.appendChild(a);
  };

  const showChapter = async (available, chapter) => {
    tocNode.hidden = true;
    proseNode.hidden = false;
    bottomNode.hidden = false;
    numberNode.textContent = `CHAPTER ${chapter.number} · LIGHT`;
    titleNode.textContent = chapter.title;
    document.title = `Chapter ${chapter.number}: ${chapter.title} — Peg-Leg Greg Light Reader`;
    jumpInput.value = chapter.number;
    setNav(available, chapter.number);
    renderModeSwitch(chapter);
    if (chapter.source === 'published') {
      setStatus('Text-only rendering from the exact published chapter. Illustrations are intentionally omitted.');
      await renderPublished(chapter);
    } else if (chapter.source === 'recovered') {
      setStatus('Text-only rendering from the recovered exact manuscript prose now synchronized into GitHub.');
      renderManuscript(chapter);
    } else {
      setStatus('Text-only rendering directly from the current permanent GitHub manuscript.');
      renderManuscript(chapter);
    }
  };

  const showMissing = (available, number) => {
    tocNode.hidden = false;
    proseNode.hidden = true;
    bottomNode.hidden = true;
    if (switchNode) switchNode.hidden = true;
    numberNode.textContent = 'LIGHT READER';
    titleNode.textContent = 'CHAPTER NOT YET MATERIALIZED';
    setStatus(`Chapter ${number} is not currently materialized as exact prose in GitHub. The table below shows all currently available exact-text chapters.`);
    renderToc(available);
  };

  jumpForm?.addEventListener('submit', (event) => {
    event.preventDefault();
    const number = Number.parseInt(jumpInput.value, 10);
    if (number > 0) location.href = lightHref(number);
  });

  Promise.all([
    fetch('index.html', { cache: 'no-store' }).then((r) => { if (!r.ok) throw new Error('Could not load published chapter index.'); return r.text(); }),
    fetch(recoveredPath, { cache: 'no-store' }).then((r) => { if (!r.ok) throw new Error('Could not load recovered Chapters 156–219.'); return r.text(); }),
    fetch(manuscriptPath, { cache: 'no-store' }).then((r) => { if (!r.ok) throw new Error('Could not load permanent manuscript.'); return r.text(); })
  ]).then(async ([indexHtml, recoveredMarkdown, manuscript]) => {
    const published = parsePublishedIndex(indexHtml);
    const publishedNumbers = new Set(published.map((chapter) => chapter.number));
    const recovered = parseManuscript(recoveredMarkdown, 'recovered').filter((chapter) => !publishedNumbers.has(chapter.number)).sort((a, b) => a.number - b.number);
    const occupiedNumbers = new Set([...published, ...recovered].map((chapter) => chapter.number));
    const forward = parseManuscript(manuscript, 'manuscript').filter((chapter) => !occupiedNumbers.has(chapter.number)).sort((a, b) => a.number - b.number);
    const available = [...published, ...recovered, ...forward].sort((a, b) => a.number - b.number);
    const latest = forward[forward.length - 1] || recovered[recovered.length - 1] || published[published.length - 1] || null;

    if (!requested) {
      numberNode.textContent = latest ? `CURRENT THROUGH CHAPTER ${latest.number}` : 'LIGHT READER';
      titleNode.textContent = 'LIGHT TABLE OF CONTENTS';
      renderCurrentShortcut(forward);
      renderToc(available);
      setStatus(latest ? `${available.length} exact-text chapters are materialized in GitHub. Current manuscript endpoint: Chapter ${latest.number} — ${latest.title}.` : `${available.length} exact-text chapters currently available.`);
      return;
    }

    const chapter = available.find((c) => c.number === requested);
    if (!chapter) return showMissing(available, requested);
    await showChapter(available, chapter);
  }).catch((error) => {
    setStatus(error.message || 'Could not initialize the light reader.');
  });
})();