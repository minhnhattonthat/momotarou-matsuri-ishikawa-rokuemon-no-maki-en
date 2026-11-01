# Fonts

Every font or glyph sheet the build reads ends up inside the released patch, so its licence must allow that. One row
per file; a font with no known licence doesn't go into a release.

| File | Source (URL, version) | Licence | Redistributable in a patch | Used for | Changes made |
|---|---|---|---|---|---|
| fonts/en12.txt | the owner's GaiaMaster translation (github.com/minhnhattonthat/gaiamaster-kamigami-no-board-game-en), via the sibling repo ../momotarou-densetsu-en | MIT, same owner | yes | dialogue/menu VWF glyphs in FONT0D page 1 (tools/engine.py) | - |
| fonts/hud7.txt | hand-drawn in this project, 2026-11-01 | MIT (repository LICENSE) | yes | small M990D HUD word sprites and costume initials | 7-pixel capitals, added K/P for card emblems and F for Fortune God's badge; no antialiasing |
| fonts/credits7.txt | hand-drawn in this project, 2026-11-01 | MIT (repository LICENSE) | yes | EVT600D credits, long Card Album region names, narrow HUD labels, Streak, Which?, M06 speech bubbles, M23 race names/labels and small sign labels/prices | condensed 7-pixel capitals and added digits 0-4; no antialiasing; Games boards use exact 2x nearest-neighbour scaling |
| fonts/ofl/Fredoka.ttf | github.com/google/fonts ofl/fredoka (variable wdth,wght), fetched 2026-11-01 | SIL OFL 1.1 (fonts/ofl/Fredoka-OFL.txt) | yes (pixels drawn from it ship in the patch) | graphics-text redraws (tools/gen_gfx.py) | - |
| tools/gfx_intro.py numeral 6 | hand-drawn in this project, 2026-11-01 | MIT (repository LICENSE) | yes | Rokuemon's coat badges in the attract portrait | nearest-neighbour scale/rotation within original badges; fan words use fonts/credits7.txt |
| tools/gfx_tanuki_bibs.py initial K | hand-drawn in this project, 2026-11-02 | MIT (repository LICENSE) | yes | Kintaro's eight Even Tanuki bib cells | 4x5 pixels; distinct diagonals below eating-pose hands; no antialiasing |
