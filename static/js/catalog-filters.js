(() => {
  const category = document.querySelector('#category');
  const group = document.querySelector('[data-subcategory-filter]');
  const data = document.querySelector('#subcategory-options');
  if (!category || !group || !data) return;
  const options = JSON.parse(data.textContent);
  const subcategory = group.querySelector('select');
  function update(reset = false) {
    const choices = options[category.value] || [];
    const selected = reset ? '' : subcategory.value;
    subcategory.replaceChildren(new Option('Wszystkie podkategorie', ''));
    choices.forEach(([value, label]) => subcategory.add(new Option(label, value)));
    subcategory.value = choices.some(([value]) => value === selected) ? selected : '';
    group.hidden = choices.length === 0;
    subcategory.disabled = choices.length === 0;
  }
  category.addEventListener('change', () => update(true));
  window.addEventListener('pageshow', () => update());
  update();
})();
