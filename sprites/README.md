# Sprites

PixelLab output, one sheet per unit, unique frames only. Play order, cell size and feet row are in `SPRITES` in `index.html`.

| Sheet | Cell | Rows (frames) | Notes |
|---|---|---|---|
| `girl.png` | 64 | idle 4 / attack 6 / hit 5 / walk 8 | first three rows from the card game; walk added here |
| `alpaca.png` | 64 | idle 5 / attack 5 / hit 5 / walk 8 | same; the walk blinks on two frames |
| `centipede.png` | 64 | 5 / 7 / 5 | card game, unchanged (also the red 2x boss 왕지네) |
| `roach.png` | 64 | 5 / 7 / 5 | card game, unchanged |
| `flyroach.png` | 64 | idle 7 | flying loop; also the purple 2x final boss 바퀴벌레 대왕 |
| `mosquito.png` | 48 | idle 3 | wing buzz, played 0-1-2-1 |
| `snail.png` | 64 | idle 1 | single frame; the game stretches it to crawl |
| `ant.png` | 32 | idle 1 | single frame; the game bobs it |
| `mist.png` | 64x32 | | card game spray cloud, drawn rotated toward the target |
| `icons/<id>.png` | 64x48 | | the card game's card art, reused as weapon / passive icons |

For the card game sheets (base prompts, how the rows were made) see `sprites/README.md` in `~/Documents/manoa-bug-squad`.

## Made for this game

All seed 7, transparent background. Style flags for new bugs match the card game: `create_image_pixen`, `view: side`, `direction: west`, `outline: single color black outline`, `detail: medium detail`.

- **Walk rows** (`animate_image`, 8 frames, unpinned, from frame 0 of the sheet). Frames 1-8 loop; frame 0 is the input and is dropped.
  - girl: walking to the right in place, side view walk cycle, legs stepping alternately, long hair bouncing gently with each step
  - alpaca: walking to the right in place, side view walk cycle, short legs stepping alternately, fluffy wool body bouncing with each step
- **flyroach** (`animate_image` from roach frame 0, 8 frames): the cockroach opens its shell and spreads its brown wings, then flies hovering in place with wings flapping fast, legs dangling. Kept frames 2-8 (wings open). The model dropped the big cartoon eyes, which suits the elite.
- **mosquito** (48x48): cute chibi pixel art mosquito monster, small dark gray body with white stripes, thin long legs, big round cartoon eyes, long thin needle nose, clear light blue wings, flying, full body, side view facing left, 16-bit retro game enemy sprite. Then `animate_image`, 4 frames: hovering in place, wings flapping very fast, body bobbing slightly up and down. Kept frames 0, 1, 3 (the others lost the pupils).
- **snail** (64x64): asked for a slug ("cute chibi pixel art slug monster, slimy soft yellowish brown body with darker spots, two eye stalks with big round cartoon eyes, glossy wet highlights, crawling low on the ground, …"); it drew a snail with a shell, so the enemy became 달팽이.
- **ant** (32x32): cute chibi pixel art ant monster, small shiny dark red brown body with three round segments, big round cartoon eyes, two antennae, six thin legs, walking, full body, side view facing left, 16-bit retro game enemy sprite

Total: 7 generations (2 walks, flyroach, mosquito base + buzz, snail, ant). With the card game's 31 that is 38 of the trial's 40.

## Still placeholders (next art to make)

- Pickups: pineapple 🍍 (heal), magnet 🧲, treasure chest 🎁
- Passives without card art: 스팸 무스비 🍙, 하얀 운동화 👟
- Projectiles drawn in code that could become real sprites: slipper, parasol (top view), spit glob, raid explosion
- Optional: hit rows for the new bugs, a snail / ant walk, a ground tileset (`create_topdown_tileset`)
