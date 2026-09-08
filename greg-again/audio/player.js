(async () => {
  const audio = document.getElementById('audio');
  const status = document.getElementById('status');
  const renderState = document.getElementById('render-state');
  const fullAudioLink = document.getElementById('full-audio-link');
  try {
    const response = await fetch('manifest.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`manifest ${response.status}`);
    const manifest = await response.json();
    status.textContent = manifest.status === 'approved' ? 'Approved' : 'Experimental';
    status.dataset.state = manifest.status;

    if (manifest.audio_src) {
      audio.src = manifest.audio_src;
      audio.removeAttribute('aria-disabled');
      if (manifest.embedded_scope === 'opening_preview') {
        renderState.textContent = 'Playable opening preview. Full Chapter 1 is linked below.';
      } else if (manifest.embedded_scope === 'full_chapter' && manifest.status === 'approved') {
        renderState.textContent = 'Qualified full Chapter 1 render.';
      } else if (manifest.embedded_scope === 'full_chapter') {
        renderState.textContent = 'Playable full Chapter 1 render. Not yet qualified.';
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

    if (fullAudioLink) {
      if (manifest.full_audio_url) {
        fullAudioLink.href = manifest.full_audio_url;
        fullAudioLink.hidden = false;
      } else {
        fullAudioLink.hidden = true;
      }
    }
  } catch (error) {
    audio.removeAttribute('src');
    audio.setAttribute('aria-disabled', 'true');
    renderState.textContent = 'Audio render not yet qualified.';
    if (fullAudioLink) fullAudioLink.hidden = true;
    console.error(error);
  }
})();
