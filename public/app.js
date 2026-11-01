/* Scrubmello shared page code: header, footer, product cards, day/night mode, scroll effects. */
(function () {
  var SM = window.SM, S = SM.site;
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var price = function (p) { return p == null ? '<span class="tbc">Price coming soon</span>' : '£' + Number(p).toFixed(2); };
  var pad = function (n) { return (n < 10 ? '0' : '') + n; };

  /* ---------- header ---------- */
  var hdr = document.getElementById('site-header');
  if (hdr) hdr.innerHTML =
    (S.underConstruction ? '<div class="uc" role="note">Preview site · Built by <a href="https://bhxuk.com" target="_blank" rel="noopener">bhxuk.com</a></div>' : '') +
    '<nav class="nav"><div class="wrap">' +
    ' <a class="logo" href="#" aria-label="Scrubmello home"><i></i>scrubmello</a>' +
    ' <div class="nav-links"><a href="#system">System</a><a href="#handles">Handles</a><a href="#heads">Heads</a><a href="#colours">Colours</a><a href="#sets">Sets</a><a href="#faq">FAQ</a></div>' +
    ' <div class="nav-right"><button class="mode" id="mode" type="button" aria-label="Switch day or night mode"><b></b><span id="mode-t">Night</span></button><a class="pill" href="#join">Join</a></div>' +
    '</div></nav>';

  /* ---------- footer ---------- */
  var ftr = document.getElementById('site-footer');
  if (ftr) ftr.innerHTML =
    '<footer><div class="wrap f-grid">' +
    ' <div><a class="logo" href="#"><i></i>scrubmello</a><p style="margin-top:12px">' + esc(S.tagline) + '</p></div>' +
    ' <div><h4>Range</h4><a href="#handles">Handles</a><a href="#heads">Heads</a><a href="#sets">Sets</a></div>' +
    ' <div><h4>Help</h4><a href="#faq">FAQ</a><a href="#materials">Materials</a></div>' +
    ' <div><h4>Contact</h4><a href="mailto:' + esc(S.email) + '">' + esc(S.email) + '</a></div>' +
    '</div><div class="f-word" aria-hidden="true">scrubmello</div>' +
    '<div class="f-legal"><span>© ' + new Date().getFullYear() + ' Scrubmello</span><span>Designed in Birmingham</span></div></footer>';

  /* ---------- day / night ---------- */
  var root = document.documentElement, mb = document.getElementById('mode'), mt = document.getElementById('mode-t');
  var sync = function () { if (mt) mt.textContent = root.getAttribute('data-theme') === 'night' ? 'Day' : 'Night'; };
  sync();
  if (mb) mb.addEventListener('click', function () {
    var t = root.getAttribute('data-theme') === 'night' ? 'day' : 'night';
    root.setAttribute('data-theme', t); sync();
    try { localStorage.setItem('sm-theme', t); } catch (e) {}
  });

  /* ---------- product cards ---------- */
  function card(item, i, extra) {
    return '<article class="card reveal"><div class="ph"><span class="n">' + pad(i + 1) + '</span><img src="' + esc(item.img) + '" alt="' + esc(item.name) + '" loading="lazy" width="800" height="1000"></div>' +
      '<div class="meta"><div><h3>' + esc(item.name) + (extra || '') + '</h3>' + (item.spec ? '<p class="spec">' + esc(item.spec) + '</p>' : '') + '</div>' + price(item.price) + '</div>' +
      '<p class="d">' + esc(item.desc) + '</p></article>';
  }
  var g;
  if ((g = document.getElementById('grid-handles'))) g.innerHTML = SM.handles.map(function (h, i) { return card(h, i); }).join('');
  if ((g = document.getElementById('grid-heads'))) g.innerHTML = SM.heads.map(function (h, i) { return card(h, i, ' head'); }).join('');
  if ((g = document.getElementById('grid-sets'))) g.innerHTML = SM.sets.map(function (s, i) { return card(s, i); }).join('');
  if ((g = document.getElementById('swatches'))) g.innerHTML = SM.colours.map(function (c) {
    return '<span class="sw"><i style="background:' + (c.hex === 'rainbow' ? 'var(--rainbow)' : c.hex) + '"></i>' + esc(c.name) + '</span>';
  }).join('');

  /* ---------- statement: words light up as you scroll ---------- */
  var w = document.querySelector('[data-words]'), spans = [];
  if (w) {
    w.innerHTML = w.textContent.trim().split(/\s+/).map(function (x) { return '<span>' + esc(x) + '</span>'; }).join(' ');
    spans = w.querySelectorAll('span');
  }

  /* ---------- reveal on scroll ---------- */
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (e) { io.observe(e); });
  } else els.forEach(function (e) { e.classList.add('in'); });

  var tick = false;
  function onScroll() {
    tick = false;
    if (spans.length) {
      var r = w.getBoundingClientRect(), vh = innerHeight;
      var p = Math.min(Math.max((vh * 0.85 - r.top) / (r.height + vh * 0.35), 0), 1);
      var n = Math.round(p * spans.length);
      for (var i = 0; i < spans.length; i++) spans[i].classList.toggle('on', i < n);
    }
  }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* ---------- join form (opens an email until a real sign-up is wired in) ---------- */
  var f = document.getElementById('join-form');
  if (f) f.addEventListener('submit', function (e) {
    e.preventDefault();
    var em = f.querySelector('[name=email]').value;
    location.href = 'mailto:' + S.email + '?subject=' + encodeURIComponent('Scrubmello launch list') + '&body=' + encodeURIComponent('Please add me to the launch list: ' + em);
  });
})();
