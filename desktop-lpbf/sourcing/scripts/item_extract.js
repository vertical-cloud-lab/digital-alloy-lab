() => {
  const q = s => document.querySelector(s);
  const txt = e => e ? e.innerText.trim() : null;
  const specs = {};
  document.querySelectorAll('.ux-labels-values').forEach(r => {
    const l = r.querySelector('.ux-labels-values__labels'); const v = r.querySelector('.ux-labels-values__values');
    if (l && v) specs[l.innerText.trim().replace(/:$/, '')] = v.innerText.trim().slice(0, 400);
  });
  const iframe = q('iframe#desc_ifr');
  return {title: txt(q('h1')), price: txt(q('.x-price-primary')) || txt(q('[data-testid="x-price-primary"]')),
          condition: txt(q('.x-item-condition-text')) || txt(q('[data-testid="x-item-condition"]')),
          specs, desc_src: iframe ? iframe.src : null, url: location.href, title_tag: document.title,
          body: (document.body.innerText || '').slice(0, 14000)};
}
