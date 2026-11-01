# Fonts

Every font or glyph sheet the build reads ends up inside the released patch, so its licence must allow that. One row
per file; a font with no known licence doesn't go into a release.

| File | Source (URL, version) | Licence | Redistributable in a patch | Used for | Changes made |
|---|---|---|---|---|---|
| fonts/en12.txt | the owner's GaiaMaster translation (github.com/minhnhattonthat/gaiamaster-kamigami-no-board-game-en), via the sibling repo ../momotarou-densetsu-en | MIT, same owner | yes | dialogue/menu VWF glyphs in FONT0D page 1 (tools/engine.py) | - |
| fonts/hud7.txt | hand-drawn in this project, 2026-11-01 | MIT (repository LICENSE) | yes | small M990D HUD word sprites | 7-pixel capitals; no antialiasing |
| fonts/credits7.txt | hand-drawn in this project, 2026-11-01 | MIT (repository LICENSE) | yes | EVT600D credit sprites | condensed 7-pixel capitals; no antialiasing or resampling |
| fonts/ofl/Fredoka.ttf | github.com/google/fonts ofl/fredoka (variable wdth,wght), fetched 2026-11-01 | SIL OFL 1.1 (fonts/ofl/Fredoka-OFL.txt) | yes (pixels drawn from it ship in the patch) | graphics-text redraws (tools/gen_gfx.py) | - |
