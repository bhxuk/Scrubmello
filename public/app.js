/* Scrubmello shared page code: header, footer, product drawings, builder, product cards. */
(function () {
  var SM = window.SM, S = SM.site;
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var price = function (p) { return p == null ? '<span class="tbc">Price coming soon</span>' : '£' + Number(p).toFixed(2); };
  var uid = 0;

  /* ---------- drawings ----------
     Every product is drawn from the same parts so the range always looks like one family:
     an egg-shaped head, a Mello Click socket and one of four handles. */
  var col = function (id) { for (var i = 0; i < SM.colours.length; i++) if (SM.colours[i].id === id) return SM.colours[i]; return SM.colours[0]; };
  var dark = function (id) { return id === 'black' ? 'rgba(255,255,255,.28)' : 'rgba(0,0,0,.16)'; };

  function paint(id, defs) {
    if (id !== 'rainbow') return col(id).hex;
    var g = 'rb' + (++uid);
    defs.push('<linearGradient id="' + g + '" x1="0" y1="0" x2="1" y2="1">' +
      ['#f6bfcd', '#f9d2ae', '#f8e59a', '#bfe5c7', '#b3d8f0', '#cfc2ef'].map(function (c, i) { return '<stop offset="' + (i / 5) + '" stop-color="' + c + '"/>'; }).join('') +
      '</linearGradient>');
    return 'url(#' + g + ')';
  }

  var EGG = 'M100 20C138 20 160 46 160 80C160 120 130 158 100 158C70 158 40 120 40 80C40 46 62 20 100 20Z';
  var SLIM = 'M100 14C121 14 132 40 132 72C132 112 116 158 100 158C84 158 68 112 68 72C68 40 79 14 100 14Z';

  function texture(tex, c, clip) {
    var out = '', x, y;
    var dots = function (step, r) {
      for (y = 20; y < 160; y += step) for (x = 40 + ((y / step) % 2 ? step / 2 : 0); x < 162; x += step) out += '<circle cx="' + x + '" cy="' + y + '" r="' + r + '" fill="' + c + '"/>';
    };
    if (tex === 'bristle') dots(11, 3);
    else if (tex === 'fine') dots(7, 1.6);
    else if (tex === 'nub') dots(18, 5.5);
    else if (tex === 'crease') dots(8, 2);
    else if (tex === 'mesh') { for (x = -40; x < 220; x += 12) out += '<path d="M' + x + ' 10l90 160M' + (x + 90) + ' 10l-90 160" stroke="' + c + '" stroke-width="2" fill="none"/>'; }
    else if (tex === 'cloth') { for (y = 26; y < 160; y += 10) out += '<path d="M30 ' + y + 'q12-6 24 0t24 0 24 0 24 0 24 0 24 0" stroke="' + c + '" stroke-width="2.4" fill="none" stroke-linecap="round"/>'; }
    else if (tex === 'face') { dots(7, 1.6); out += '<ellipse cx="100" cy="84" rx="34" ry="38" fill="#fff" opacity=".85"/><ellipse cx="100" cy="84" rx="34" ry="38" fill="none" stroke="' + c + '" stroke-width="2" stroke-dasharray="3 4"/>'; }
    return '<g clip-path="url(#' + clip + ')">' + out + '</g>';
  }

  function handle(kind, fill, line) {
    var s = '<rect x="84" y="152" width="32" height="24" rx="8" fill="' + fill + '"/><rect x="84" y="160" width="32" height="5" fill="' + line + '"/>';
    if (kind === 'pebble' || kind === 'mini') {
      s += '<path d="M100 172C128 172 138 206 138 236C138 272 121 300 100 300C79 300 62 272 62 236C62 206 72 172 100 172Z" fill="' + fill + '"/>' +
           '<circle cx="100" cy="284" r="6" fill="var(--bg-draw,#fff)"/>';
    } else if (kind === 'reach') {
      s += '<path d="M100 172C100 230 106 284 126 330" stroke="' + fill + '" stroke-width="22" fill="none" stroke-linecap="round"/>' +
           '<circle cx="130" cy="342" r="10" fill="none" stroke="' + fill + '" stroke-width="6"/>';
    } else if (kind === 'easy') {
      s += '<path d="M84 172H116C124 214 152 248 152 288C152 322 132 344 106 344C80 344 64 324 64 298C64 262 78 226 84 172Z" fill="' + fill + '"/>' +
           '<path d="M74 268q30 10 72 0M70 292q34 10 80 0M72 316q32 9 72 0" stroke="' + line + '" stroke-width="3" fill="none" stroke-linecap="round"/>';
    }
    return s;
  }

  function draw(o) {
    var defs = [], clip = 'c' + (++uid);
    var hf = paint(o.headCol, defs), gf = paint(o.handleCol, defs);
    var head = SM.heads.filter(function (h) { return h.id === o.head; })[0] || SM.heads[0];
    var shape = head.tex === 'crease' ? SLIM : EGG;
    var body = handle(o.handle, gf, dark(o.handleCol)) +
      '<path d="' + shape + '" fill="' + hf + '"/>' + texture(head.tex, dark(o.headCol), clip) +
      (o.headCol === 'white' ? '<path d="' + shape + '" fill="none" stroke="#d9d5cd" stroke-width="2"/>' : '') +
      (o.handleCol === 'white' ? '' : '');
    if (o.handle === 'mini') body = '<g transform="translate(25 40) scale(.75)">' + body + '</g>';
    return '<svg viewBox="0 0 200 360" role="img" aria-label="' + esc(o.label || 'Scrubmello scrubber') + '">' +
      '<defs>' + defs.join('') + '<clipPath id="' + clip + '"><path d="' + shape + '"' + (o.handle === 'mini' ? '' : '') + '/></clipPath></defs>' + body + '</svg>';
  }
  SM.draw = draw;

  /* ---------- header ---------- */
  var hdr = document.getElementById('site-header');
  if (hdr) hdr.innerHTML =
    (S.underConstruction ? '<div class="uc" role="note">Site under construction · Built by <a href="https://bhxuk.com" target="_blank" rel="noopener">bhxuk.com</a></div>' : '') +
    '<div class="bar">' + esc(S.note) + '</div>' +
    '<nav><div class="wrap">' +
    ' <a class="logo" href="index.html" aria-label="Scrubmello home"><span class="dot"></span>scrub<span>mello</span></a>' +
    ' <div class="links"><a href="#how">How it works</a><a href="#build">Build yours</a><a href="#handles">Handles</a><a href="#heads">Heads</a><a href="#sets">Sets</a><a href="#faq">FAQ</a></div>' +
    ' <a class="btn sm" href="#join">Join the list</a>' +
    '</div></nav>';

  /* ---------- footer ---------- */
  var ftr = document.getElementById('site-footer');
  if (ftr) ftr.innerHTML =
    '<footer><div class="wrap">' +
    ' <div><a class="logo" href="index.html"><span class="dot"></span>scrub<span>mello</span></a><p>' + esc(S.tagline) + '</p></div>' +
    ' <div><h4>Shop</h4><a href="#handles">Handles</a><a href="#heads">Heads</a><a href="#sets">Sets</a></div>' +
    ' <div><h4>Help</h4><a href="#faq">FAQ</a><a href="#join">Contact</a><a href="mailto:' + esc(S.email) + '">' + esc(S.email) + '</a></div>' +
    ' <div class="legal">© ' + new Date().getFullYear() + ' Scrubmello. All rights reserved.</div>' +
    '</div></footer>';

  /* ---------- product cards ---------- */
  var colourIds = ['pink', 'blue', 'yellow', 'black', 'white', 'rainbow'];
  function card(item, art) {
    return '<article class="p"><div class="ph">' + art + '</div><h3>' + esc(item.name) + '</h3><p class="d">' + esc(item.desc) + '</p><div class="m">' + price(item.price) + '</div></article>';
  }
  var g;
  if ((g = document.getElementById('grid-handles'))) g.innerHTML = SM.handles.map(function (h, i) {
    return card(h, draw({ handle: h.id, head: 'body', headCol: 'white', handleCol: colourIds[i % 6], label: h.name }));
  }).join('');
  if ((g = document.getElementById('grid-heads'))) g.innerHTML = SM.heads.map(function (h, i) {
    return card(h, draw({ handle: 'pebble', head: h.id, headCol: h.id === 'intimate' ? 'pink' : colourIds[i % 6], handleCol: 'white', label: h.name }));
  }).join('');
  if ((g = document.getElementById('grid-sets'))) g.innerHTML = SM.sets.map(function (s, i) {
    var a = [['pebble', 'body'], ['reach', 'mesh'], ['mini', 'soft'], ['easy', 'crease']][i];
    return card(s, draw({ handle: a[0], head: a[1], headCol: colourIds[(i + 1) % 6], handleCol: colourIds[(i + 1) % 6], label: s.name }));
  }).join('');
  if ((g = document.getElementById('swatches'))) g.innerHTML = SM.colours.map(function (c) {
    return '<span class="sw"><i style="background:' + (c.hex === 'rainbow' ? 'var(--rainbow)' : c.hex) + '"></i>' + esc(c.name) + '</span>';
  }).join('');

  /* ---------- hero line-up ---------- */
  if ((g = document.getElementById('hero-art'))) g.innerHTML =
    '<div class="h1a">' + draw({ handle: 'reach', head: 'body', headCol: 'yellow', handleCol: 'black', label: 'Reach Handle with Body Head' }) + '</div>' +
    '<div class="h2a">' + draw({ handle: 'pebble', head: 'face', headCol: 'pink', handleCol: 'pink', label: 'Pebble Grip with Face Head' }) + '</div>' +
    '<div class="h3a">' + draw({ handle: 'easy', head: 'scalp', headCol: 'blue', handleCol: 'white', label: 'Easy Grip with Scalp Head' }) + '</div>';

  /* ---------- builder ---------- */
  var b = document.getElementById('builder');
  if (b) {
    var st = { handle: 'reach', head: 'body', headCol: 'yellow', handleCol: 'black' };
    var chips = function (key, list, isCol) {
      return list.map(function (x) {
        return '<button type="button" class="chip' + (st[key] === x.id ? ' on' : '') + '" data-k="' + key + '" data-v="' + x.id + '">' +
          (isCol ? '<i style="background:' + (x.hex === 'rainbow' ? 'var(--rainbow)' : x.hex) + '"></i>' : '') + esc(x.name) + '</button>';
      }).join('');
    };
    var render = function () {
      var h = SM.handles.filter(function (x) { return x.id === st.handle; })[0];
      var hd = SM.heads.filter(function (x) { return x.id === st.head; })[0];
      b.innerHTML =
        '<div class="b-art">' + draw({ handle: st.handle, head: st.head, headCol: st.headCol, handleCol: st.handleCol, label: h.name + ' with ' + hd.name }) + '</div>' +
        '<div class="b-opts">' +
        ' <h3>' + esc(h.name) + ' + ' + esc(hd.name) + '</h3><p class="d">' + esc(h.desc) + ' ' + esc(hd.desc) + '</p>' +
        ' <div class="row"><b>1. Handle</b><div>' + chips('handle', SM.handles) + '</div></div>' +
        ' <div class="row"><b>2. Head</b><div>' + chips('head', SM.heads) + '</div></div>' +
        ' <div class="row"><b>3. Head colour</b><div>' + chips('headCol', SM.colours, true) + '</div></div>' +
        ' <div class="row"><b>4. Handle colour</b><div>' + chips('handleCol', SM.colours, true) + '</div></div>' +
        ' <div class="m">' + price(null) + '</div>' +
        '</div>';
    };
    b.addEventListener('click', function (e) {
      var t = e.target.closest('.chip'); if (!t) return;
      st[t.getAttribute('data-k')] = t.getAttribute('data-v'); render();
    });
    render();
  }

  /* ---------- join form (demo: opens an email until a real sign-up is wired in) ---------- */
  var f = document.getElementById('join-form');
  if (f) f.addEventListener('submit', function (e) {
    e.preventDefault();
    var em = f.querySelector('[name=email]').value;
    location.href = 'mailto:' + S.email + '?subject=' + encodeURIComponent('Scrubmello launch list') + '&body=' + encodeURIComponent('Please add me to the launch list: ' + em);
  });

  /* ---------- FAQ ---------- */
  document.querySelectorAll('.faq button').forEach(function (q) {
    q.addEventListener('click', function () { q.parentNode.classList.toggle('open'); });
  });
})();
