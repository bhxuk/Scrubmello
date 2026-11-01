/* Scrubmello product list. Prices are left empty (null) until they are decided.
   When a price is null the site shows "Price coming soon".
   Sizes come from the 3D design models. */
window.SM = {
  site: {
    name: 'Scrubmello',
    tagline: 'One handle. Every head. Every body.',
    note: 'Launching soon. Join the list to hear first.',
    email: 'hello@scrubmello.co.uk',
    underConstruction: true
  },

  colours: [
    { id: 'pink',    name: 'Blush',    hex: '#f4b9c8' },
    { id: 'blue',    name: 'Sky',      hex: '#a9d3ee' },
    { id: 'yellow',  name: 'Butter',   hex: '#f7e08c' },
    { id: 'black',   name: 'Charcoal', hex: '#4a4a54' },
    { id: 'white',   name: 'Cloud',    hex: '#f2f0ec' },
    { id: 'rainbow', name: 'Rainbow',  hex: 'rainbow' },
    { id: 'mint',    name: 'Mint',     hex: '#bfe5c7' },
    { id: 'lilac',   name: 'Lilac',    hex: '#cfc2ef' }
  ],

  /* Handles all share the Mello Click collar, so any head fits any handle. */
  handles: [
    { id: 'pebble', name: 'Pebble Grip',  img: 'img/handle-pebble.webp', spec: '23mm wide · 112mm long', desc: 'Short palm grip for everyday washing, with a clear frosted thumb window and hang tab.', price: null },
    { id: 'reach',  name: 'Reach Handle', img: 'img/handle-reach.webp',  spec: '14 to 19mm wide · 400mm long', desc: 'Long, gently curved back handle. A clear shaft shows the coloured spine inside.', price: null },
    { id: 'easy',   name: 'Easy Grip',    img: 'img/handle-easy.webp',   spec: 'Up to 25mm wide · 170mm long', desc: 'Angled grip with soft clear rings, for arthritis, weaker grip or limited reach.', price: null },
    { id: 'mini',   name: 'Mini',         img: 'img/handle-mini.webp',   spec: '13mm wide · 60mm long', desc: 'Small and light, sized for children\'s hands.', price: null }
  ],

  /* Heads all share one egg shape (72 x 88mm) so the range looks like one family. */
  heads: [
    { id: 'body',     name: 'Body',     img: 'img/head-body.webp',     spec: 'Long silicone bristles', desc: 'Lathers well and scrubs deep.', price: null },
    { id: 'soft',     name: 'Soft',     img: 'img/head-soft.webp',     spec: 'Short, fine bristles', desc: 'Gentle on sensitive skin.', price: null },
    { id: 'scalp',    name: 'Scalp',    img: 'img/head-scalp.webp',    spec: 'Firm rounded nubs', desc: 'For bald heads, scalps and beards.', price: null },
    { id: 'face',     name: 'Face',     img: 'img/head-face.webp',     spec: 'Ultra-fine silicone', desc: 'Soft enough for faces, with a cleansing foam pad to swap in.', price: null },
    { id: 'mesh',     name: 'Mesh',     img: 'img/head-mesh.webp',     spec: 'Layered net pouf', desc: 'Big lather, light scrub.', price: null },
    { id: 'cloth',    name: 'Cloth',    img: 'img/head-cloth.webp',    spec: 'Waffle-weave fabric', desc: 'The flannel, reinvented. Machine washable.', price: null },
    { id: 'crease',   name: 'Crease',   img: 'img/head-crease.webp',   spec: 'Slim 38mm flexible paddle', desc: 'Gets gently between skin folds.', price: null },
    { id: 'intimate', name: 'Intimate', img: 'img/head-intimate.webp', spec: 'Smooth rippled silicone', desc: 'Extra soft and always lilac, so it never gets mixed up.', price: null }
  ],

  sets: [
    { id: 'starter', name: 'Starter Set',   img: 'img/set-starter.webp', desc: 'Pebble Grip, Body and Soft heads, suction hook and screw hook.', price: null },
    { id: 'back',    name: 'Back Set',      img: 'img/set-back.webp',    desc: 'Reach Handle, Body and Mesh heads, suction hook and screw hook.', price: null },
    { id: 'family',  name: 'Family Set',    img: 'img/set-family.webp',  desc: 'Two Pebble Grips, a Reach Handle and a Mini, in mixed colours.', price: null },
    { id: 'care',    name: 'Easy Care Set', img: 'img/set-care.webp',    desc: 'Easy Grip, Reach Handle, Crease, Soft and Cloth heads.', price: null }
  ]
};
