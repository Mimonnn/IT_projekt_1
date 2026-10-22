document.addEventListener('DOMContentLoaded', () => {
  const category = document.querySelector('#id_category');
  const subcategory = document.querySelector('#id_subcategory');
  if (!category || !subcategory) return;
  const options = JSON.parse(subcategory.dataset.subcategories);
  function update(reset = false) {
    const selected = reset ? '' : subcategory.value;
    const choices = options[category.value] || [];
    subcategory.replaceChildren(new Option('---------', ''));
    choices.forEach(([value, label]) => subcategory.add(new Option(label, value)));
    subcategory.value = choices.some(([value]) => value === selected) ? selected : '';
    subcategory.required = choices.length > 0;
  }
  category.addEventListener('change', () => update(true));
  update();
});
