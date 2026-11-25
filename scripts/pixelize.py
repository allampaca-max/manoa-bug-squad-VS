#!/usr/bin/env python3
"""Turn a big "pixel art" picture (Codex image generation, ~1024-1500 px) into a game sprite sheet.

    python3 scripts/pixelize.py IN.png OUT.png [--cell 64] [--base 61] [--pitch 25.1] [--scale 1]
    python3 scripts/pixelize.py IN.png OUT.png --canvas 64x48     # a full-frame picture (card-art icon)
    python3 scripts/pixelize.py IN.png OUT.png --each              # every figure to OUT-1.png, OUT-2.png, ... (props)

- Finds the picture's own pixel grid (the size of one art pixel) and samples one colour per grid square,
  so the art stays crisp instead of being resampled.
- A transparent background is kept; an opaque one is keyed out by the most common border colour.
- Every separate figure becomes one frame. Figures are read in rows (top to bottom, left to right);
  each row of figures becomes one sheet row, in the order idle / attack / hit / walk.
- Each frame is centred in its cell with its lowest pixel on row base-1 (61 -> row 60), like the other sheets.

Needs ffmpeg on PATH. No Python packages.
"""
import argparse, subprocess, sys
from collections import Counter


def load(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                          '-of', 'csv=p=0', path], capture_output=True, text=True, check=True).stdout.strip().split(',')
    w, h = int(out[0]), int(out[1])
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'],
                         capture_output=True, check=True).stdout
    return w, h, raw


def save(path, w, h, buf):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{w}x{h}',
                    '-i', '-', '-pix_fmt', 'rgba', path], input=bytes(buf), check=True)


def key_background(w, h, px):
    """Opaque picture: make the dominant border colour (and anything close to it) transparent."""
    if any(px[i + 3] < 255 for i in range(3, len(px), 4 * 97)):
        return px
    border = Counter()
    for x in range(w):
        for y in (0, h - 1):
            i = (y * w + x) * 4
            border[(px[i] >> 4, px[i + 1] >> 4, px[i + 2] >> 4)] += 1
    br, bg, bb = [(c << 4) + 8 for c in border.most_common(1)[0][0]]
    out = bytearray(px)
    for i in range(0, len(out), 4):
        if abs(out[i] - br) + abs(out[i + 1] - bg) + abs(out[i + 2] - bb) < 60:
            out[i + 3] = 0
    return out


def same(px, i, j):
    a, b = px[i + 3] >= 128, px[j + 3] >= 128
    if a != b:
        return False
    return not a or abs(px[i] - px[j]) + abs(px[i + 1] - px[j + 1]) + abs(px[i + 2] - px[j + 2]) < 40


def runs_and_edges(w, h, px, horizontal):
    """Lengths of same-colour runs and how many colour edges sit at each position, along rows or columns."""
    n, m = (w, h) if horizontal else (h, w)
    runs, edges = [], [0] * (n + 1)
    for line in range(0, m, 2):
        start = 0
        for k in range(1, n):
            i = ((line * w + k) if horizontal else (k * w + line)) * 4
            j = ((line * w + k - 1) if horizontal else ((k - 1) * w + line)) * 4
            if not same(px, i, j):
                edges[k] += 1
                if start:
                    runs.append(k - start)
                start = k
    return runs, edges


def find_pitch(runs):
    """The art-pixel size: runs are whole multiples of it, so fit the smallest common step."""
    runs = [r for r in runs if r >= 4]
    if not runs:
        sys.exit('pixelize: no flat colour runs found; is this pixel art?')
    best, best_err = None, None
    lo = max(4, min(sorted(runs)[len(runs) // 20], 64))
    p = lo * 0.6
    while p <= lo * 1.6:
        err = sum(min(abs(r - round(r / p) * p), p / 2) for r in runs if round(r / p) >= 1) / len(runs) / p
        if best_err is None or err < best_err - 1e-4:
            best, best_err = p, err
        p += 0.02
    # refine: average of run / multiple for runs that are clean multiples
    fit = [r / round(r / best) for r in runs if round(r / best) >= 1 and abs(r - round(r / best) * best) < best * 0.2]
    return sum(fit) / len(fit) if fit else best


def find_offset(edges, pitch):
    best, best_score = 0.0, -1
    o = 0.0
    while o < pitch:
        score, k = 0, 0
        while o + k * pitch < len(edges) - 1:
            c = int(round(o + k * pitch))
            score += edges[c] + (edges[c - 1] + edges[c + 1]) * 0.5 if 0 < c < len(edges) - 1 else 0
            k += 1
        if score > best_score:
            best, best_score = o, score
        o += 0.25
    return best


def sample(w, h, px, pitch_x, off_x, pitch_y, off_y):
    """One colour per grid square: vote among the centre pixels, then average the winning colour."""
    gw, gh = int((w - off_x) // pitch_x), int((h - off_y) // pitch_y)
    out = bytearray(gw * gh * 4)
    for gy in range(gh):
        y0, y1 = off_y + gy * pitch_y, off_y + (gy + 1) * pitch_y
        for gx in range(gw):
            x0, x1 = off_x + gx * pitch_x, off_x + (gx + 1) * pitch_x
            votes, sums = Counter(), {}
            for y in range(int(y0 + (y1 - y0) * 0.25), int(y0 + (y1 - y0) * 0.75) + 1):
                for x in range(int(x0 + (x1 - x0) * 0.25), int(x0 + (x1 - x0) * 0.75) + 1):
                    if x >= w or y >= h:
                        continue
                    i = (y * w + x) * 4
                    if px[i + 3] < 128:
                        k = None
                    else:
                        k = (px[i] >> 3, px[i + 1] >> 3, px[i + 2] >> 3)
                        s = sums.setdefault(k, [0, 0, 0, 0])
                        s[0] += px[i]; s[1] += px[i + 1]; s[2] += px[i + 2]; s[3] += 1
                    votes[k] += 1
            if not votes:
                continue
            k = votes.most_common(1)[0][0]
            if k is None:
                continue
            s = sums[k]
            o = (gy * gw + gx) * 4
            out[o:o + 4] = bytes([s[0] // s[3], s[1] // s[3], s[2] // s[3], 255])
    return gw, gh, out


def figures(w, h, px):
    """Separate figures (8-connected, gaps of one pixel bridged), as lists of (x, y)."""
    seen = [False] * (w * h)
    opaque = lambda x, y: 0 <= x < w and 0 <= y < h and px[(y * w + x) * 4 + 3] > 0
    out = []
    for y in range(h):
        for x in range(w):
            if seen[y * w + x] or not opaque(x, y):
                continue
            stack, pts = [(x, y)], []
            seen[y * w + x] = True
            while stack:
                cx, cy = stack.pop()
                pts.append((cx, cy))
                for dy in (-2, -1, 0, 1, 2):
                    for dx in (-2, -1, 0, 1, 2):
                        nx, ny = cx + dx, cy + dy
                        if opaque(nx, ny) and not seen[ny * w + nx]:
                            seen[ny * w + nx] = True
                            stack.append((nx, ny))
            if len(pts) >= 12:          # ignore specks
                out.append(pts)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--cell', type=int, default=64)
    ap.add_argument('--base', type=int, default=61, help='feet row + 1, as in SPRITES (default 61)')
    ap.add_argument('--pitch', type=float, help='art-pixel size in the source, if detection picks wrong')
    ap.add_argument('--scale', type=int, default=1, help='repeat each art pixel N times (art drawn too small)')
    ap.add_argument('--canvas', help='WxH: keep the whole picture (no background keying) and fit it to exactly WxH')
    ap.add_argument('--each', action='store_true', help='write every figure to its own tightly cropped file')
    a = ap.parse_args()

    w, h, px = load(a.src)
    if not a.canvas:
        px = key_background(w, h, px)
    rx, ex = runs_and_edges(w, h, px, True)
    ry, ey = runs_and_edges(w, h, px, False)
    pitch = a.pitch or find_pitch(rx + ry)
    ox, oy = find_offset(ex, pitch), find_offset(ey, pitch)
    gw, gh, small = sample(w, h, px, pitch, ox, pitch, oy)
    print(f'pixelize: {w}x{h} source, art pixel {pitch:.2f}px -> {gw}x{gh} grid', file=sys.stderr)

    if a.canvas:
        # nearest-neighbour fit of the sampled grid to the exact size (absorbs a row or column of drift)
        W, H = (int(v) for v in a.canvas.lower().split('x'))
        out = bytearray(W * H * 4)
        for y in range(H):
            for x in range(W):
                i = ((y * gh // H) * gw + x * gw // W) * 4
                o = (y * W + x) * 4
                out[o:o + 3] = small[i:i + 3]
                out[o + 3] = 255
        save(a.dst, W, H, out)
        print(f'pixelize: wrote {a.dst} ({W}x{H} from a {gw}x{gh} grid)', file=sys.stderr)
        return

    figs = figures(gw, gh, small)
    if not figs:
        sys.exit('pixelize: nothing opaque found')
    if a.each:
        stem = a.dst[:-4] if a.dst.endswith('.png') else a.dst
        for n, f in enumerate(sorted(figs, key=lambda f: min(p[0] for p in f)), 1):
            x0, y0 = min(p[0] for p in f), min(p[1] for p in f)
            fw, fh = max(p[0] for p in f) - x0 + 1, max(p[1] for p in f) - y0 + 1
            out = bytearray(fw * fh * 4)
            for (x, y) in f:
                o = ((y - y0) * fw + x - x0) * 4
                out[o:o + 4] = small[(y * gw + x) * 4:(y * gw + x) * 4 + 4]
            save(f'{stem}-{n}.png', fw, fh, out)
            print(f'pixelize: wrote {stem}-{n}.png ({fw}x{fh})', file=sys.stderr)
        return
    # rows of figures by vertical centre
    figs.sort(key=lambda f: sum(p[1] for p in f) / len(f))
    hmed = sorted(max(p[1] for p in f) - min(p[1] for p in f) + 1 for f in figs)[len(figs) // 2]
    rows = []
    for f in figs:
        cy = sum(p[1] for p in f) / len(f)
        if rows and abs(cy - rows[-1][0]) < hmed / 2:
            rows[-1][1].append(f)
        else:
            rows.append([cy, [f]])
    rows = [sorted(r[1], key=lambda f: min(p[0] for p in f)) for r in rows]

    s, C = a.scale, a.cell
    cols = max(len(r) for r in rows)
    W, H = cols * C, len(rows) * C
    out = bytearray(W * H * 4)
    for ri, row in enumerate(rows):
        for ci, f in enumerate(row):
            x0, x1 = min(p[0] for p in f), max(p[0] for p in f)
            y0, y1 = min(p[1] for p in f), max(p[1] for p in f)
            fw, fh = (x1 - x0 + 1) * s, (y1 - y0 + 1) * s
            if fw > C or fh > a.base:
                sys.exit(f'pixelize: frame {ri},{ci} is {fw}x{fh}, too big for a {C}px cell with base {a.base}')
            dx = ci * C + (C - fw) // 2
            dy = ri * C + a.base - fh
            for (x, y) in f:
                i = (y * gw + x) * 4
                for sy in range(s):
                    for sx in range(s):
                        o = ((dy + (y - y0) * s + sy) * W + dx + (x - x0) * s + sx) * 4
                        out[o:o + 4] = small[i:i + 4]
            print(f'  row {ri} frame {ci}: {fw}x{fh}', file=sys.stderr)
    save(a.dst, W, H, out)
    print(f'pixelize: wrote {a.dst} ({W}x{H}, {len(rows)} row(s), up to {cols} frame(s))', file=sys.stderr)


if __name__ == '__main__':
    main()
