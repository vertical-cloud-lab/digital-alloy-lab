() => {
  const sep = [...document.querySelectorAll('li, h2, h3, div, span')].find(e =>
      /Results matching fewer words|Results for fewer words/i.test(e.textContent || '') && (e.textContent || '').length < 120);
  const seen = new Set(); const cards = [];
  for (const a of document.querySelectorAll('a[href*="/itm/"]')) {
    const li = a.closest('li'); if (!li || seen.has(li)) continue; seen.add(li);
    const m = a.href.match(/\/itm\/(?:[^/?]*\/)?(\d{9,})/);
    let after = false;
    if (sep) after = !!(sep.compareDocumentPosition(li) & Node.DOCUMENT_POSITION_FOLLOWING) && !sep.contains(li);
    cards.push({item_id: m ? m[1] : null, url: m ? 'https://www.ebay.com/itm/' + m[1] : a.href.split('?')[0],
                text: (li.innerText || '').replace(/\n{2,}/g, '\n').trim().slice(0, 900), after_fewer_words: after});
  }
  const h = [...document.querySelectorAll('h1, h2')].map(e => e.innerText.trim()).filter(t => /results? for/i.test(t))[0] || '';
  return {heading: h, has_separator: !!sep, title: document.title, url: location.href, cards};
}
