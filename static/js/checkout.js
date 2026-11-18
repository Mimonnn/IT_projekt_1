(() => {
  const form = document.querySelector('#checkout-form');
  const pricingNode = document.querySelector('#checkout-pricing');
  if (!form || !pricingNode) return;
  const pricing = JSON.parse(pricingNode.textContent);
  const ui = JSON.parse(document.querySelector('#ui-strings').textContent);
  const shipping = form.querySelector('[data-shipping-fields]');
  const pickup = form.querySelector('[data-pickup-fields]');
  const submit = form.querySelector('.checkout-submit');
  const locale = document.documentElement.lang;
  const integers = new Intl.NumberFormat(locale, {maximumFractionDigits: 0, useGrouping: true});
  const separator = new Intl.NumberFormat(locale).formatToParts(1.1).find(part => part.type === 'decimal').value;
  const cents = value => BigInt(value.replace('.', ''));
  const money = value => `${integers.format(value / 100n)}${separator}${String(value % 100n).padStart(2, '0')} ${ui.currency}`;
  function update() {
    const method = form.querySelector('input[name="delivery_method"]:checked')?.value || 'pickup';
    shipping.hidden = method !== 'courier';
    pickup.hidden = method !== 'pickup';
    for (const group of [shipping, pickup]) {
      group.querySelectorAll('input, select').forEach(input => {
        input.disabled = group.hidden;
        input.required = !group.hidden;
      });
    }
    const fee = cents(pricing.fees[method]);
    form.querySelector('[data-delivery-total]').textContent = money(fee);
    form.querySelector('[data-order-total]').textContent = money(cents(pricing.subtotal) + fee);
  }
  form.querySelectorAll('input[name="delivery_method"]').forEach(input => input.addEventListener('change', update));
  form.addEventListener('submit', () => { submit.disabled = true; form.setAttribute('aria-busy', 'true'); });
  window.addEventListener('pageshow', () => { submit.disabled = form.dataset.canCheckout !== 'true'; form.removeAttribute('aria-busy'); update(); });
  update();
})();
