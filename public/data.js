/* Scrubmello product list. Prices are left empty (null) until they are decided.
   When a price is null the site shows "Price coming soon". */
window.SM = {
  site: {
    name: 'Scrubmello',
    tagline: 'One handle. Every head. Every body.',
    note: 'Launching soon. Join the list to hear first.',
    email: 'hello@scrubmello.co.uk',
    underConstruction: true
  },

  colours: [
    { id: 'pink',    name: 'Blush Pink',   hex: '#f4b9c8' },
    { id: 'blue',    name: 'Sky Blue',     hex: '#a9d3ee' },
    { id: 'black',   name: 'Charcoal',     hex: '#4a4a54' },
    { id: 'white',   name: 'Cloud White',  hex: '#f4f2ee' },
    { id: 'yellow',  name: 'Sunny Yellow', hex: '#f7e08c' },
    { id: 'rainbow', name: 'Rainbow',      hex: 'rainbow' }
  ],

  /* Handles all share the same Mello Click socket, so any head fits any handle. */
  handles: [
    { id: 'pebble', name: 'Pebble Grip',  desc: 'Short palm grip for everyday body washing. Fits in the hand like a smooth stone.', price: null },
    { id: 'reach',  name: 'Reach Handle', desc: 'Long, gently curved handle for your back and shoulders. Hang loop at the end.', price: null },
    { id: 'easy',   name: 'Easy Grip',    desc: 'Thick, soft, angled handle for weaker grip, arthritis or limited reach.', price: null },
    { id: 'mini',   name: 'Mini',         desc: 'Small, light handle sized for children\'s hands.', price: null }
  ],

  /* Heads all share the same egg shape so the range looks like one family. */
  heads: [
    { id: 'body',     name: 'Body Head',      tex: 'bristle', desc: 'Long silicone bristles that lather well and scrub deep.', price: null },
    { id: 'soft',     name: 'Soft Head',      tex: 'fine',    desc: 'Very fine, short bristles for sensitive skin.', price: null },
    { id: 'scalp',    name: 'Scalp Head',     tex: 'nub',     desc: 'Firm rounded nubs for bald heads, scalps and beards.', price: null },
    { id: 'face',     name: 'Face Head',      tex: 'face',    desc: 'Ultra-fine silicone on one side, a removable cleansing foam pad on the other.', price: null },
    { id: 'mesh',     name: 'Mesh Head',      tex: 'mesh',    desc: 'Puffy mesh for big lather with less scrub.', price: null },
    { id: 'cloth',    name: 'Mello Cloth',    tex: 'cloth',   desc: 'A soft fabric head that scrubs gently. The flannel, reinvented. Machine washable.', price: null },
    { id: 'crease',   name: 'Crease Head',    tex: 'crease',  desc: 'Slim, tapered and flexible for between skin folds and hard to reach places.', price: null },
    { id: 'intimate', name: 'Intimate Head',  tex: 'fine',    desc: 'Extra soft, colour-coded so it is never mixed up with the others.', price: null }
  ],

  sets: [
    { id: 'starter', name: 'Starter Set',  desc: 'Pebble Grip, Body Head, Soft Head, suction hook and screw hook.', price: null },
    { id: 'back',    name: 'Back Set',     desc: 'Reach Handle, Body Head, Mesh Head, suction hook and screw hook.', price: null },
    { id: 'family',  name: 'Family Set',   desc: 'Two Pebble Grips, a Reach Handle, a Mini and six heads in mixed colours.', price: null },
    { id: 'care',    name: 'Easy Care Set', desc: 'Easy Grip, Reach Handle, Crease Head, Soft Head and Mello Cloth.', price: null }
  ]
};
