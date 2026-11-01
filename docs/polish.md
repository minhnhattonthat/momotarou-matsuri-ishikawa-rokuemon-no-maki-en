# Polish list

Minor issues deferred from reviews (phase 6 reviewer pass, 2026-11-01). One pass fixes them before release; tick
each line (`- [x]`) when fixed or ruled out. The release gate needs no unticked line.
Format: ids - problem - suggested direction (the reviewers' full wording was condensed here).

### Credits graphics
- [x] waived (D11 lenient; release README says some staff readings are inferred): gfx/credits.tsv - confirm uncited kanji-name/pen-name readings listed in docs/re/credits-qa.md or record an explicit editorial ruling; current conventional readings are provisional, despite complete visual coverage.

### g01 (OVLGMAIN item/menu descriptions, code strings: byte caps)
- [x] OVLGMAIN@800CB6FC - "Monkey-san's home" next to "Mr. Rabbit/Tanuki/Turtle" - align after the honorific sweep (kept: neighbours already Rabbit-san/Turtle-san/Tanuki-san)
- [x] OVLGMAIN@800CC1F0 "valor" -> Mark of Courage; 800CC3C0 -> "World's Greatest Pun Contest" (if caps allow) (1F0 fixed "seal: Mark of Courage"; 3C0 kept: cap + lint needs "Pun Contest" in that entry)
- [x] OVLGMAIN@800CB540 "Sound" -> "Music"; 800CB560 "Mid" -> "Normal"; 800CB5EC "Tea" -> "Teahouse" (caps) (540 fixed; 560 kept: "Normal" 29 px > 26 and must match M580D/SLPM "Mid"; 5EC kept: 7 B cap, glossary plaque rule "Tea")
- [x] OVLGMAIN@800CCB9C "Biroon" opaque -> "a stretchy blob" (kept: links to the "biroon" creatures in GSV0209D/GSV1611D; "stretchy blob" over cap)
- [x] OVLGMAIN@800CCED4 "salmon bento"; 800CBE54 "mirror she made"; 800CCD18 bamboo lost; 800CBC58, 800CC260 "lets you understand" (all fixed: "Cheap tasty salmon / bento!"; "Bright even in caves: / Princess Kaguya made / this mirror"; "Bamboo milk flask"; cat/frog "...speech / makes sense!", dog "and understand dog / speech!")

- [x] OVLGMAIN@800CC220 "Otohime glass" (reviewer: "Otohime Mirror") - 13-char in-place cap; kept. Straw Tycoon / Orihime's town / Destruction Bell: same, already in script/glossary_ok.txt

### g02 (OVLXTTL/OVLGMAIN code strings)
- [x] OVLXTTL@800CC4A8 "Outrageous"; 800CB504 "Trial Match!"; 800CB514 "To the Story!"; 800CBD50 drop "Hey," (4A8 fixed "Outrageous; preposterous"; 504/514 kept: already "Quick Match!"/"Story Mode", clear menu labels; BD50 fixed)
- [x] OVLXTTL@800CCD34 "Which One Show"; 800CBF80 "Thanks for your hard work" (match 800CC1D8) (CD34 kept: "Which One SHOW" used in GSV1308D/GSV1621D/M030D; BF80 fixed)
- [x] OVLGMAIN@800CD808 "Showy fireworks"; 800CD664 stray "!"; 800CD830 topic marker; 800CD494 "Even ... loves it"; 800CD5B4 "one stick, two tastes!"; 800CD868/898 "Lots of ... paste"; 800CD708 "tastes more nostalgic" (808 kept: 15 B cap; 494 kept: "...too" over cap; fixed: 664 "apricot.", 840/830/820 "Momotaro's / travel pal? / This is it!", 5B4, 868 "Chunky bean galore", 898 "Silky paste galore", 708 "the homier it tastes")

### g03 (EXE item names, OVLM racer comments; 7-11 B caps)
- [x] SLPM_868@80019130 "Candyfloss" - "Cotton Candy" is 12 B over a 10-char cap: kept
- [x] SLPM_868@80018AD4/80018B98 "Moon/True Glass" -> "Mirror"; 80018B8C "Courage Mark" (all kept: 11 B caps incl. terminator, "Moon Mirror"/"True Mirror"/"Courage Mark" over)
- [x] SLPM_868@8008C198 "Prism", 8008C1C0 "Steps", 8008C190 "Invite", 80019160 "Dumplings" (7 B caps) (all kept: "Rainbow" 8 B > 7, Pedometer/Invitation over cap, millet dumpling/Kibidango no clearer)
- [x] OVLM03@800CB364 "Imp", 800CB3B4 "Fisher"; OVLM02@800CB350 "Crown" -> "Horns", 800CB384 "Back Hair" (350 fixed "Horns"; rest kept: 7 B caps, Amanojaku/Urashima/Back Hair over)
- [x] SLPM_868@80018EBC "Candy Apple"; 80018DBC "Salt Salmon"; 8008C2AC "Eggplant"; 800191B0 "Warm"; OVLM25@800CB34C "Face-off time!" (191B0 fixed "Warm friendship..."; EBC/DBC/2AC kept: over cap; OVLM25 kept: same JP as OVLM71 "Funny face time!", lint same-JP rule)

### g04/g05 (OVLEVT ending, GDEF0D shops)
- [x] GDEF0D/56/0004 appraiser "eh"; 99/013E "elsewhere"; 53/000E repeat; 100/0040 "slimmed down"; 75/0008 "here are two"; 65/075C order (all fixed except 99/013E kept: identical JP+EN in GSV3204D, lint same-JP rule; change both together if wanted)
- [x] YUGI0D/11/0002 vs PREM0D/19/0002 - same JP, unify EN (fixed: YUGI0D now matches PREM0D)
- [x] OVLEVT@800CB3C0 待つ家 dropped; 800CB4B0/49C "see the error of his ways" (fixed: "To Grandpa and Grandma, who waited,"; "and made Great King Enma / mend his ways!")
- [x] GDEF0D/103/0040, 0060 debug "Select Yes/No" (kept: neutral JP, "Selected Yes/No" reads as the post-choice debug result)
- [x] GDEF0D/93-96 Kansai bank "-han" vs "-san": pick one (GSV0700D/4 uses "-han") (kept: all 桃太郎はん already "-han"; お客はん -> "friend")

### g06
- [x] fixed (EVT030D same-JP twins EVT040/050/060/140/150/200/210/280D synced): GSV0001D/2/039A "We got so many trophies that..."; GSV0100D/20/0002 title "!" + comma; EVT030D/7/0002 "gall" -> "frustrated"

### g07 and title punctuation
- [x] fixed (twin GSV0300D/10/0674 synced; label now matches the other "{n}The number is" labels): GSV0200D/15/0010, 21/0298 elder voice; 23/0504 "A nobody like you...!"; GSV0209D/3/0002 "jumpy one"; GSV0300D/20/0002 label; GSV0300D/21/0126 "Hello, hello"; GSV0300D/10/0534 "Whoa there"; GSV0207D/7/0002 "so mad"; GSV0200D/12/0002 repeat; GSV0302D/3/0010; GSV0200D/24/0010 "This year's"
- [x] fixed (titles now end the sentence; also GSV0209D/3/0002, twin GSV1611D/4/000E; 5/0002 = GSV0808D/5/0002), except kept GSV0900D/16/056E (title already ends the line, nothing follows): Titles ending in "!" collide with punctuation ("Match!{ww} for", "GO!{ww}!"): GSV0208D/4/0070, GSV0209D/2/0074, GSV0302D/2/01A0, GSV0808D/3/026A, 5/0002, GSV0900D/16/0320, 056E, 29/0018, GSV1600D/26,28,37/0002, GSV3000D/13/0002, GSF0603D/3/0002 - one pass over every "!{ww}" followed by punctuation

### g08
- [x] fixed (twin GSV0400D/21/0002 synced; plop puns: "plop-ages", "so giddy I could plop"): GSV0408D/2/02DC, 035C "thank goodness"; GSV0400D/20/0002 "I'm Tanishinosuke!!"; GSV0600D/21/00EC dogs badmouthing; GSV0400D/13/005C "so scared of"; GSV0500D/6/0052, 9/0062, 10/0156 plop puns; GSV0600D/21/0010 "Dang it!!"; GSV0500D/3/0010 farmer; GSV0409D/2/03C6, 0498 "pockets are full"; GSV0400D/16/0010 "set its sights"; GSV0600D/36/00EC "Phew"

### g09
- [x] GSV0800D/11/0A60 - JP itself has {bb} with no {ww} (the code check requires the same codes), so EN keeps "{bb}Game Axe?!"; check the colour in the phase 8 tour
- [x] fixed (5/0002 read as GSV0808D/5/0002, done in the title pass; GSV0806D/4/002A "game items", glossary 道具 = item; GSV0800D/12/009C Kinichiro still says "number one pupil" (other JP, not my id)): GSV0800D/15/0326 "knees give out"; 12/0018 vs 23/0018 "first/second disciple"; 11/04AE, 11/0722, 31/08CA, 5/0002, 11/07C4; GSV0806D/4/002A "equipment"

### g10
- [x] fixed: GSV0900D/30/0038 "favoooor"; 30/0232 "I'll haunt youuu"; 19/0002 antecedent; 27/0256; 16/0884; 16/0E8A "I knew it"; 17/001E "master medicine-maker"; 18/03E4 digger dialect; GSV0810D/2/00D2; GSV0900D/28/01BA article; GSV1001D/2/033C "passing himself off"; GSV0900D/16/11C2; GSV0807D/2/0116 stray dots

### g11
- [x] fixed (also same-JP 41/01BA): GSV1200D/41/00CA "fare kon-well"; 42/0010 cough joke; GSV1001D/5/001E "Sorry"; GSV1207D/2/05CA; GSV1200D/46/01CE "Yay!"; GSV1002D/2/0010 "and more"; GSV1100D/10/030E "Oh, I seeee"; GSV1200D/25/002C, 0206 elder "eh"; GSV1213D/3/0002 "Explosives"

### g12
- [x] fixed (also same-JP GSV2106D/2/0140), except kept: 23/023C "......" (JP page is blank; lint forbids an empty page), 7/0AEC tulip/two-lips (classic pun fits the host's 王道 comment; lavender has no English pun): GSV1300D/24/01A2 tail pun; 24/001E "Dajare-dare"; GSV1309D/7/05D8 cake cutting; 7/15BA "sweet pea"; GSV1300D/29/01E2 stutter; GSV1306D/2/0140; GSV1300D/23/023C extra "......"; GSV1309D/7/0AEC lavender pun

### g13
- [x] fixed ({rr}<3{ww} everywhere: '<' is in fonts/en12.txt; 32/0010 lisp now th-lisp, same speaker's 32/00A6, 01C6 aligned; ドロロン -> "Whoooo...!"): GSV1316D/2/01A8 "Trade it to me for"; GSV1600D/43/0002 heart "<3"; 32/0010 lisp; 51/001A, 00E4 "Above all"; 51/03A8; 29/0010 "everyone's talking about"; GSV1611D/6/0002 "Full Mastery"; GSV1600D/38/0002 address; 47/0038 "fifth floor"; GSV1607D/3/0106; GSV1600D/58/0148, 06B2 ドロロン

### g14
- [x] fixed, except kept: 18/0010 "Tanuki-san" (D1 honorifics, matches the Tanuki-san label), GSV2200D/28, 38 (already {rr}<3{ww}, glyph exists): GSV2109D/2/0010 のに; GSV2200D/45/0152, 01B8 "Before long"; GSV2100D/17/0010 "too"; 18/0010 "Tanuki-san"; 28/0000 page break; 19/006E; 15/0038, 30/004E, 30/00D4 "useful tip"; 31/00CC; GSV2108D/3/0002 "me"; GSV2113D/5/022A "Huh?!"; GSV2200D/29/004E; GSV1622D/7/0002 wish; GSV1620D/8/00B2 Dentetsu pun; GSV2200D/28, 38 "<3" glyph check

### g15
- [x] fixed, except Tsuzura Cave glossary row (glossary.md is controller-only; NEW TERM つづらの洞窟 -> Tsuzura Cave, used in GSV2111D): GSV2215D/2/02D2 "Uuugh"; GSV2214D/2/0306 "tons"; GSV2300D/25/001C "anymore"; 18/0002; GSV2302D/3/0002; GSV2500D/3/000E, GSV2300D/27/022E "Whoa!"; GSV3000D/11/04F4, 0630 "Oh? You'll use it here"; GSV2212D/2/0010; GSV2220D/3/0058 "eh"; GSV2300D/20/0002 "my boy"; Tsuzura Cave glossary row

### g16
- [x] fixed, except kept: GSV3413D/2/03E2 "Ryu Plate" (item name SLPM_868@80018C90 is "Ryu Plate", 11 B cap, "Dragon Plate" is 12; "Dragon Dish" would fit both if wanted), GSV3900D/11-12/0048 panels (same-JP lint forces both ア = AP, both ン = RI; panels spell MIL LET DUMP LING + AP RI COT POP): GSV3301D/4/0010 "But"; GSV3409D/2/0002 "Boss"; GSV3300D/3/0336 ぞい; 3/05C6 carpenter; 4/00E4 "Big Brother Peach"; GSV3400D/15/0010 monkeys; 21/0002 "Wow!"; GSV3410D/2/0316; GSV3412D/2/009E; GSV3413D/2/03E2 "Ryu Plate" -> "Dragon Plate"; GSV3600D/15/00FA "bungler"; GSV3700D/6/0002 "Torch"; 16/0000 ♪; GSV3900D/11-12/0048 panel words; GSV3301D/2/0070

### g17
- [x] fixed: GSF0000D/78/0000; 32/000A "blew"; 91/0002 ", ken!"; 96/0002 "You haven't"; 67/02A4, 68/000A "eh"; 93/0002; GSV4000D/3/0002 page split; GSV3900D/13/0740

### g18
- [x] fixed (twin GSF0401D/1/01F4 synced; item name stays "Stir-Fry" (SLPM 11 B cap), dialogue says "veggie {bb}Stir-Fry{ww}"): GSF0400D/4/08AA; GSF0500D/3/0178, GSF0501D/3/0184; GSF0603D/2/0146, 028C person switch; 2/0630 "lame"; GSF0803D/4/0076 register; 4/019A, 3/0074 "Veggie Stir-Fry"; GSF0900D/5/0096 "anymore"; GSF0903D/4/0050, 6/0052 "Auntie"; GSF0501D/3/020A

### g19
- [x] fixed: GSF1206D/3/02BE "kept on going"; 7/0002, 8/0002 "my way"; GSS0800D/2/0998; GSF1205D/9/00E0; 2/0686; GSF1300D/3/006A; GSS0400D/2/0018 sweetfish hint

### g20
- [x] fixed (all; M030D/29 now matches 30/31 wording) - M020D/21/0002 snaggleteeth; M030D/36/0002 "Ook!"; M070D/20/0078 "Level up!!"; M110D/19/0002; M030D/42/0002, 40/0002; M020D/10/000A; M040D/140/000A; M030D/29-31/000A harmonize

### g21
- [x] fixed ("a die"/"extra die", "Rocks smashed by Momotaro: {R0}!", Ossu x3, "position chaaange" x6); M170D/33 kept: "Shocker Ono (stage name)" is a parody name, no recoverable pun - M140D/14/000A, M170D/41/0224, 027A/02BC/02FE/033E dice wording; M180D/24/0002, 22/0002, 26/0002; M150D/15/0002 "{R0} rocks" plural; M170D/41/0002; M220D/75/0022; M190D/66/0002 osu/ossu; M170D/33 Ono pun; M170D/36 "position chaaange"

### g22
- [x] fixed (all) - M510D/36/0014 blank season; M240D/15/0012 person; 15/007C; M510D/16,19,22,25,28 "blanked"; M490D/4/0016; M380D/10/000A; M500D/4/02E4

### g23-g26 (quizzes; every .0 answer verified correct)
- [x] M510D/227/0026, 229/0024, 238/0024 - JP key looks factually off (Nagasaki coastline, Shikotsu volume, Hokkaido rice): kept, the game scores .0
- [x] fixed (all; same-JP twins 73/0000.1, 78/0000.1 synced; 110/.2 "Mujina" not "Badger"; 125 gloss "Like ___ to like") - M510D/69/0000.0 "League of Nations"; 66/0000.1 "Yellow River Man"; 91/0000.2 "Crop failure"; 103/0000.1 "Self"; 109/0000.1 "Pot"; 67/0000.2; 62/0000.2 "Angles"; 76/0028; 101/0024 "mokaru"; 110/0024; 125/001C
- [x] glosses fixed (less give-away, one question form); 146/148 kept: sentence-case answers match all other quiz choices - M510D/151/0028, 215/002C, 209/0034, 145/0014 glosses; 146/148 capitalized answers
- [x] 277 "Tiananmen Square", 282 "Zoo", 296 fixed; kept 286 (kanji can't be shown, "read seirei" asks the same), 326 (already "hoikoro"), 301/.3 (Mackerel+Leaf matches the part-gloss style) - M510D/286/002A, 326/0024 "hoikourou", 301/0000.3, 277/0000.1 "Tiananmen Square", 296/0024, 282/0000.2 "Zoo"
- [x] fixed (all; M540D folksy in all 8 entries; 356/.1 "Wrong+Danger"; romaji kyocho/kando) - M530D/4/008C tense + "zoiii"; M510D/354/001C, 343/001C, 351/002A; M550D/4/00D4 "his {MM}", 4/0258, 4/001A; M540D hermit stiffness; M520D/4/00E0; M510D/356/0000.1

### Story pass (2026-11-02, chapter minors; suggested EN in quotes)
- [x] fixed (かしら = "Boss" in all 13 narration lines): s01: GSF0000D/67/02A4, 68/000A Jizo elder tone ("Truly sorry about that, eh!"); GSF0000D/114/0010 "Peach Buns" casing; GSF0000D/105-119 かしら "captain" vs "Boss": one word; GSS0000D/2/0236 Tanokyu folksy
- [x] fixed ("her" via script/by_id.tsv, its 6 same-JP twins are men; Mommy twin GSF0000D/86/0002 synced), except kept GSV0200D/11/035E (narration, no voice): s02: GSV0400D/22/0120 "showed her the mask"; GSV0409D/2/0030, 00D0, 01FA, 03C6 turnip girl "ye/yer" -> "you/ya/your"; GSV0200D/11/00C6, 0250, 035E bonfire oni consistent rough register; GSF0200D/23/0002, 24/00BE, 24/0298 Yoshikichi "Mommy" throughout; GSF0201D/2/0002 Green Poop keeps どす tic in the question; GSF0300D/3/0000 "Please listen to my hint!"
- [x] fixed: s03: GSF0500D/3/0178, GSF0501D/3/0184 "Just a little trip!"; GSV0600D/38/07D8 end punctuation; GSV0611D/3/006A "The Dog has come home safe and sound, too."
- [x] fixed (number labels: no period, as 20 of 24; twins GSV0900D/15/0002, GSV1309D/2/0002 dropped theirs; GSV0800D/13/0002 already matched): s04: GSV0900D/1/0624 "I'll make you look like a total fool in front of big bro, kuri!"; GSF0900D/5/02BE + GSV1600D/57/0178 "The Red Bell was stolen from Momotaro!"; GSV0910D/2/0104 widow reads the Will herself; GSV0900D/18/02F2 "Oh, that's right!"; GSV0800D/13/0002 empty-number period consistency
- [x] fixed, except kept GSV1200D/29/0002 doubled {bb} (JP has 2 {bb} + 1 {ww}; codes must match). s05: GSF1205D/2/116E Enma "was great fun, I must say!"; GSV1200D/29/0002 drop doubled {bb} if codes check allows; GSV1001D/3/0026 "she's feeling unwell"; GSV1215D/3/0002 アタイ brash girl; GSV1217D/3/080E "Well, aren't you modest!"; GSF1201D/3/01EE "Pesky little Momotaro!"
- [x] fixed. s06: GSV1314D/2/02AC "Aw, don't say that! Lend an old man a hand, eh?"; GSV1314D/2/0216 "Wonderful! I knew I could count on you, Momotaro-san!"
- [x] fixed (heart = {rr}<3{ww} both places). s07: GSV1617D/2/0102 vs GSV1600D/43/0002 {rr}∞ heart: same rendering both places; GSV1620D/7/020E "collect so many!"; GSV1622D/10/0002 gūsū -> snoring gag; GSV1620D/4/0140 "mooney"
- [x] fixed. s08: GSV2307D/3/0002, GSV2100D/22/0002 lisp style (th-lisp like other kids); GSV2100D/19/006E "if you pick all three right"; GSV2200D/36/007E farmer rustic; GSV2110D/2/00BE "Fried Tofu" casing; GSV2009D/2/0002 stray period
- [x] fixed (also 3/07AC same "Much appreciated"). s09: GSV3409D/2/0002 "the Boss of the Dragon God Ship"; GSV3410D/2/0316 "Looks like we can't understand each other!!"; GSV3300D/3/0048, 0498, 05C6, 06EE Boss "Much appreciated!"; GSV3300D/4/00E4 "Big Bro Peach!"; GSV3600D/19/00FA "Monkey-san's praise wasn't wrong, kee!"; GSV3700D/14/015E "several of the Jizo"
