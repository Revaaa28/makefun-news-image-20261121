# The World in One Day — Saturday, 21 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Revaaa28/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Revaaa28/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

One image that sums up a day of world news, drawn as a broadsheet front
page: a dotted world map with a numbered pin for every story, a hero
story with a large illustrated scene, and five more stories — each with
its own pictorial vignette, place label, headline and one-line summary —
plus an "Also today" ticker.

The six stories: Russian missiles fall in Poland · Trump, Xi and Putin
end the first trilateral summit in Shenzhen · AI sell-off tips Wall
Street into correction · Sudan's army says RSF strongholds in West
Kordofan are broken · 10,000 Rohingya to resettle in Türkiye under a
Malaysian deal · a record Indian opening stand in Wellington.

## How it works

- `entry.png` — the rendered front page (1024×1024), shipped in the repo
  as the rules allow.
- `main.py` — the graded program (Python 3.13, standard library only).
  It validates the shipped PNG (signature, chunk CRCs, dimensions, 1 MiB
  cap) and copies it to `/output/entry.png` (or
  `$MAKEFUN_OUTPUT_DIR/entry.png`), verifying the byte count.
- `build.py` — the local build tool that rendered `entry.png` with
  Pillow. The grader never runs it; it is kept for transparency.
- `SOURCES.md` — the reporting each story was checked against, and the
  attribution choices behind the wording.

## License

MIT — see `LICENSE`.
