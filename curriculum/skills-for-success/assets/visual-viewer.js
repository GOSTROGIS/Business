/* Local image viewer. Parameters are text and allowlisted asset paths, never HTML. */
(() => {
  'use strict';
  const query = new URLSearchParams(window.location.search);
  const stage = document.getElementById('visual-stage');
  const picture = document.getElementById('viewer-image');
  const status = document.getElementById('viewer-status');
  const error = document.getElementById('viewer-error');
  const buttons = [...document.querySelectorAll('.viewer-controls button')];
  const back = document.getElementById('viewer-return');
  const root = new URL('../', window.location.href);
  const asset = query.get('asset') || '';
  const title = query.get('title') || 'Learning visual';
  const description = query.get('description') || 'Read the caption and explanation in the learning chapter.';
  const minScale = 0.1;
  const maxScale = 4;
  let scale = 1;
  let fitted = true;
  let ready = false;
  let drag = null;

  document.getElementById('viewer-title').textContent = title;
  document.getElementById('viewer-description').textContent = description;
  document.title = `${title} | ACCESS IS4S visual`;
  picture.alt = description;
  buttons.forEach(button => { button.disabled = true; });

  // A return link may point only to a reading page inside this curriculum tree.
  try {
    const candidate = new URL(query.get('return') || '../index.html', window.location.href);
    if (candidate.origin === root.origin && candidate.protocol === root.protocol &&
        candidate.pathname.startsWith(root.pathname) && candidate.pathname.endsWith('.html') &&
        candidate.pathname !== window.location.pathname) back.href = candidate.href;
  } catch (_) { /* The ordinary books link remains available. */ }

  function fail(message) {
    error.textContent = message;
    error.hidden = false;
    status.textContent = 'Visual unavailable';
    buttons.forEach(button => { button.disabled = true; });
  }

  function fitScale() {
    return Math.min(1, Math.max(minScale, (stage.clientWidth - 24) / picture.naturalWidth));
  }

  function render(next, fit = false) {
    if (!ready) return;
    const oldWidth = picture.clientWidth || picture.naturalWidth;
    const oldHeight = picture.clientHeight || picture.naturalHeight;
    const centerX = (stage.scrollLeft + stage.clientWidth / 2) / oldWidth;
    const centerY = (stage.scrollTop + stage.clientHeight / 2) / oldHeight;
    scale = Math.max(minScale, Math.min(maxScale, next));
    fitted = fit;
    stage.classList.toggle('is-fitted', fit);
    picture.style.width = `${Math.round(picture.naturalWidth * scale)}px`;
    picture.style.height = `${Math.round(picture.naturalHeight * scale)}px`;
    stage.scrollLeft = fit ? 0 : centerX * picture.clientWidth - stage.clientWidth / 2;
    stage.scrollTop = fit ? 0 : centerY * picture.clientHeight - stage.clientHeight / 2;
    status.textContent = `${Math.round(scale * 100)}%${fit ? ' · fit width' : ''}`;
    document.getElementById('viewer-out').disabled = scale <= minScale;
    document.getElementById('viewer-in').disabled = scale >= maxScale;
    stage.classList.toggle('is-draggable', picture.clientWidth > stage.clientWidth || picture.clientHeight > stage.clientHeight);
  }

  document.getElementById('viewer-fit').addEventListener('click', () => render(fitScale(), true));
  document.getElementById('viewer-actual').addEventListener('click', () => render(1));
  document.getElementById('viewer-in').addEventListener('click', () => render(scale * 1.25));
  document.getElementById('viewer-out').addEventListener('click', () => render(scale / 1.25));
  stage.addEventListener('keydown', event => {
    if (event.ctrlKey || event.metaKey || event.altKey || !ready) return;
    const step = event.shiftKey ? 120 : 40;
    const moves = {ArrowLeft: [-step, 0], ArrowRight: [step, 0], ArrowUp: [0, -step], ArrowDown: [0, step]};
    if (moves[event.key]) {
      event.preventDefault();
      stage.scrollBy(...moves[event.key]);
    } else if (['+', '=', '-', '−', '0', '1', 'Escape'].includes(event.key)) {
      event.preventDefault();
      if (event.key === '+' || event.key === '=') render(scale * 1.25);
      else if (event.key === '-' || event.key === '−') render(scale / 1.25);
      else if (event.key === '0') render(fitScale(), true);
      else if (event.key === '1') render(1);
      else back.focus();
    }
  });

  // Mouse drag supplements native scrollbars; touch keeps native pan/pinch behavior.
  stage.addEventListener('pointerdown', event => {
    if (!ready || event.pointerType !== 'mouse' || event.button !== 0 || !stage.classList.contains('is-draggable')) return;
    drag = {x: event.clientX, y: event.clientY, left: stage.scrollLeft, top: stage.scrollTop};
    stage.setPointerCapture(event.pointerId);
    stage.classList.add('is-dragging');
    stage.focus({preventScroll: true});
    event.preventDefault();
  });
  stage.addEventListener('pointermove', event => {
    if (!drag) return;
    stage.scrollLeft = drag.left - (event.clientX - drag.x);
    stage.scrollTop = drag.top - (event.clientY - drag.y);
  });
  for (const name of ['pointerup', 'pointercancel', 'lostpointercapture']) {
    stage.addEventListener(name, () => { drag = null; stage.classList.remove('is-dragging'); });
  }
  window.addEventListener('resize', () => { if (ready && fitted) render(fitScale(), true); });

  if (!/^(diagrams|illustrations)\/[A-Za-z0-9._-]+\.(svg|png|jpe?g|webp)$/i.test(asset)) {
    fail('Choose a visual from a learning chapter. This link does not name an available local image.');
    return;
  }
  picture.addEventListener('load', () => {
    if (!picture.naturalWidth || !picture.naturalHeight) {
      fail('The image has no readable dimensions. Return to the chapter for its text description.');
      return;
    }
    ready = true;
    picture.hidden = false;
    buttons.forEach(button => { button.disabled = false; });
    render(fitScale(), true);
  });
  picture.addEventListener('error', () => fail('The image could not be opened. Its description is below; use the return link to continue reading.'));
  const imageURL = new URL(asset, window.location.href);
  const original = document.getElementById('viewer-original');
  original.href = imageURL.href;
  original.hidden = false;
  picture.src = imageURL.href;
})();
