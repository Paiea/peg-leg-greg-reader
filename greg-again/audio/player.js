(async () => {
  const audio = document.getElementById('audio');
  const status = document.getElementById('status');
  const renderState = document.getElementById('render-state');
  try {
    const response = await fetch('manifest.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`manifest ${response.status}`);
    const manifest = await response.json();
    status.textContent = manifest.status === 'approved' ? 'Approved' : 'Experimental';
    status.dataset.state = manifest.status;

    if (manifest.audio_src) {
      audio.src = manifest.audio_src;
      audio.removeAttribute('aria-disabled');
      if (manifest.sample_status === 'full_chapter_experimental') {
        renderState.textContent = 'Full Chapter 1 experimental render. Not yet qualified.';
      } else if (manifest.sample_status === 'narrator_audition') {
        renderState.textContent = 'Experimental narrator audition. Not yet qualified.';
      } else if (manifest.status === 'approved') {
        renderState.textContent = 'Qualified Chapter 1 render.';
      } else {
        renderState.textContent = 'Playable experimental render. Not yet qualified.';
      }
    } else {
      audio.removeAttribute('src');
      audio.setAttribute('aria-disabled', 'true');
      renderState.textContent = 'Audio render not yet qualified.';
    }
  } catch (error) {
    audio.removeAttribute('src');
    audio.setAttribute('aria-disabled', 'true');
    renderState.textContent = 'Audio render not yet qualified.';
    console.error(error);
  }
})();
