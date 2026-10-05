# CLAUDE.md

Private inner-joke game for the owner and their wife: a Vampire Survivors–style run with the characters of the card game in `~/Documents/manoa-bug-squad`. The wife plays on a phone in portrait, so mobile portrait is the primary target; always check a 375px-wide viewport.

## Layout of the code

All code lives in `index.html` (vanilla HTML/CSS/JS, no build, no framework); pixel art lives in `sprites/`.

- `DATA` section at the top of the script: heroes, weapons (level steps + evolutions), passives, enemies, per-minute `WAVES`, timed `EVENTS`, XP curve. Balance changes go here.
- The world is one low-res canvas: 1 canvas px = 1 sprite px, about `VIEW_TARGET` px on the short side, scaled up with `image-rendering: pixelated`. `resize()` snaps the scale to whole device pixels when that is within 12%.
- Run state `S` is plain JSON (no `Infinity`, no class instances) so the artifact's hot-reload snapshot can hand it back; a restored run opens paused. Derived player stats live in `ST` (`recalc()`); the spatial grid and baked art live outside `S`.
- Fixed 60 Hz simulation (`update`) apart from `render`. Enemies sit in a 32px spatial hash (`buildGrid` / `near`); `near()` reuses one array, so never nest calls to it.
- Weapons: data in `WEAPONS[id]`, behaviour in `WB[id]`. Reaching level n adds `lv[n-2]`; evolving needs max level + the `evo.with` passive + a chest (elites and the 5:00 boss drop chests).
- Sprites: `SPRITES` in `DATA`, one sheet per unit, rows idle / attack / hit / walk, 64px cells unless `cell` / `base` say otherwise (`base` is the feet row, `cy` the body centre above it). `loadArt` bakes each sheet into plain / mirrored / white-flash canvases, plus tinted copies for bosses. Heroes face right and bugs face left in the art; the game mirrors them by movement. A unit without a sheet falls back to `fallback`, then to its emoji, so a new enemy can ship before its art.
- Drawn in code (`makePixelArt`): XP gems, spit, slipper, parasol, ground tile, props, damage digits. Emoji placeholders: pineapple / magnet / chest pickups and the 스팸 무스비 / 하얀 운동화 passives.
- Upgrade icons are the card game's card art, `sprites/icons/<id>.png` (64x48).

## Testing

- Local preview: `.claude/launch.json` serves this folder on :8124 (config `survivors`). file:// pages open as a `data:` snapshot in the browser pane, where relative `sprites/` URLs don't resolve.
- `window.__mbs` is a test hook: `__mbs.start('girl')`, `__mbs.DEBUG.god = true`, `__mbs.give('raid')`, `__mbs.chest()`. `__mbs.sim(60, S => [dx, dy])` runs a minute headless with a steering function and random level-up picks; it works while the browser pane is hidden (rAF does not), so use it for balance checks.

## Publishing

- The standalone page is `index.html` (works from file:// and GitHub Pages).
- The Claude artifact needs the page without the `<html>/<head>/<body>` wrapper: run `scripts/build-artifact.sh`, then publish `dist/artifact.html` with `url: https://claude.ai/artifact/DvVrra8fWqhNZAaaYu5q3B` to keep the same link. Pass every PNG under `sprites/` (including `sprites/icons/`) in `files` (published path = repo path) or the units and icons render blank / as emoji.
- Keep `<!-- artifact:start -->` / `<!-- artifact:end -->` markers and the `</head>` / `<body>` lines on their own lines; the build script depends on them.

## Art and PixelLab

- Sheets copied from the card game keep their rows; this project appended a walk row to `girl.png` / `alpaca.png` and added `flyroach`, `mosquito`, `snail`, `ant`. Prompts, seeds and frame picks are in `sprites/README.md`.
- PixelLab MCP is configured at local scope (`claude mcp add`, not `.mcp.json`) so the API token never lands in the repo. Never add a `.mcp.json` with the token. As of 2026-10-05 it is registered only for the card game folder; a session started here needs the owner to add it for this folder too (or at user scope).
- The owner's PixelLab account is a free trial shared with the card game: 40 generations, then 5 per day (stored up to 20), one job at a time. Check `get_balance` and say what a generation costs before spending.
