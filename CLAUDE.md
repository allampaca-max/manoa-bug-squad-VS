# CLAUDE.md

Private inner-joke game for the owner and their wife: a Vampire Survivors–style run with the characters of the card game in `~/Documents/manoa-bug-squad`, plus the green gecko that lives in their laundry room. The wife plays on a phone in portrait, so mobile portrait is the primary target; always check a 375px-wide viewport.

## Layout of the code

All code lives in `index.html` (vanilla HTML/CSS/JS, no build, no framework); pixel art lives in `sprites/`.

- `DATA` section at the top of the script: heroes, weapons (level steps + evolutions), passives, enemies, per-minute `WAVES`, timed `EVENTS`, `STAGES` (each stage's waves, events, ground tile in `TILES`; `ready: false` shows a locked card), XP curve. Balance changes go here.
- The world is one low-res canvas: 1 canvas px = 1 sprite px, about `VIEW_TARGET` px on the short side, scaled up with `image-rendering: pixelated`. `resize()` snaps the scale to whole device pixels when that is within 12%.
- Run state `S` is plain JSON (no `Infinity`, no class instances) so the artifact's hot-reload snapshot can hand it back; a restored run opens paused. Derived player stats live in `ST` (`recalc()`); the spatial grid and baked art live outside `S`.
- Two overlay layers: `#menu` holds the screens outside a run (`showMain` / `showHeroes` / `showStages` / `showRecords` / `showSettings`; the main screen's background parade is `drawParade`), `#modal` holds the in-run panels (level up, chest, pause, results). Both route `data-act` buttons through `act()`. Last picked hero and stage: localStorage `mbs.last`; records: `mbs.records[stage][hero]` (best run) and `mbs.stats` (totals), written by `saveRecord()`; the old per-hero `mbs.best` is folded in by `migrateRecords()`.
- Fixed 60 Hz simulation (`update`) apart from `render`. Enemies sit in a 32px spatial hash (`buildGrid` / `near`); `near()` reuses one array, so never nest calls to it.
- Weapons: data in `WEAPONS[id]`, behaviour in `WB[id]`. Reaching level n adds `lv[n-2]`; evolving needs max level + the `evo.with` passive + a chest (elites and the 5:00 boss drop chests).
- Sprites: `SPRITES` in `DATA`, one sheet per unit, rows idle / attack / hit / walk, 64px cells unless `cell` / `base` say otherwise (`base` is the feet row, `cy` the body centre above it). `loadArt` bakes each sheet into plain / mirrored / white-flash canvases, plus tinted copies for bosses. Heroes face right and bugs face left in the art; the game mirrors them by movement. A unit without a sheet falls back to `fallback`, then to its emoji, so a new enemy can ship before its art.
- Drawn in code (`makePixelArt`): XP gems, spit, slipper, parasol, ground tile, ground props, damage digits. A key listed in `PROP_ART` swaps the code-drawn prop or emoji pickup for `sprites/props/<key>.png`.
- Upgrade icons are 64x48 pictures in `sprites/icons/<icon>.png` (card game art plus Codex art). The icon `<img>` sits over the item's emoji and removes itself if the file is missing.
- Heroes have an `emoji` too: `heroArt()` uses it until the hero has a sheet. `tail: true` (gecko) survives one knockout via `dropTail()`: half HP, 2.5 s of `inv`, and enemies chase `S.decoy` for 3 s.

- Sound is synthesised with WebAudio in the SOUND section, no audio files. `sfx(name)` plays an entry of `SFX` (each has a `gap` throttle and a `vol`); `music(name)` picks a song from `SONGS` (8th-note steps, one chord per bar) that a lookahead sequencer (`musicTick`, 25 ms) plays; `frame()` chooses title / battle / boss and ducks it under menus. Nothing sounds until `audioInit()` runs from a tap (`act()` or the joystick). Settings live in localStorage `mbs.audio`. Levels were set by rendering offline and measuring peaks (music ~0.38, weapons 0.2-0.3, fanfares ~0.4); nobody has listened critically yet.

## Testing

- Local preview: `.claude/launch.json` serves this folder on :8124 (config `survivors`). file:// pages open as a `data:` snapshot in the browser pane, where relative `sprites/` URLs don't resolve.
- `window.__mbs` is a test hook: `__mbs.start('girl', 'backyard')`, `__mbs.freeze(6.6)` (stops the menu animation at a moment, for screenshots), `__mbs.DEBUG.god = true`, `__mbs.give('raid')`, `__mbs.chest()`. `__mbs.audio` exposes the sound internals for offline rendering. `__mbs.sim(60, S => [dx, dy])` runs a minute headless (silently) with a steering function and random level-up picks; it works while the browser pane is hidden (rAF does not), so use it for balance checks.

## Publishing

- The standalone page is `index.html` (works from file:// and GitHub Pages).
- The Claude artifact needs the page without the `<html>/<head>/<body>` wrapper: run `scripts/build-artifact.sh`, then publish `dist/artifact.html` with `url: https://claude.ai/artifact/DvVrra8fWqhNZAaaYu5q3B` to keep the same link. Pass every PNG under `sprites/` (including `sprites/icons/`) in `files` (published path = repo path) or the units and icons render blank / as emoji.
- Keep `<!-- artifact:start -->` / `<!-- artifact:end -->` markers and the `</head>` / `<body>` lines on their own lines; the build script depends on them.

## Art

- New art comes from Codex image generation (`codex exec`, installed and logged in on the owner's Mac), converted with `scripts/pixelize.py`. The whole procedure, prompt rules and templates are in `art/CODEX.md`; Codex originals and prompts go in `art/codex/`.
- Sheets copied from the card game keep their rows; this project appended a walk row to `girl.png` / `alpaca.png` and added `flyroach`, `mosquito`, `snail`, `ant` (PixelLab) and `gecko` (Codex). Provenance per file is in `sprites/README.md`.
- PixelLab MCP is configured at local scope (`claude mcp add`, not `.mcp.json`) so the API token never lands in the repo. Never add a `.mcp.json` with the token. As of 2026-10-05 it is registered only for the card game folder; a session started here needs the owner to add it for this folder too (or at user scope).
- PixelLab is no longer the main source (owner's choice, 2026-11). Its account is a free trial shared with the card game: 40 generations, then 5 per day (stored up to 20), one job at a time. Check `get_balance` and say what a generation costs before spending.
