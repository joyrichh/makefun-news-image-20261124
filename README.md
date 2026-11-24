# 24 November 2026 — World News in One Image

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/joyrichh/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/joyrichh/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Make.Fun competition entry ([`news-image-20261124`](https://make.fun/bounty/news-image-20261124)) by [@joyrichh](https://github.com/joyrichh).
A program that writes one image summing up the world's news of Tuesday,
24 November 2026, to `/output/entry.png`.

## The image

A 1024×1024 PNG infographic — "24 November 2026: the day's biggest stories,
in one image" — with six main stories and an "Also today" strip:

1. **Tech** — Nvidia brings back Jensen Huang as CEO.
   Eleven days after he resigned, Huang returns; Nvidia jumps a third,
   the Nasdaq rallies 6% and the S&P 500 4%.
2. **Ukraine** — Ukraine says its drones sank a Russian warship off Libya.
   Kyiv says seven naval drones sank the corvette Merkury at Benghazi,
   carrying the war into the Mediterranean.
3. **Climate** — COP31 collapses in Antalya over fossil fuels.
   After nearly 50 hours of overtime, 90+ nations reject a final text
   that never mentions fossil fuels.
4. **Asia** — Gas blast kills 6 at Hanoi food shop.
   An explosion at a crowded food shop in the Vietnamese capital injures 10;
   police blame cooking gas.
5. **Justice** — 14 nations back ICJ's Rohingya genocide ruling.
   The UK, Canada, Australia and 11 others acknowledge the verdict;
   London sanctions five Myanmar generals.
6. **Diplomacy** — Trump to meet NATO chief Rutte on Wednesday.
   The Florida talks follow Trump's meetings with Putin and Xi last week,
   with Ukraine peace on the agenda.

Also today:

- Sanofi to buy Insmed for $41bn in a Tuesday deal.
- Russian strike on Zaporizhzhia kills 2 and wounds 22, including two children.
- Sports court to rule today on Senegal's Africa Cup title appeal.

The stories were verified on 24 November 2026 against Reuters, Middle East
Eye, Grist and France 24 reporting and are retained in `news.json`. Sources credited in the image footer are Reuters,
Middle East Eye, Grist and France 24. The build performs no network requests.

## How it works

- `main.ts` (Node 22, standard library only) decodes the bundled
  `entry.png.b64`, checks the PNG magic bytes, and writes `/output/entry.png`.
  The base64 bundle keeps the entry suitable for plain UTF-8 repositories.
  No network, randomness or timestamps: repeated runs write identical bytes.
- `news.json` holds all six stories, three additional stories, date and sources.
- `build_image.py` renders the PNG using Pillow 10.2.0 and system DejaVu fonts.
  It measures every line, fits headlines to at most two lines and summaries
  to at most three, and asserts text stays within its containing bounds.
  No words are truncated. The finished PNG is encoded as `entry.png.b64`.
- `.makefun/owner.json` names the entry wallet for this account.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# out/entry.png — 1024x1024 PNG, 128,648 bytes
```

Rebuild the bundled image (Pillow 10.2.0 and DejaVu fonts required):

```sh
python3 build_image.py
base64 -w0 entry.png > entry.png.b64
```

Determinism check:

```sh
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 node main.ts
MAKEFUN_OUTPUT_DIR=out2 node main.ts
sha256sum out1/entry.png out2/entry.png   # identical hashes
```

## License

MIT — see `LICENSE`.
