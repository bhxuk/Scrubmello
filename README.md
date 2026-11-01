# Scrubmello website

One handle. Every head. Every body.

Scrubmello is a range of interchangeable scrubbers: handles and click-on heads for body, back, face, scalp, sensitive skin and skin folds, in soft pastel colours. This repo holds the brand's landing page.

## Layout
- `public/` everything that goes on the web host
  - `index.html` home: hero, How it works, Build yours, Handles, Heads, Colours, Sets, Made for every body, FAQ, Launch list
  - `data.js` **products, colours and prices**. Prices are `null` until decided, which shows "Price coming soon"
  - `app.js` header, footer, product drawings, the Build yours tool and product cards
  - `styles.css` styling (relaxed, modern, soft pastels)
  - `favicon.svg`
- `CHANGELOG.md` every change, request by request
- `.github/workflows/pages.yml` publishes `public/` to GitHub Pages as a preview

## Product drawings
The products are drawn in code (SVG) from shared parts, so the whole range always looks like one family: an egg-shaped head, the Mello Click socket and one of four handles (Pebble Grip, Reach Handle, Easy Grip, Mini). These are placeholders until real product renders or photos exist.

## Turning on the preview
Repo Settings > Pages > Source: **GitHub Actions**. The site then publishes on every push to `main`.
