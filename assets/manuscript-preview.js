(() => {
  const root = document.querySelector('[data-manuscript-chapter]');
  if (!root) return;

  const chapter = String(root.dataset.manuscriptChapter || '').trim();
  const source = root.dataset.manuscriptSource || '../state/manuscript/Peg_Leg_Greg_Running_Manuscript.md';
  const titleNode = document.querySelector('[data-chapter-title]');
  const statusNode = document.querySelector('[data-preview-status]');

  const fail = (message) => {
    if (statusNode) statusNode.textContent = message;
    root.innerHTML = '';
    const p = document.createElement('p');
    p.textContent = message;
    root.appendChild(p);
  };

  const render = (markdown) => {
    const text = markdown.replace(/\r\n?/g, '\n');
    const escapedChapter = chapter.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const manuscriptHeading = new RegExp(`^# CHAPTER ${escapedChapter}\\s*$`, 'm');
    const standaloneHeading = new RegExp(`^# ${escapedChapter}\\s+[—-]\\s+(.+)\\s*$`, 'm');
    const manuscriptMatch = manuscriptHeading.exec(text);
    const standaloneMatch = standaloneHeading.exec(text);

    let title;
    let body;

    if (manuscriptMatch) {
      const afterHeading = manuscriptMatch.index + manuscriptMatch[0].length;
      const remainder = text.slice(afterHeading);
      const nextHeading = /^# CHAPTER [0-9]+[A-Z]?\s*$/m.exec(remainder);
      let chunk = nextHeading ? remainder.slice(0, nextHeading.index) : remainder;
      chunk = chunk.replace(/^-{20,}\s*$/gm, '').trim();

      const titleMatch = /^##\s+(.+)\s*$/m.exec(chunk);
      if (!titleMatch) throw new Error(`Chapter ${chapter} title could not be read.`);
      title = titleMatch[1].trim();
      body = chunk.slice(titleMatch.index + titleMatch[0].length).trim();
    } else if (standaloneMatch) {
      title = standaloneMatch[1].trim();
      body = text.slice(standaloneMatch.index + standaloneMatch[0].length).trim();
    } else {
      throw new Error(`Chapter ${chapter} could not be found in its manuscript source.`);
    }

    const blocks = body.split(/\n\s*\n+/).map((block) => block.trim()).filter(Boolean);

    if (titleNode) titleNode.textContent = title;
    document.title = `Chapter ${chapter}: ${title} — Peg-Leg Greg`;
    root.innerHTML = '';

    for (const block of blocks) {
      if (/^-{20,}$/.test(block)) continue;
      const p = document.createElement('p');
      p.textContent = block;
      root.appendChild(p);
    }

    if (statusNode) statusNode.textContent = 'Rendered directly from the permanent GitHub manuscript.';
  };

  fetch(source, { cache: 'no-store' })
    .then((response) => {
      if (!response.ok) throw new Error(`Could not load manuscript (${response.status}).`);
      return response.text();
    })
    .then(render)
    .catch((error) => fail(error.message || 'Could not load this manuscript preview.'));
})();
