# Making art with Codex

New art for this game comes from Codex image generation (`codex exec`, feature `image_generation`), not PixelLab. Codex draws big "pixel art" pictures (1000-1800 px); `scripts/pixelize.py` finds their pixel grid and turns them into the small sheets the game reads.

## Steps

1. Write a prompt file from a template below. Attach a style reference made from existing sprites (heroes and bugs side by side, enlarged 8x on a light grey background) and, for a new pose of an existing character, the character's earlier picture.
2. Run Codex in a scratch folder:

   ```sh
   codex exec -C <scratch> -s workspace-write --skip-git-repo-check -c model_reasoning_effort="medium" \
     -i ref/style.png [-i ref/<character>.png] -o last.txt - < prompt.txt
   ```

   It copies the generated PNG into `<scratch>/out/`. One picture takes about 1-3 minutes.
3. Convert:
   - character sheet: `python3 scripts/pixelize.py out/x_sheet.png sprites/x.png` (64px cells, feet on row 60)
   - card-art icon: `python3 scripts/pixelize.py out/x.png sprites/icons/x.png --canvas 64x48`
   - small pickups: `python3 scripts/pixelize.py out/props.png /tmp/props.png --each`, then rename each part to `sprites/props/<key>.png`
4. Look at the result enlarged before using it (`ffmpeg ... scale=iw*4:ih*4:flags=neighbor`).
5. Register it: a `SPRITES` entry with `auto: true` (rows are counted from the sheet), an `icon` on the weapon or passive, or the key in `PROP_ART`.
6. Keep the Codex original and its prompt in `art/codex/` so the asset can be reprocessed or regenerated.

## What the game expects

| Asset | File | Size | Notes |
|---|---|---|---|
| Hero or bug sheet | `sprites/<id>.png` | 64px cells | rows top to bottom: idle, attack, hit, walk; frames left-aligned; transparent; heroes face right, bugs face left |
| Weapon / passive icon | `sprites/icons/<icon>.png` | 64x48 | full-frame scene, no frame drawn inside; attack weapons on warm orange, defensive things on blue, food and team things on gold |
| Pickup or projectile | `sprites/props/<key>.png` | about 8-16 px | transparent, 1px dark outline; keys listed at `PROP_ART` in `index.html` |

Characters should read at about the size of the card game's sprites: the girl is ~40x57, the roach ~57x50, the gecko ~44x27 art pixels.

## Prompt rules that worked

- Name the art-pixel size and the figure size in art pixels ("about 44 art pixels long, 26 tall", "every art pixel is an exact square block of 4x4 image pixels"). Without that, Codex draws on a finer grid (the first gecko came out 68 px long).
- Ask for a whole sheet in one picture (rows of frames, clear space between frames). Frames drawn together stay consistent; separate pictures drift.
- "Fully transparent background, if impossible one flat pure magenta #FF00FF" — the converter handles both.
- "No text, no labels, no grid lines, no shadows, no border." Speech marks and impact lines are dropped by the converter when they are small and detached.
- Keep things the game draws itself out of the sprite (the gecko's long tongue, the spray mist).

## Template: character sheet

```
Make one pixel-art sprite sheet with your image generation tool and save it to a file. Do not write code for the art itself and do not touch anything outside this folder.

Character: <description, colours, distinguishing marks>. <If redrawing: "Keep the design of the first attached image exactly.">
The attached style image shows other sprites from the same game for style and scale.

Size: in every frame the whole character is about <W> art pixels wide and <H> tall. Clean 1-art-pixel near-black outline, 3-4 shades per colour, no anti-aliasing, no blur, no gradients.

Layout: <N> rows of frames, read left to right. Every frame faces <RIGHT for heroes / LEFT for bugs>, shows the full body, and is the same size. Leave at least 8 art pixels of empty space between frames and rows. Feet of all frames in a row sit on the same line.
- Row 1, idle, 4 frames: <...>
- Row 2, attack, 4 frames: <...>
- Row 3, hurt, 3 frames: <...>
- Row 4, walk, 6 frames: <...>

Render: every art pixel is an exact square block of 4x4 image pixels. Landscape image. Fully transparent background (if impossible, one flat pure magenta #FF00FF). No text, no labels, no grid lines, no shadows, no border.

Save as ./out/<id>_sheet.png. When done, reply with only the file path.
```

## Done with Codex

- `sprites/gecko.png`: idle 4 / attack 4 / hit 3 / walk 6 (`art/codex/gecko_sheet.*`)
- Icons and pickups made in the same session: see `sprites/README.md`
