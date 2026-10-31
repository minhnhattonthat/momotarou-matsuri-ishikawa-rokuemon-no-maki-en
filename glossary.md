# Glossary - Momotarou Matsuri: Ishikawa Rokuemon no Maki (PS1)

Binding for every translator and reviewer. Agents propose additions in reports; only the controller edits this file.
`tools/batches.py terms` puts the rows a batch needs into `build/terms_<batch>.txt`; `batches.py check` fails a line
whose JP has a term but whose English lacks the EN form (exceptions: `script/glossary_ok.txt`, id/term/reason).
Shared names reuse `../momotarou-densetsu-en/glossary.md` (same series, same owner).

## Rulings (asked of the user once; options and reasons in docs/decisions.md)
- Honorifics: kept, hyphenated (Momotaro-san, Kintaro-kun, -sama, -dono). Name order: Western (given name first).
  Hepburn drops the long-vowel u (Momotaro, Rokuemon). 姫 in a name: Yashahime, Otohime; fairy-tale title: Princess
  Kaguya.
- Romanisation source: official English names where they exist, else an earlier fan patch (the sibling repo), else
  Hepburn without macrons.
- Credits: English.
- Register: light, comic, all-ages Hudson humour; keep Japanese folklore flavour (oni, ryo, hermits, shrines,
  festivals), translate everything else. Sound effects in plain English or romaji onomatopoeia that reads well.
- Abbreviations: full names and terms everywhere; prefer engine changes over shortening.

## Style rules
- Punctuation map: 「」 -> "...", 『』 -> '...', … / ・・・ -> ..., ！？ -> ?!, ～ (drawn out) -> stretch the word or
  "...", ー in a shout -> stretch the word ("Welcooome!").
- Dialogue in straight double quotes exactly where the JP uses 「」; narration unquoted.
- Character tics become an English tic, used as often as the JP uses it (docs/style-reference.md).
- Puns, parodies, proverbs and quiz answers: rebuild the joke in English; never footnote. Quiz questions whose
  answer depends on Japanese (kanji readings, opposite words, dialects) keep the Japanese word in romaji where needed.

## Characters
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| 桃太郎 / ももたろう | Momotaro | | hero, silent; 桃太郎さん -> Momotaro-san | Momotarou, Momotarō |
| 金太郎 / きんたろう | Kintaro | | 金太郎先生 -> Kintaro-sensei | Kintarou |
| 浦島 / 浦島太郎 | Urashima / Urashima Taro | | | |
| 夜叉姫 / やしゃひめ | Yashahime | | | Princess Yasha |
| 乙姫 | Otohime | | Ryugu Palace | |
| かぐや姫 | Princess Kaguya | | かぐや姫さま -> Princess Kaguya-sama | |
| 石川六右衛門 / 六右衛門 | Ishikawa Rokuemon / Rokuemon | | villain, leads the Oni Mask Gang; parody of the thief Ishikawa Goemon | Rokuemonn |
| 鬼面党 | Oni Mask Gang | | the bandits (盗賊団) | Kimen-to |
| はかい神 / 破壊神 | God of Destruction | | King Bombee revived (はかい神の復活書 Revival Book of the God of Destruction) | |
| 寝太郎 | Netaro | | sleeps all year | |
| 柿太郎 | Kakitaro | | persimmon boy, cry カキーッ -> "Kakiii!" | |
| 栗太郎 | Kuritaro | | chestnut boy, ends lines with クリ -> ", kuri!" | |
| 小太郎 | Kotaro | | | |
| 忠三郎 | Chuzaburo | | from Tabidachi Village; loves おせん Osen | |
| 権兵衛 | Gonbe | | kimono peddler | Gonbei |
| 銀次 | Ginji | | | |
| 不幸太 | Fukota | | | |
| 金一郎 | Kinichiro | | | |
| えのん | Enon | | poverty god (貧乏神・えのん -> Enon the Poverty God) | |
| ボンビー | Bombee | | | Bonby |
| キングボンビー | King Bombee | | | |
| ミニボンビー | Mini Bombee | | | |
| えんま大王 / えんま | Great King Enma / Enma | | | Emma |
| 水龍 | Water Dragon | | | |
| 雪女 | Yuki-onna | | snow woman | |
| 天邪鬼 | Amanojaku | | | |
| 鬼子母神 | Kishibojin | | | |
| 白蛇鬼 | White Snake Oni | | | |
| 花咲かじいさん / 花咲かじい | Old Man Hanasaka | | | |
| おりひめ / ひこぼし | Orihime / Hikoboshi | | Tanabata lovers | |
| イヌ / サル / キジ | Dog / Monkey / Pheasant | | companions | |
| ウンチ | Poop | | | Unchi |
| カレン | Karen | | | |
| 希望観音 | Kannon of Hope | | | |
| じんぱち | Jinpachi | | | |
| さくま | Sakuma | | | |

## Places
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| 希望の都 / 都 | Capital of Hope / the Capital | | | |
| 鬼ヶ島 | Onigashima | | | Oni Island |
| 竜宮城 | Ryugu Palace | | | |
| 地獄 | Hell | | | |
| 旅立ちの村 | Tabidachi Village | | X村 / Xの村 -> "X Village" (romaji X) | |
| カチカチの村 | Kachi-Kachi Village | | カチカチ大レース -> Great Kachi-Kachi Race | |
| 金太郎の村 | Kintaro Village | | | |
| 寝太郎の村 | Netaro Village | | | |
| 花咲かの村 | Hanasaka Village | | | |
| 浦島の村 | Urashima Village | | | |
| ひょっとこの村 | Hyottoko Village | | ひょっとこ山 Mt. Hyottoko | |
| おりひめの村 | Orihime Village | | | |
| ひこぼしの村 | Hikoboshi Village | | | |
| ほほえみの村 | Hohoemi Village | | | |
| 竹取りの村 | Taketori Village | | | |
| ウサカメの村 | Usakame Village | | | |
| 恩返しの村 | Ongaeshi Village | | | |
| 小太郎の村 | Kotaro Village | | | |
| おむすび村 | Omusubi Village | | | |
| 仙人の村 | Hermit Village | | | |
| すずめの都 | Sparrow Capital | | | |
| 氷の塔 | Ice Tower | | | |
| 宝物塔 | Treasure Tower | | | |
| 兄弟の洞窟 | Brothers' Cave | | | |
| 並び洞窟 | Row Cave | | | |
| 氷の洞窟 | Ice Cave | | | |
| 龍の島 | Dragon Island | | | |
| ひょうたんの森 | Gourd Forest | | | |

## Items / arts / terms
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| 鬼 | oni | | lowercase in prose, Oni in names (History Quiz Oni); plural oni | ogre, demon |
| 仙人 | hermit / Hermit | | | sage |
| 術 | art | | ひえんの術 -> the Warp art | spell, jutsu |
| ひえん | Warp | | ひえんの巻物 Warp Scroll | |
| ぬけだし | Escape | | | |
| はやあし | Dash | | | |
| ほうひ | Fart | | | |
| りょうり | Cooking | | | |
| おまもり | Protection | | おまもりの術 the Protection art | |
| ときかね | Time Bell | | ときかねの術 the Time Bell art (rings day/night) | |
| たこあげ | Kite | | たこあげの術 the Kite art | |
| 段 | level | | 段がもらえる -> earn levels | dan |
| 両 | ryo | | currency, "100 ryo" | gold, yen |
| お祭り / 祭り | festival | | | matsuri |
| トロフィー | trophy | | | |
| 鐘 | bell | | 赤/青/黄/緑の鐘 Red/Blue/Yellow/Green Bell | |
| カード / カードアルバム | card / Card Album | | 方言カード Dialect Card | |
| 道具 / どうぐ | item | | menu label: Items | |
| だいじなもの | Key Items | | | |
| といち屋 | Bank | | | |
| かんてい小屋 | Appraisal Hut | | | |
| 茶屋 | teahouse | | | tea house |
| 道具屋 | item shop | | | |
| ウサカメレース | Rabbit-Turtle Race | | betting race in Usakame Village | |
| サイコロ | dice | | "roll the dice" | |
| 鬼兄弟 | Oni Brothers | | | |
| ウヒャヒャ | Uhyahya | | hermits' laugh | |
| メモリーカード | Memory Card | | | |
| 勇気の印 | Mark of Courage | | | |
| 龍神船 | Dragon God Ship | | | |
| 七夕祭 / 七夕祭り | Tanabata Festival | | | |
| 大文字焼 / 大文字焼き | Daimonji Bonfire | | | |
| ゆうぎ / 遊戯 | game | | the festival minigames; ゆうぎ場 game stall | |
| ゆうぎ道 | Way of Games | | | |
| ゆうぎ仙人 | Game Hermit | | top rank title | |
| 名人 | Master | | rank title | |
| 達人 | Expert | | rank title | |
| 招待状 | Invitation | | | |
| きびだんご | millet dumpling | | | kibidango |
| 方言カード | Dialect Card | | 方言カード００１ -> Dialect Card 001 | |
| 新記録 | new record | | | |
| 宿屋 | inn | | | |
| 歩数 | Steps | | status field | |

## Decisions from earlier batches
- (none yet)
