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
  const specificationData = document.querySelector('#specification-options');
  const specifications = specificationData ? JSON.parse(specificationData.textContent) : [];
  function updateSpecifications(reset = false) {
    const rows = specifications.filter(item => (!category.value || item.category === category.value) &&
      (!subcategory.value || item.subcategory === subcategory.value));
    const sizes = [...new Set(rows.map(item => item.size).filter(Boolean))].sort((a, b) => a.localeCompare(b, 'pl', {numeric:true}));
    const materials = new Map(rows.flatMap(item => item.materials));
    const materialChoices = [...materials.entries()].sort((a, b) => a[1].localeCompare(b[1], 'pl'));
    function populate(selector, choices, label) {
      const select = document.querySelector(selector);
      if (!select) return;
      const selected = reset ? '' : select.value;
      select.replaceChildren(new Option(label, ''));
      choices.forEach(([value, text]) => select.add(new Option(text, value)));
      if (selected && !choices.some(([value]) => value === selected)) {
        select.add(new Option(`${selected} — brak w tej grupie`, selected));
      }
      select.value = selected;
    }
    populate('#size', sizes.map(size => [size, size]), 'Wszystkie rozmiary');
    populate('#material', materialChoices, 'Wszystkie materiały');
  }
  category.addEventListener('change', () => { update(true); updateSpecifications(true); });
  subcategory.addEventListener('change', () => updateSpecifications(true));
  window.addEventListener('pageshow', () => { update(); updateSpecifications(); });
  update();
  updateSpecifications();
})();
