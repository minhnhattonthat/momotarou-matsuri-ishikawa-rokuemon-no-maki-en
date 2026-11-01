Momotarou Matsuri: Ishikawa Rokuemon no Maki (PlayStation) - English fan translation v@VERSION@

This is an unofficial fan translation. It contains no playable game image.
Use your own clean Japanese disc dump. Do not distribute pre-patched images.

BASE DISC
Name: Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).bin (Redump naming)
Serial: SLPM-86888
Size: @BASE_SIZE@ bytes
CRC32: @BASE_CRC32@
MD5: @BASE_MD5@
SHA-1: @BASE_SHA1@

PATCHING
1. Keep an untouched backup of your original .bin and .cue.
2. Use xdelta3 or an xdelta-compatible patcher (e.g. Delta Patcher) to apply
   @PATCH@ to the original .bin, saving the result in a separate folder
   under the same file name. Never apply it to the .cue or an already-patched image.
3. Copy your original .cue into that folder. Its FILE entry must name the
   patched .bin exactly. The original single-track layout is kept.
4. Boot that .cue in your emulator. Start from a cold boot; old savestates
   contain old code and graphics. Circle confirms.

Command-line example (choose a new output path):
xdelta3 -d -s "original.bin" "@PATCH@" "Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).bin"

PATCHED IMAGE
Size: @PATCHED_SIZE@ bytes
CRC32: @PATCHED_CRC32@
MD5: @PATCHED_MD5@
SHA-1: @PATCHED_SHA1@

TRANSLATION STATUS
Dialogue, story, menus, items, quizzes, minigames and system messages: English.
Title, menus, banners, minigame labels, all 100 Dialect Cards, readable shop
and place signs, and the credits roll: English.
Left as art: marks on character clothes and costumes, small emblems, tiny or
illegible placards, wall scrolls and landscape kanji. Some character costumes
(Kintaro, Poverty God, God of Fortune, Enma) were redrawn with English
initials; others keep their original marks.
Music and sound are unchanged.

TESTING AND LIMITATIONS
Tested with PCSX-Redux (nightly 2026-10-30, x64) and a Japanese PS1 BIOS.
The final image passed a cold-boot smoke test, automated scene routes,
text and engine checks, visual review and a chapter-by-chapter story review.
Scene routes used external debugger warps; the release image contains no
debug tool or cheats. This is not a complete natural playthrough, and real
hardware has not been tested. Some staff name readings are inferred.

CREDITS
Original game: Hudson Soft and its original creators (see the in-game credits).
English translation and tools: this project's contributors, with extensive
AI assistance from Claude (Anthropic).
Names and terms shared with the series follow the project's Momotarou
Densetsu (PS1) translation.
Fonts: listed with their licences in the source repository (docs/fonts.md).
Tools: PCSX-Redux, mkpsxiso/dumpsxiso, armips, xdelta3 and the
retro-translation skill.

Source, build instructions and bug reports:
https://github.com/minhnhattonthat/momotarou-matsuri-ishikawa-rokuemon-no-maki-en
For a bug report, include the patch version, emulator, steps and a savestate
if you have one.
