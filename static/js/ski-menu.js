// Podmenu jest nakładką poza układem nawigacji; zmienia się wyłącznie jego widoczność.
const categoryMenus = [...document.querySelectorAll('[data-ski-menu]')];
categoryMenus.forEach((menu) => {
  const trigger = menu.querySelector('.ski-menu-trigger');
  const panel = menu.querySelector('.ski-submenu');
  function setOpen(open) {
    if (open) {
      categoryMenus.forEach((other) => {
        if (other === menu) return;
        other.querySelector('.ski-submenu').hidden = true;
        other.querySelector('.ski-menu-trigger').setAttribute('aria-expanded', 'false');
      });
    }
    panel.hidden = !open;
    trigger.setAttribute('aria-expanded', String(open));
  }
  trigger.addEventListener('click', (event) => {
    // Klik myszy nie zamyka panelu otwartego chwilę wcześniej przez najechanie.
    const mouseClick = event.detail > 0 && window.matchMedia('(hover: hover)').matches;
    setOpen(mouseClick || panel.hidden);
  });
  menu.addEventListener('pointerenter', (event) => {
    if (event.pointerType === 'mouse') setOpen(true);
  });
  menu.addEventListener('pointerleave', (event) => {
    if (event.pointerType === 'mouse' && !menu.contains(document.activeElement)) setOpen(false);
  });
  menu.addEventListener('focusout', (event) => {
    if (!menu.contains(event.relatedTarget)) setOpen(false);
  });
  menu.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      setOpen(false);
      trigger.focus();
    } else if (event.key === 'ArrowDown' && event.target === trigger) {
      event.preventDefault();
      setOpen(true);
      panel.querySelector('a').focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!menu.contains(event.target)) setOpen(false);
  });
});
