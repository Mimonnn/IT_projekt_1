(() => {
  const carousel = document.querySelector('[data-slideshow]');
  if (!carousel) return;
  const slides = [...carousel.querySelectorAll('[data-slide]')];
  const buttons = [...carousel.querySelectorAll('[data-slide-button]')];
  const pause = carousel.querySelector('[data-pause]');
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let index = 0;
  let paused = motion.matches;
  let timer;

  function schedule() {
    window.clearTimeout(timer);
    if (!paused && !document.hidden && !carousel.contains(document.activeElement)) {
      timer = window.setTimeout(() => show((index + 1) % slides.length), 6000);
    }
  }

  function show(next) {
    index = next;
    slides.forEach((slide, i) => {
      slide.classList.toggle('is-current', i === index);
      slide.setAttribute('aria-hidden', String(i !== index));
      buttons[i].setAttribute('aria-pressed', String(i === index));
    });
    schedule();
  }

  function updatePause() {
    pause.textContent = paused ? 'Wznów pokaz' : 'Wstrzymaj pokaz';
    pause.setAttribute('aria-pressed', String(paused));
    schedule();
  }

  buttons.forEach((button, i) => button.addEventListener('click', () => show(i)));
  pause.addEventListener('click', () => { paused = !paused; updatePause(); });
  carousel.addEventListener('focusin', schedule);
  carousel.addEventListener('focusout', () => window.setTimeout(schedule, 0));
  document.addEventListener('visibilitychange', schedule);
  motion.addEventListener('change', () => { paused = motion.matches; updatePause(); });
  carousel.querySelector('[data-controls]').hidden = false;
  updatePause();
})();
