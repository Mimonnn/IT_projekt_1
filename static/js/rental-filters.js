(() => {
  const category = document.querySelector('#rental-category');
  const model = document.querySelector('#rental-model');
  const size = document.querySelector('#rental-size');
  const data = document.querySelector('#rental-options');
  if (!category || !model || !size || !data) return;
  const rows = JSON.parse(data.textContent);
  const ui = JSON.parse(document.querySelector('#ui-strings').textContent);
  const allModels = model.options[0].text;
  const allSizes = size.options[0].text;
  function populate(select, choices, label, reset) {
    const selected = reset ? '' : select.value;
    select.replaceChildren(new Option(label, ''));
    [...choices.entries()].sort((a, b) => a[1].localeCompare(b[1], document.documentElement.lang, {numeric: true}))
      .forEach(([value, text]) => select.add(new Option(text, value)));
    if (selected && !choices.has(selected)) {
      select.add(new Option(`${selected} — ${ui.notInGroup}`, selected));
    }
    select.value = selected;
  }
  function updateSizes(reset = false) {
    const choices = rows.filter(row => (!category.value || row.category === category.value) &&
      (!model.value || row.model === model.value));
    populate(size, new Map(choices.map(row => [row.size, row.size_label])), allSizes, reset);
  }
  function updateModels(reset = false) {
    const choices = rows.filter(row => !category.value || row.category === category.value);
    populate(model, new Map(choices.map(row => [row.model, row.name])), allModels, reset);
    updateSizes(reset);
  }
  category.addEventListener('change', () => updateModels(true));
  model.addEventListener('change', () => updateSizes(true));
  window.addEventListener('pageshow', () => updateModels());
  updateModels();
})();
