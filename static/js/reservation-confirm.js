(() => {
  const form = document.querySelector('[data-reservation-confirm]');
  const start = document.querySelector('#id_start_date');
  const end = document.querySelector('#id_end_date');
  const notice = document.querySelector('#reservation-dates-changed');
  if (!form || !start || !end || !notice) return;
  const button = form.querySelector('button[type="submit"]');
  function update() {
    const changed = start.value !== form.dataset.startDate || end.value !== form.dataset.endDate;
    button.disabled = changed;
    notice.hidden = !changed;
  }
  [start, end].forEach(input => {
    input.addEventListener('input', update);
    input.addEventListener('change', update);
  });
  window.addEventListener('pageshow', update);
  update();
})();
