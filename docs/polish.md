# Polish list

Minor issues deferred from reviews (phase 6 reviewer pass, 2026-11-01). One pass fixes them before release; tick
each line (`- [x]`) when fixed or ruled out. The release gate needs no unticked line.
Format: ids - problem - suggested direction (the reviewers' full wording was condensed here).

### g01 (OVLGMAIN item/menu descriptions, code strings: byte caps)
- [ ] OVLGMAIN@800CB6FC - "Monkey-san's home" next to "Mr. Rabbit/Tanuki/Turtle" - align after the honorific sweep
- [ ] OVLGMAIN@800CC1F0 "valor" -> Mark of Courage; 800CC3C0 -> "World's Greatest Pun Contest" (if caps allow)
- [ ] OVLGMAIN@800CB540 "Sound" -> "Music"; 800CB560 "Mid" -> "Normal"; 800CB5EC "Tea" -> "Teahouse" (caps)
- [ ] OVLGMAIN@800CCB9C "Biroon" opaque -> "a stretchy blob"
- [ ] OVLGMAIN@800CCED4 "salmon bento"; 800CBE54 "mirror she made"; 800CCD18 bamboo lost; 800CBC58, 800CC260 "lets you understand"

- [x] OVLGMAIN@800CC220 "Otohime glass" (reviewer: "Otohime Mirror") - 13-char in-place cap; kept. Straw Tycoon / Orihime's town / Destruction Bell: same, already in script/glossary_ok.txt

### g02 (OVLXTTL/OVLGMAIN code strings)
- [ ] OVLXTTL@800CC4A8 "Outrageous"; 800CB504 "Trial Match!"; 800CB514 "To the Story!"; 800CBD50 drop "Hey,"
- [ ] OVLXTTL@800CCD34 "Which One Show"; 800CBF80 "Thanks for your hard work" (match 800CC1D8)
- [ ] OVLGMAIN@800CD808 "Showy fireworks"; 800CD664 stray "!"; 800CD830 topic marker; 800CD494 "Even ... loves it"; 800CD5B4 "one stick, two tastes!"; 800CD868/898 "Lots of ... paste"; 800CD708 "tastes more nostalgic"

### g03 (EXE item names, OVLM racer comments; 7-11 B caps)
- [x] SLPM_868@80019130 "Candyfloss" - "Cotton Candy" is 12 B over a 10-char cap: kept
- [ ] SLPM_868@80018AD4/80018B98 "Moon/True Glass" -> "Mirror"; 80018B8C "Courage Mark"
- [ ] SLPM_868@8008C198 "Prism", 8008C1C0 "Steps", 8008C190 "Invite", 80019160 "Dumplings" (7 B caps)
- [ ] OVLM03@800CB364 "Imp", 800CB3B4 "Fisher"; OVLM02@800CB350 "Crown" -> "Horns", 800CB384 "Back Hair"
- [ ] SLPM_868@80018EBC "Candy Apple"; 80018DBC "Salt Salmon"; 8008C2AC "Eggplant"; 800191B0 "Warm"; OVLM25@800CB34C "Face-off time!"

### g04/g05 (OVLEVT ending, GDEF0D shops)
- [ ] GDEF0D/56/0004 appraiser "eh"; 99/013E "elsewhere"; 53/000E repeat; 100/0040 "slimmed down"; 75/0008 "here are two"; 65/075C order
- [ ] YUGI0D/11/0002 vs PREM0D/19/0002 - same JP, unify EN
- [ ] OVLEVT@800CB3C0 待つ家 dropped; 800CB4B0/49C "see the error of his ways"
- [ ] GDEF0D/103/0040, 0060 debug "Select Yes/No"
- [ ] GDEF0D/93-96 Kansai bank "-han" vs "-san": pick one (GSV0700D/4 uses "-han")

### g06
- [ ] GSV0001D/2/039A "We got so many trophies that..."; GSV0100D/20/0002 title "!" + comma; EVT030D/7/0002 "gall" -> "frustrated"

### g07 and title punctuation
- [ ] GSV0200D/15/0010, 21/0298 elder voice; 23/0504 "A nobody like you...!"; GSV0209D/3/0002 "jumpy one"; GSV0300D/20/0002 label; GSV0300D/21/0126 "Hello, hello"; GSV0300D/10/0534 "Whoa there"; GSV0207D/7/0002 "so mad"; GSV0200D/12/0002 repeat; GSV0302D/3/0010; GSV0200D/24/0010 "This year's"
- [ ] Titles ending in "!" collide with punctuation ("Match!{ww} for", "GO!{ww}!"): GSV0208D/4/0070, GSV0209D/2/0074, GSV0302D/2/01A0, GSV0808D/3/026A, 5/0002, GSV0900D/16/0320, 056E, 29/0018, GSV1600D/26,28,37/0002, GSV3000D/13/0002, GSF0603D/3/0002 - one pass over every "!{ww}" followed by punctuation

### g08
- [ ] GSV0408D/2/02DC, 035C "thank goodness"; GSV0400D/20/0002 "I'm Tanishinosuke!!"; GSV0600D/21/00EC dogs badmouthing; GSV0400D/13/005C "so scared of"; GSV0500D/6/0052, 9/0062, 10/0156 plop puns; GSV0600D/21/0010 "Dang it!!"; GSV0500D/3/0010 farmer; GSV0409D/2/03C6, 0498 "pockets are full"; GSV0400D/16/0010 "set its sights"; GSV0600D/36/00EC "Phew"

### g09
- [x] GSV0800D/11/0A60 - JP itself has {bb} with no {ww} (the code check requires the same codes), so EN keeps "{bb}Game Axe?!"; check the colour in the phase 8 tour
- [ ] GSV0800D/15/0326 "knees give out"; 12/0018 vs 23/0018 "first/second disciple"; 11/04AE, 11/0722, 31/08CA, 5/0002, 11/07C4; GSV0806D/4/002A "equipment"

### g10
- [ ] GSV0900D/30/0038 "favoooor"; 30/0232 "I'll haunt youuu"; 19/0002 antecedent; 27/0256; 16/0884; 16/0E8A "I knew it"; 17/001E "master medicine-maker"; 18/03E4 digger dialect; GSV0810D/2/00D2; GSV0900D/28/01BA article; GSV1001D/2/033C "passing himself off"; GSV0900D/16/11C2; GSV0807D/2/0116 stray dots

### g11
- [ ] GSV1200D/41/00CA "fare kon-well"; 42/0010 cough joke; GSV1001D/5/001E "Sorry"; GSV1207D/2/05CA; GSV1200D/46/01CE "Yay!"; GSV1002D/2/0010 "and more"; GSV1100D/10/030E "Oh, I seeee"; GSV1200D/25/002C, 0206 elder "eh"; GSV1213D/3/0002 "Explosives"

### g12
- [ ] GSV1300D/24/01A2 tail pun; 24/001E "Dajare-dare"; GSV1309D/7/05D8 cake cutting; 7/15BA "sweet pea"; GSV1300D/29/01E2 stutter; GSV1306D/2/0140; GSV1300D/23/023C extra "......"; GSV1309D/7/0AEC lavender pun

### g13
- [ ] GSV1316D/2/01A8 "Trade it to me for"; GSV1600D/43/0002 heart "<3"; 32/0010 lisp; 51/001A, 00E4 "Above all"; 51/03A8; 29/0010 "everyone's talking about"; GSV1611D/6/0002 "Full Mastery"; GSV1600D/38/0002 address; 47/0038 "fifth floor"; GSV1607D/3/0106; GSV1600D/58/0148, 06B2 ドロロン

### g14
- [ ] GSV2109D/2/0010 のに; GSV2200D/45/0152, 01B8 "Before long"; GSV2100D/17/0010 "too"; 18/0010 "Tanuki-san"; 28/0000 page break; 19/006E; 15/0038, 30/004E, 30/00D4 "useful tip"; 31/00CC; GSV2108D/3/0002 "me"; GSV2113D/5/022A "Huh?!"; GSV2200D/29/004E; GSV1622D/7/0002 wish; GSV1620D/8/00B2 Dentetsu pun; GSV2200D/28, 38 "<3" glyph check

### g15
- [ ] GSV2215D/2/02D2 "Uuugh"; GSV2214D/2/0306 "tons"; GSV2300D/25/001C "anymore"; 18/0002; GSV2302D/3/0002; GSV2500D/3/000E, GSV2300D/27/022E "Whoa!"; GSV3000D/11/04F4, 0630 "Oh? You'll use it here"; GSV2212D/2/0010; GSV2220D/3/0058 "eh"; GSV2300D/20/0002 "my boy"; Tsuzura Cave glossary row

### g16
- [ ] GSV3301D/4/0010 "But"; GSV3409D/2/0002 "Boss"; GSV3300D/3/0336 ぞい; 3/05C6 carpenter; 4/00E4 "Big Brother Peach"; GSV3400D/15/0010 monkeys; 21/0002 "Wow!"; GSV3410D/2/0316; GSV3412D/2/009E; GSV3413D/2/03E2 "Ryu Plate" -> "Dragon Plate"; GSV3600D/15/00FA "bungler"; GSV3700D/6/0002 "Torch"; 16/0000 ♪; GSV3900D/11-12/0048 panel words; GSV3301D/2/0070

### g17
- [ ] GSF0000D/78/0000; 32/000A "blew"; 91/0002 ", ken!"; 96/0002 "You haven't"; 67/02A4, 68/000A "eh"; 93/0002; GSV4000D/3/0002 page split; GSV3900D/13/0740

### g18
- [ ] GSF0400D/4/08AA; GSF0500D/3/0178, GSF0501D/3/0184; GSF0603D/2/0146, 028C person switch; 2/0630 "lame"; GSF0803D/4/0076 register; 4/019A, 3/0074 "Veggie Stir-Fry"; GSF0900D/5/0096 "anymore"; GSF0903D/4/0050, 6/0052 "Auntie"; GSF0501D/3/020A

### g19
- [ ] GSF1206D/3/02BE "kept on going"; 7/0002, 8/0002 "my way"; GSS0800D/2/0998; GSF1205D/9/00E0; 2/0686; GSF1300D/3/006A; GSS0400D/2/0018 sweetfish hint

### g20
- [ ] M020D/21/0002 snaggleteeth; M030D/36/0002 "Ook!"; M070D/20/0078 "Level up!!"; M110D/19/0002; M030D/42/0002, 40/0002; M020D/10/000A; M040D/140/000A; M030D/29-31/000A harmonize

### g21
- [ ] M140D/14/000A, M170D/41/0224, 027A/02BC/02FE/033E dice wording; M180D/24/0002, 22/0002, 26/0002; M150D/15/0002 "{R0} rocks" plural; M170D/41/0002; M220D/75/0022; M190D/66/0002 osu/ossu; M170D/33 Ono pun; M170D/36 "position chaaange"

### g22
- [ ] M510D/36/0014 blank season; M240D/15/0012 person; 15/007C; M510D/16,19,22,25,28 "blanked"; M490D/4/0016; M380D/10/000A; M500D/4/02E4

### g23-g26 (quizzes; every .0 answer verified correct)
- [x] M510D/227/0026, 229/0024, 238/0024 - JP key looks factually off (Nagasaki coastline, Shikotsu volume, Hokkaido rice): kept, the game scores .0
- [ ] M510D/69/0000.0 "League of Nations"; 66/0000.1 "Yellow River Man"; 91/0000.2 "Crop failure"; 103/0000.1 "Self"; 109/0000.1 "Pot"; 67/0000.2; 62/0000.2 "Angles"; 76/0028; 101/0024 "mokaru"; 110/0024; 125/001C
- [ ] M510D/151/0028, 215/002C, 209/0034, 145/0014 glosses; 146/148 capitalized answers
- [ ] M510D/286/002A, 326/0024 "hoikourou", 301/0000.0/.2 "Flower", 301/0000.3, 277/0000.1 "Tiananmen Square", 296/0024, 282/0000.2 "Zoo"
- [ ] M530D/4/008C tense + "zoiii"; M510D/354/001C, 345/0000.1/.3 "Flower", 343/001C, 351/002A; M550D/4/00D4 "his {MM}", 4/0258, 4/001A; M540D hermit stiffness; M520D/4/00E0; M510D/356/0000.1
