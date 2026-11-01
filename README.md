<p align="center"><img src="public/img/hero.webp" alt="The Scrubmello range" width="100%"></p>

<h1 align="center">scrubmello</h1>
<p align="center"><b>One handle. Every head. Every body.</b><br>Interchangeable scrubbers for body, back, face and scalp. Launching soon.</p>
<p align="center"><a href="https://bhxuk.github.io/Scrubmello/"><b>View the landing page →</b></a></p>

---

## The Mello Click system
Every handle and every head share one click collar, so any head fits any handle. Keep the handle, replace the head.

<p align="center"><img src="public/img/click.webp" alt="A head clicking onto a Pebble Grip" width="80%"></p>

## Handles
Slim (under an inch wide), soft-touch silicone, with clear frosted details and a hang loop on every one.

| Pebble Grip | Reach Handle | Easy Grip | Mini |
|:-:|:-:|:-:|:-:|
| <img src="public/img/handle-pebble.webp" width="200"> | <img src="public/img/handle-reach.webp" width="200"> | <img src="public/img/handle-easy.webp" width="200"> | <img src="public/img/handle-mini.webp" width="200"> |
| 23mm · 112mm | 14 to 19mm · 400mm | up to 25mm · 170mm | 13mm · 60mm |

## Heads
One egg shape (72 x 88mm), eight textures.

| Body | Soft | Scalp | Face |
|:-:|:-:|:-:|:-:|
| <img src="public/img/head-body.webp" width="200"> | <img src="public/img/head-soft.webp" width="200"> | <img src="public/img/head-scalp.webp" width="200"> | <img src="public/img/head-face.webp" width="200"> |
| **Mesh** | **Cloth** | **Crease** | **Intimate** |
| <img src="public/img/head-mesh.webp" width="200"> | <img src="public/img/head-cloth.webp" width="200"> | <img src="public/img/head-crease.webp" width="200"> | <img src="public/img/head-intimate.webp" width="200"> |

## Colours
Blush, Sky, Butter, Charcoal, Cloud and Rainbow, plus Mint and Lilac.

<p align="center"><img src="public/img/colours.webp" alt="Colourways" width="100%"></p>

---

## About this repo
- `public/` the website: `index.html`, `styles.css`, `app.js`, and `data.js` (**products, sizes and prices**; a `null` price shows "Price coming soon")
- `public/img/` product renders
- `design/` the 3D model and render script for the whole range (Blender). Run `python design/sm.py all` with the `bpy` package to re-render
- `CHANGELOG.md` every change, request by request
- `.github/workflows/pages.yml` publishes `public/` to GitHub Pages on every push to `main`

**Turning on the landing page:** repo Settings > Pages > Source: **GitHub Actions**. It then lives at https://bhxuk.github.io/Scrubmello/.
