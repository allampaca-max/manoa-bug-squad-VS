# Sprites

PixelLab and Codex output, one sheet per unit, unique frames only. Play order, cell size and feet row are in `SPRITES` in `index.html`.

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
| `gecko.png` | 64 | idle 4 / attack 4 / hit 3 / walk 6 | Codex; rows counted from the sheet (`auto: true`) |
| `silverfish.png` `moth.png` `termite.png` | 64 | idle 4 | Codex, sampled at half size (see below) |
| `caneSpider.png` `termiteQueen.png` | 96 | idle 4 | Codex at full size; the 5:00 boss is the spider at 2x, the queen is drawn at 2x |
| `fruitFly.png` | 32 | idle 4 | Codex, sampled at half size |
| `ensignWasp.png` | 64 | idle 4 | Codex, half size (깃대벌: Codex read "flag" literally and gave it a little flag) |
| `ensignWaspBig.png` `antQueen.png` | 96 | idle 4 | Codex at full size: the 5:00 boss 대왕 깃대벌 (drawn at 1.3x) and the final boss 여왕개미 (1.5x) |
| `mist.png` | 64x32 | | card game spray cloud, drawn rotated toward the target |
| `icons/<id>.png` | 64x48 | | the card game's card art, reused as weapon / passive icons; `tongue`, `egg`, `musubi`, `sneakers`, `swatter`, `footShampoo`, `chopsticks`, `waterJug` are Codex |
| `props/<key>.png` | ~16 | | Codex pickups: `heal` (pineapple), `magnet`, `chest`, `coin` (also the coin glyph in menus); laundry obstacles `washer`, `dryer`, `basket`, `bottle`, kitchen obstacles `riceCooker`, `trashCan`, `riceSack`, `kimchi` (drawn at 2x); `jug` (the water-jug trap, drawn at 1.5x); listed in `PROP_ART` |

For the card game sheets (base prompts, how the rows were made) see `sprites/README.md` in `~/Documents/manoa-bug-squad`.

## Made for this game with PixelLab

All seed 7, transparent background. Style flags for new bugs match the card game: `create_image_pixen`, `view: side`, `direction: west`, `outline: single color black outline`, `detail: medium detail`.

- **Walk rows** (`animate_image`, 8 frames, unpinned, from frame 0 of the sheet). Frames 1-8 loop; frame 0 is the input and is dropped.
  - girl: walking to the right in place, side view walk cycle, legs stepping alternately, long hair bouncing gently with each step
  - alpaca: walking to the right in place, side view walk cycle, short legs stepping alternately, fluffy wool body bouncing with each step
- **flyroach** (`animate_image` from roach frame 0, 8 frames): the cockroach opens its shell and spreads its brown wings, then flies hovering in place with wings flapping fast, legs dangling. Kept frames 2-8 (wings open). The model dropped the big cartoon eyes, which suits the elite.
- **mosquito** (48x48): cute chibi pixel art mosquito monster, small dark gray body with white stripes, thin long legs, big round cartoon eyes, long thin needle nose, clear light blue wings, flying, full body, side view facing left, 16-bit retro game enemy sprite. Then `animate_image`, 4 frames: hovering in place, wings flapping very fast, body bobbing slightly up and down. Kept frames 0, 1, 3 (the others lost the pupils).
- **snail** (64x64): asked for a slug ("cute chibi pixel art slug monster, slimy soft yellowish brown body with darker spots, two eye stalks with big round cartoon eyes, glossy wet highlights, crawling low on the ground, …"); it drew a snail with a shell, so the enemy became 달팽이.
- **ant** (32x32): cute chibi pixel art ant monster, small shiny dark red brown body with three round segments, big round cartoon eyes, two antennae, six thin legs, walking, full body, side view facing left, 16-bit retro game enemy sprite

Total: 7 generations (2 walks, flyroach, mosquito base + buzz, snail, ant). With the card game's 31 that is 38 of the trial's 40.

## Made for this game with Codex

Procedure, prompt rules and templates: `art/CODEX.md`. Originals and the exact prompts are in `art/codex/`.

- **gecko** (2026-11-24): first a single base picture (gold dust day gecko, side view facing right) for the design; it came out 68 px long, so Codex redrew it as a whole sheet at ~44x26 art pixels with the first picture attached as the design reference (`art/codex/gecko_sheet.*`). Converted with `scripts/pixelize.py` (art pixel 6.0 px → 17 frames, the hurt frame's impact lines dropped as specks).
- **icons** `tongue`, `egg`, `musubi`, `sneakers` and **props** `heal`, `magnet`, `chest`: one Codex session with the card art attached as the style reference (`art/codex/icons/`). Converted with `--canvas 64x48` and `--each`.

- **laundry bugs** (`art/codex/laundry/`): one sheet, five rows of four frames, facing left. Codex drew them 1.7-2x bigger than asked (silverfish 69 px), so `silverfish`, `moth`, `termite` were converted with `--pitch 8` (half size, some detail lost) and `caneSpider`, `termiteQueen` at full size with `--cell 96 --base 93`; rows cut into one sheet each with ffmpeg.
- **laundry props**: washer, dryer, basket, bottle from one picture, `--each`.
- **kitchen** (`art/codex/kitchen/`, two Codex sessions): a bug sheet (fruit fly, ensign wasp, queen ant; drawn ~2x too big, so the fly and wasp were sampled at `--pitch 9.26` and the big wasp and queen kept at full size in 96px cells), four props (`--each`, sampled at 1.5x pitch except the trash can), the coin and the water jug (`--each --pitch 40.18`), and four card icons (`--canvas 64x48`).

## Still placeholders (next art to make)

- Projectiles drawn in code that could become real sprites: slipper, parasol (top view), spit glob, raid explosion
- Optional: hit rows for the new bugs, a snail / ant walk, a ground tileset (`create_topdown_tileset`)
