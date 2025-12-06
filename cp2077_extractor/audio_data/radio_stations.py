#!/usr/bin/env python3
#
#  radio_station_data.py
"""
Data for songs that play on the in game radio.
"""
#
#  Copyright © 2025 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# TODO: generes (from tags in sounddb)
# TODO: check in-game capitalisation of station names

# stdlib
from collections.abc import Sequence

# this package
from cp2077_extractor.track import Track

__all__ = [
		"body_heat_radio",
		"dark_star",
		"growl_fm",
		"misc",
		"morro_rock_radio",
		"night_fm",
		"pacific_dreams",
		"principales",
		"radio_jingle_ids",
		"radio_pebkac",
		"radio_stations",
		"radio_vexelstrom",
		"ritual_fm",
		"royal_blue_radio",
		"samizdat_radio",
		"the_dirge",
		]

# TODO: read from JSON file

# Other uses of the songs (mainly in quests).
HANGOUT_QUEST = "Hangout"
RACES = "Races"
MUS_OW_PHONE = "mus_ow_phone"
SOMEWHAT_DAMAGED_FLASHBACK = "mus_q305_brooklyn_vinyl_01"
SOMEWHAT_DAMAGED_FLASHBACK_REED = "mus_q305_brooklyn_vinyl_reed"
CLOUDS_MUSIC = "mus_q105_dollhouse"
DARK_MATTER = "mus_sq017_dark_matter_club_user_friendly"  # Dark Matter during Kerry quest
JOHNNY_KERRY = "mus_q101_js_and_kerry_source"  # Love Like Fire quest Johnny & Kerry

# TODO: or is it 88.3, as in the credits data?
#: 88.9 Pacific Dreams
pacific_dreams: list[Track] = [
		Track("Quantum Lovers", "Isometric Air", 253367813, "Brian Aspey", "Brian Aspey"),
		Track("Quantum Lovers", "Practical Heart", 910852846, "Brian Aspey", "Brian Aspey"),
		Track(
				"Quantum Lovers",
				"Real Window",
				1005242856,
				"Brian Aspey",
				"Brian Aspey", {895217420: HANGOUT_QUEST}
				),
		Track(
				"Pacific Avenue",
				"Antagonistic",
				190841656,
				"Sebastian Robertson and Chris Cardena",
				"Chris Cardena & Sebastian Robertson",
				{871197545: HANGOUT_QUEST},
				),
		Track(
				"Jänsens",
				"Simple Pleasures",
				803750564,
				"Elena Charbila; Dimitris Mann",
				"Kid Moxie", {880346021: HANGOUT_QUEST}
				),
		Track("Flatlander Woman", "Lithium", 770891476, "SLG", "SLG"),
		Track("Flatlander Woman", "Slag", 1044871022, "SLG", "SLG"),
		Track(
				"Muchomorr",
				"Chodze",
				1066343217,
				"Mchy i Porosty",
				"Mchy i Porosty", {443457920: "Parade and Wako's briefing"}
				),
		Track("Lick Switch", "Midnight Eye", 928920080, "Earth Trax", "Earth Trax"),
		Track("Lick Switch", "Blurred", 285910393, "Earth Trax", "Earth Trax"),
		Track("Lick Switch", "The Other Room", 869646378, "Earth Trax", "Earth Trax"),
		Track("Sonoris Causa", "La Stessa Causa", 621406329, "Eltron", "Eltron"),
		Track("Left Unsaid", "Retrogenesis", 562668759, "Private Press", "Private Press"),
		Track("Talk to Us", "Miami Suicide", 400079366, "Chino", "Chino"),
		Track("Talk to Us", "Slippery Stabs", 1056620275, "Chino", "Chino"),
		Track("Wormview", "Ashes and Diamonds", 95368841, "Hatti Vatti", "Hatti Vatti"),
		Track("Mona Mitchell", "Ice Maddox", 1017413855, "FOQL", "FOQL"),
		]

#: 89.3 Radio Vexelstrom
radio_vexelstrom: list[Track] = [
		Track("The Cartesian Duelists", "Resist and Disorder", 308480891, "Jason Charles Miller", "Rezodrone"),
		Track("The Cartesian Duelists", "Kill the Messenger", 525137074, "Jason Charles Miller", "Rezodrone"),
		Track("Slavoj McAllister", "Makes Me Feel Better", 66952680, "Kevin Hastings", "OnenO"),
		Track("Keine", "Dead Pilot", 409198739, "Sebastian Robertson; Daniel Davies", "SRDD (Sebastian Daniel)"),
		Track("Keine", "Come Close", 303931745, "Sebastian Robertson; Daniel Davies", "SRDD (Sebastian Daniel)"),
		Track("Upgrade", "Black Terminal", 1065746543, "Bret Autrey; Danny Cocke", "Black Terminal"),
		Track("Alexei Brayko", "Reaktion", 49937168, "Jason Charles Miller", "Rezodrone"),
		Track("Ego Affliction", "With Her", 257784898, "Steven Richard Davis", "Steven Richard Davis"),
		Track("Den of Degenerates", "Never Stop Me", 811249141, "Steven Richard Davis", "Steven Richard Davis"),
		Track("The Red Glare", "Violence", 588422768, "Kristina Michelle Olson", "Le Destroy"),
		Track("The Red Glare", "Pain", 365987976, "Kristina Michelle Olson", "Le Destroy"),
		Track("Homeschool Dropouts", "Night City Aliens", 86209634, "The Armed", "The Armed"),
		Track("Tainted Overlord", "A Caça", 420329756, "Deafkids", "Deafkids", {640742970: RACES}),
		Track("Tainted Overlord", "Selva Pulsátil", 50379518, "Deafkids", "Deafkids"),
		Track(
				"N1v3Z",
				"Pig Dinner",
				874085468,
				"Ho99o9, N8NOFACE",
				"Ho99o9, N8NOFACE",
				),  # Not listed in credits data
		]

# TODO: check against credits
#: 89.7 Growl FM
growl_fm: list[Track] = [
		Track(
				"Coeur Noir",
				"Let The Stars Die",
				444314240,
				'Jeremy Ghanassia, Maxime "Paka" Marin',
				other_uses={959192573: SOMEWHAT_DAMAGED_FLASHBACK_REED}
				),
		Track(
				"Red Dead Roadkill",
				"Flatline",
				694001176,
				"Julien Röttger",
				"Red Dead Roadkill, Dee Wolf", {896635379: MUS_OW_PHONE}
				),
		Track(
				"Spirit Machines",
				"Candy Shell",
				945083955,
				"Jessica McCombs, Dave Crespo, Michael Collins, Sergio Marticorena"
				),
		Track("NoWorld", "Do or Die", 807725976, "NoWorld"),
		Track("Entolim", "LIT", 265573485, "Entolim"),
		Track("Skin on Flesh", "El Tiempo", 951381637, "Laura Jiménez Alvarez, Michiel Sybers"),
		Track(
				"Frost, Justtjokay, Dubbygotbars, Knyvez",
				"Killshot",
				116162799,
				"Frost, Justtjokay, Dubbygotbars, Knyvez",
				other_uses={316992516: MUS_OW_PHONE, 608799802: SOMEWHAT_DAMAGED_FLASHBACK}
				),
		Track(
				"Haru Nemuri",
				"さまよえるままゆけ (Samayoeru mama yuke) / Let It Go As If You Wander",
				214475991,
				"春ねむり (Haru Nemuri)",
				"春ねむり (Haru Nemuri)"
				),
		Track("Kiba", "Slipstream", 581037122, "Kiba"),
		Track("Aleyna Moon, Shrinjay Ghosh", "FUMES", 252703137, "Aleyna Moon, Shrinjay Ghosh"),
		Track(
				"D.O.H. Dollahz Ova Hoez",
				"Look Through My Kiroshis (The Solo Life)",
				606235279,
				"D.O.H. Dollahz Ova Hoez",
				other_uses={328723041: MUS_OW_PHONE, 1009571067: SOMEWHAT_DAMAGED_FLASHBACK}
				),
		Track("St. Aurora", "Going to Heaven", 816183854, "St. Aurora", other_uses={254921013: MUS_OW_PHONE}),
		Track(
				"Thai McGrath (ft. JustCosplaySings)",
				"Afterlife",
				900442762,
				"Thai McGrath; JustCosplaySings",
				"Thai McGrath; JustCosplaySings", {740594675: MUS_OW_PHONE}
				),
		]

#: 91.9 Royal Blue Radio
royal_blue_radio: list[Track] = [
		Track("Miles Davis", "Black Satin/What If/Agharta Prelude Dub", 448263054, "Miles Davis; Bill Laswell"),
		Track("Miles Davis", "Bitches Brew", 915057747, "Miles Davis"),
		Track(
				"Miles Davis",
				"Générique (from Ascenseur pour L'échafaud)",
				143859087,
				"Miles Davis",
				other_uses={987597831: HANGOUT_QUEST}
				),
		Track("John Coltrane", "Impressions", 230077180, "John Coltrane"),
		Track(
				"Charles Mingus",
				"Solo Dancer",
				1014236840,
				"Charles Mingus",
				),  # From the album The Black Saint and the Sinner Lady
		Track("Dexter Gordon", "Laura", 419089334, "David Raksin"),
		Track(
				"Chet Baker",
				"You Don't Know What Love Is",
				400388835,
				"Gene Depaul; Don Raye",
				other_uses={187092121: HANGOUT_QUEST, 397320180: "Konpeki Plaza Braindance"}
				),
		Track("Thelonious Monk", "Round Midnight", 487426870, "Thelonious Monk; Bernie Hanighen; Cootie Williams"),
		Track("Trio of Doom", "Dark Prince", 449864253, "John Mclaughlin", other_uses={395786567: RACES}),
		]

#: 92.9 Night FM
night_fm: list[Track] = [
		Track("Perilous Futur", "Dirty Roses", 664992914, "Kevin Hastings", "OnenO"),
		Track(
				"The Unresolved",
				"Worlds",
				188143271,
				"Sebastian Robertson, Daniel Davies",
				"SRDD (Sebastian Daniel)"
				),
		Track("The Unresolved", 'X', 52108015, "Sebastian Robertson; Daniel Davies", "SRDD (Sebastian Daniel)"),
		Track("Doctor Berserk", "Maniak", 592937823, "Fabian Velazquez", "Picasso"),
		Track("Generating Dependencies", "Me Machine", 621649083, "Kuba Sojka", "Poly Face"),
		Track("Lick Switch", "Like a Miracle", 791114400, "Earth Trax", "Earth Trax"),
		Track("Kings of Collapse", "Run", 649255606, "Steven Richard Davis", "Steven Richard Davis"),
		Track("Reviscerator", "Glitched Revelation", 521364565, "Procesor Plus", "Procesor Plus"),
		Track("Reviscerator", "Yellow Box", 884931314, "Procesor Plus", "Procesor Plus"),
		Track("The Bait", "Kill Kill", 84073683, "Kristina Michelle Olson", "Le Destroy"),
		Track(
				"Ashes Potts",
				"Flying Heads",
				710361138,
				"Ivan Iusco; Elena Charbila",
				"Kid Moxie; Ivan Iusco; Elena Charbila"
				),
		Track("Yards of the Moon", "Volcano the Sailor", 783271344, "Połoz", "Połoz"),
		Track("Cyber Coorayber", "Brain-Damaged", 239254618, "Nikola Nikita Jeremic", "Nikola Nikita Jeremic"),
		]

#: 95.2 Samizdat Radio
samizdat_radio: list[Track] = [
		Track(
				"Bara Nova",
				"Piling in my Head",
				185138126,
				"Nina Kraviz",
				"Nina Kraviz", {892337963: CLOUDS_MUSIC}
				),
		Track(
				"Bara Nova",
				"Delirium 2",
				625219838,
				"Nina Kraviz",
				"Nina Kraviz",
				{900420316: "mus_sq027_panam_csex_01_pre_sex", 439311782: "mus_sq027_panam_csex_01_pre_sex"}
				),
		Track("Bara Nova", "Harm Sweaty Pit", 928983117, "Nina Kraviz", "Nina Kraviz", {655028819: CLOUDS_MUSIC}),
		Track(
				"Bara Nova",
				"My Lullaby for You",
				740337697,
				"Nina Kraviz",
				"Nina Kraviz",
				{174026915: CLOUDS_MUSIC},
				),
		Track("Bara Nova", "Surprise Me, I'm Surprised Today", 822859958, "Nina Kraviz", "Nina Kraviz"),
		]

#: 96.1 Ritual FM
ritual_fm: list[Track] = [
		Track("V3RM1N", "Finis", 323048169, "Piotr Maciejewski (Drivealone)", "Piotr Maciejewski (Drivealone)"),
		Track("Dread Soul", "The Accursed", 969984534, "Antre", "Antre"),
		Track(
				"Bacillus",
				"March 30",
				643009039,
				"Tomb Mold",
				"Tomb Mold",
				),  # Also called Adaptive Manipulator outside the game.
		Track("Forlorn Scourge", "Acid Breather", 685504893, "Mastiff", "Mastiff"),
		Track("Nuclear Aura", "Witches of the Harz Mountains", 670708886, "Marcin Rybicki", "Marcin Rybicki"),
		Track("Weles", "The Loop", 381506730, "Deszcz", "Deszcz"),
		Track("Hysteria", "Scrum", 516709760, "Totenmesse", "Totenmesse"),
		Track("Inferno Corps", "Fuelled by Poison", 532284261, "Antigama", "Antigama", {544955296: JOHNNY_KERRY}),
		Track("Inferno Corps", "Kevin", 606018074, "Antigama", "Antigama"),
		Track("heXXXer", "Future Drugs", 620624990, "Entropia", "Entropia"),  # Or is the artist Mord'A'Stigmata?
		Track("Wydech", "Żurawie", 101839488, "Ugory", "Ugory"),
		Track(
				"Fist of Satan",
				"Abandoned Land",
				957306104,
				"Artur Rumiński; Haldor Grunberg",
				"Artur Rumiński; Haldor Grunberg"
				),
		Track(
				"Fist of Satan",
				"Black Concrete",
				114092930,
				"Artur Rumiński; Haldor Grunberg",
				"Artur Rumiński; Haldor Grunberg"
				),
		Track("Shattered Void", "I Won't Let You Go", 643641585, "Converge", "Converge"),
		]

#: 98.7 Body Heat Radio
body_heat_radio: list[Track] = [
		Track(
				"Clockwork Venus",
				"BM",
				1017973036,
				"SOPHIE; Shygirl; Sega Bodega; Kai Whiston",
				"SOPHIE; Shygirl",
				),  # Also called SLIME in the game credits and outside the game.
		Track("Neon Haze", "Circus Minimus", 903009003, "Jazelle Rodriguez; Deryk Mitchell; Erika Nuri", "Jvzel"),
		Track(
				"Window Weather",
				"Major Crimes",
				688260506,
				"Jake Duzsik; John Famiglietti; Lars Stalfors",
				"HEALTH",
				{41444121: DARK_MATTER}  # Also for Shy Delamain quest
				),
		Track("Artemis Delta", "Night City", 862539357, "Arielle Sitrick; Bill Burke", "R E L"),
		Track(
				"Hallie Coggins",
				"I Really Want To Stay At Your House",
				717186759,
				"Rosa Walton",
				"Rosa Walton (Let's Eat Grandma)",
				{670626837: HANGOUT_QUEST, 881817538: "mus_q105_fingers_01_source", 890846657: DARK_MATTER}
				),
		Track(
				"Point Break Candy",
				"Hole In The Sun",
				698612311,
				"Raney Shockne",
				"Raney Shockne feat. COS, Conway"
				),
		# TODO: Track("American Medical Association", "Bliind", 0, "Raney Shockne", "Raney Shockne"),
		Track(
				"Trash Generation",
				"History",
				941358832,
				"Gazelle Twin",
				"Gazelle Twin", {986982905: "mus_q000_corpo_standoff_source"}
				),
		Track("Lizzy Wizzy", "4ÆM", 5020242, "Grimes", "Grimes"),
		Track(
				"Lizzy Wizzy",
				"Delicate Weapon",
				726229946,
				"Grimes",
				"Grimes", {670923974: "Phantom Liberty Black Sapphire performance"}
				),
		Track("Us Cracks", "Ponpon Shit", 259328250, "Yuki Kawamura", "Namakopuri", {180075549: DARK_MATTER}),
		Track(
				"Us Cracks",
				"User Friendly",
				503548262,
				"Katarzyna Kraińska; Yuki Kawamura; Kaito Sakuma",
				"Namakopuri",
				{386020430: DARK_MATTER},
				),  # TODO: does this play on this station?
		Track(
				"Us Cracks feat. Kerry Eurodyne",
				"Off The Leash",
				235217575,
				"Kaito Sakuma; Yuki Kawamura; Tomas Shimizu (American Dream Express)",
				"Namakopuri & Damian Ukeje",
				{988042201: DARK_MATTER},
				),
		Track("IBDY", "Crustpunk", 949985077, "Rat Boy", "Rat Boy", {675780732: RACES}),
		Track("IBDY", "Here's a Thought", 575003013, "Rat Boy", "Rat Boy", {825809386: JOHNNY_KERRY}),
		]

#: 99.9 Impulse
impulse: list[Track] = [
		# TODO: songs list.
		Track(
				"Mr. Kipper",
				"DJ Set",
				424884909,
				),  # mus_radio_14_impulse_djset, also mus_radio_14impls_djset_pyramid_edit
		# Track("Mr. Kipper", "Walk Of Shame", 0, "Idris Elba", "Idris Elba"),
		# Track("Private Press", "Dreamy", 0, "Adam Brocki; Jan Wóycicki"),
		# Track("Private Press", "DEEEEEEP", 0, "Adam Brocki; Jan Wóycicki"),
		# Track("Private Press", "Black Labyrinth", 0, "Adam Brocki; Jan Wóycicki"),
		# Track("Private Press", "Feed Your Soul", 0, "Adam Brocki; Jan Wóycicki"),
		# Track("Private Press", "Liquid Disco", 0, "Adam Brocki; Jan Wóycicki"),
		# Track("Private Press", "Sleepy Dust", 0, "Adam Brocki; Jan Wóycicki"),
		# Track("Private Press", "Sparkling Frequency", 0, "Adam Brocki; Jan Wóycicki"),
		# Track("Private Press", "Undeniably Changes", 0, "Adam Brocki; Jan Wóycicki"),
		# Track("Private Press", "Void", 0, "Adam Brocki; Jan Wóycicki"),
		# Track("Private Press", "Woozee", 0, "Adam Brocki; Jan Wóycicki"),
		# Track("Private Press", "GREEEEEENHOUSE", 0, "Adam Brocki; Jan Wóycicki"),
		# Track("Private Press", "BESTPL", 0, "Adam Brocki; Jan Wóycicki"),
		# Track("Private Press", "ENERGEEHOUSE", 0, "Adam Brocki; Jan Wóycicki"),
		]

# TODO: or is it 101.0 like in the credits data
#: 101.9 The Dirge
the_dirge: list[Track] = [
		Track(
				"Kill Trigger feat. Paul Senai, KraKow",
				"The God Machines",
				660406395,
				"Sebastian Robertson; Daniel Davies; Tristan Calder; Brandon Hale; Michael Garcia",
				"Sebastian Robertson, Kill The Computer & Indijinouz"
				),
		Track(
				"NC3",
				"Blouses Blue",
				777673336,
				"Konrad Abramowicz",
				"Konrad OldMoney feat. Cidro Onetoo, Perry Porter"
				),
		Track("Young Kenny", "Problem Kids", 422374976, "Konrad Abramowicz", "Konrad OldMoney feat. Taelor Yung"),
		Track("Droox", "Bigger Man", 305730733, "Konrad Abramowicz", "Konrad OldMoney feat. Taelor Yung"),
		Track(
				"DNE feat. G'Natt",
				"Go Blaze",
				216704447,
				"Konrad Abramowicz",
				"Konrad OldMoney feat. Chanarah, Cidro Onetoo"
				),
		Track("ICHIBANCHI", "Dishonor", 495804559, "Konrad Abramowicz", "Konrad OldMoney feat. Brevner"),
		Track("Yamete", "Frost", 433713094, "Konrad Abramowicz", "Konrad OldMoney feat. Frawst"),
		Track(
				"UMVN feat. Imp Ra",
				"High School Bully",
				384046700,
				"Konrad Abramowicz",
				"Konrad OldMoney feat. Cidro Onetoo, Perry Porter"
				),
		Track(
				"DAPxFLEM",
				"NBOM",
				749562071,
				"Konrad Abramowicz",
				"Konrad OldMoney feat. Cidro Onetoo, Perry Porter"
				),
		Track("Code 137", "Suicide", 706423871, "Geno Lenardo", "Geno Lenardo feat. Zeale"),
		Track("HAPS", "Day of Dead", 279160746, "Konrad Abramowicz", "Konrad OldMoney feat. Taelor Yung"),
		Track("Knixit", "Bruzez", 960655358, "Konrad Abramowicz", "Konrad OldMoney feat. Johnny GR4VES"),
		Track(
				"Sugarcoob feat. ANAK KONDA",
				"Clip Boss",
				101795579,
				"Konrad Abramowicz",
				"Konrad OldMoney feat. Johnny GR4VES"
				),
		Track(
				"Triple-B feat. Gun-Fu",
				"PLUCK U",
				921768250,
				"Konrad Abramowicz",
				"Konrad OldMoney feat. Ded Stark"
				),
		Track("Pazoozu", "Hello Good Morning", 466119236, "Konrad Abramowicz", "Konrad OldMoney feat. S-God"),
		Track(
				"Bez Tatami feat. Gully Foyle",
				"Run The Block",
				39020019,
				"Konrad Abramowicz",
				"Konrad OldMoney feat. Taelor Yung"
				),
		Track(
				"Kyubik",
				"GR4VES",
				728377454,
				"Konrad Abramowicz",
				"Konrad OldMoney feat. Johnny GR4VES",
				),  # Check 3479
		Track(
				"Laputan Machine",
				"Warning Shots",
				761987513,
				"Konrad Abramowicz",
				"Konrad OldMoney feat. Perry Porter, Cidro Onetoo"
				),
		Track("Gorgon Madonna", "Metamorphosis", 274367834, "Yugen Blakrok", "Yugen Blakrok"),
		Track(
				"Yankee and the Brave",
				"No Save Point",
				595318736,
				"Michael Render",
				"Aniyah's Music",
				),  # Or is the artist Run The Jewels?
		Track(
				"TELO$",
				"Flacko Locko",
				344041802,
				"A$ap Rocky",
				"A$ap Rocky",
				),  # Also called 4Loko outside the game
		Track(
				"Cacimbo",
				"CCC",
				304807830,
				"Marek Walaszek & Dunia Hejneman",
				"Maro Music & Zuda",
				),  # TODO: not listed in the wiki; credits data has it under other songs not the station; TODO: check in game  # TODO: check 3506
		Track(
				"PeCero",
				"Nose Bleed",
				697396654,
				"Marek Walaszek & Okutama Akpan Etim",
				"Maro Music & Razzy Razo",
				),  # TODO: not listed in the wiki; credits data has it under other songs not the station; TODO: check in game
		]

#: 103.5 Radio PEBKAC
radio_pebkac: list[Track] = [
		Track("Error", "Bios", 254461336, "Jan Szarecki", "Louve"),
		Track("Sao Mai", "Drained", 450630849, "Rhys Fulber", "Rhys Fulber"),
		Track("Spoon Eater", "Subvert", 992013305, "Rhys Fulber", "Rhys Fulber"),
		Track(
				"Nablus",
				"Follow the White Crow",
				903459303,
				"Ivan Iusco; Elena Charbila",
				"Kid Moxie; Ivan Iusco; Elena Charbila"
				),
		Track("IOshrine", "Fake Spook", 854232133, "Kuba Sojka", "Poly Face"),
		Track("[flesh]reactor", "Move Dat", 472230949, "Kuba Sojka", "Poly Face"),
		Track("Bullet in the Head", "CANNIBALISMUS", 361407323, "Lutto Lento", "Lutto Lento"),
		Track("culteX", "La Canopée", 713386379, "Private Press", "Private Press"),
		Track("Skin<>Drifter", "Undertow Velocity", 104232706, "Private Press", "Private Press"),
		Track("Yards of the Moon", "II0I Break", 573266683, "Private Press", "Private Press", {784816738: RACES}),
		Track(
				"Retinal Scam",
				"Across the Floor",
				265347381,
				"Private Press",
				"Private Press",
				{252414463: JOHNNY_KERRY},
				),
		Track("Retinal Scam", "Gridflow", 789246932, "Private Press", "Private Press"),
		Track("Tar Hawk", "Vascular", 789477170, "Speed Dating", "Speed Dating feat. Horrid Charme"),
		Track("Tinnitus", "On My Way to Hell", 954776920, "Połoz", "Połoz", {371789278: "mus_sq011_totentanz_01"}),
		Track("Clockwork OS", "Stackoverflow", 28890981, "Bret Autrey", "Dos Era"),
		Track("Dukes of Azure", "Darkretro", 172754141, "Count", "Count"),
		]

#: 106.9 30 Principales
principales: list[Track] = [
		Track("Kartel Sonoro", "Bamo", 505436507, "Konrad Abramowicz", "Konrad OldMoney feat. Frawst"),
		Track(
				"Kartel Sonoro",
				"Dagga",
				507913744,
				"Konrad Abramowicz",
				"Konrad OldMoney feat. Cerbeus, Johnny GR4VES"
				),  # TODO: Check 3807
		Track("7 Facas", "Dinero", 7556210, "Konrad Abramowicz", "Konrad OldMoney feat. Cerbeus"),
		Track(
				"7 Facas",
				"Serpant",
				200129727,
				"Konrad Abramowicz",
				"Konrad OldMoney feat. Cerbeus, Johnny GR4VES"
				),
		Track(
				"Don Mara",
				"Tatted On My Face",
				626364837,
				"Konrad Abramowicz",
				"Konrad OldMoney feat. 37 Heartbreak"
				),
		Track("Big Machete", "Barrio", 973916952, "Konrad Abramowicz", "Konrad OldMoney"),
		Track("ChickyChickas", "Hood", 328370557, "Konrad Abramowicz", "Konrad OldMoney feat. Awrath"),
		Track("ChickyChickas", "Only Son", 398402575, "Konrad Abramowicz", "Konrad OldMoney feat. 37 Heartbreak"),
		Track(
				"Papito Gringo",
				"Muévelo / Cumbia",
				179243125,
				"David Perez",
				"David Rolas",
				),  # TODO: one file or two?
		Track("FKxU", "Muerto Trash", 858828322, "Konrad Abramowicz", "Konrad OldMoney feat. Blackheart NC"),
		Track("DJ CholoZ", "Westcoast Til I Die", 711322898, "Konrad Abramowicz", "Konrad OldMoney feat. Cerbeus"),
		]

#: 107.3 Morro Rock Radio
morro_rock_radio: list[Track] = [
		Track("Brutus Backlash", "Suffer Me", 360407664, "Chris Tapp", "The Cold Stares"),
		Track("XerzeX", "Heave Ho", 239971311, "Konrad Abramowicz", "Konrad OldMoney feat. Frawst"),
		Track("Beached Tarantula", "I Will Follow", 216269337, "Snot Abundance", "Snot Abundance"),
		Track("IBDY", "Who's Ready for Tomorrow", 688358243, "Rat Boy", "Rat Boy"),  # Pre 2.0 only?
		Track("IBDY", "Likewise", 92260188, "Rat Boy", "Rat Boy"),
		Track(
				"Rubicones",
				"Friday Night Fire Fight",
				534318699,
				"Jacques Barbot",
				"Aligns", {950011967: SOMEWHAT_DAMAGED_FLASHBACK}
				),
		Track("Rubicones", "Trauma", 146627573, "Jacques Barbot", "Aligns"),
		Track(
				"Blood and Ice",
				"Summer of 2069",
				395305747,
				"Metz",
				"Metz",
				),  # Also called Heaven's Gate when not in the game.
		Track(
				"Krushchev's Ghosts",
				"Testmaster / No Convenient Apocalypse",
				826126133,
				"Pissed Jeans",
				"Pissed Jeans",
				),
		Track("Cutthroat", "Sustain/Decay", 82962273, "Piotr Maciejewski", "Drivealone"),
		Track("Artificial Kids", "To the Fullest", 521529624, "The Unfit", "The Unfit"),
		Track("Fingers and the Outlaws", "So It Goes", 533813975, "Man Man", "Man Man"),
		Track(
				"SAMURAI",
				"Never Fade Away",
				230331069,
				"David Sandström; Kristofer Steen; P.T. Adamczyk; Dennis Lyxzén",
				"Refused",
				{904252670: "mus_q108_concert_glitch"},
				),
		Track(
				"SAMURAI",
				"Black Dog",
				847868585,
				"David Sandström; Kristofer Steen; Mattias Bärj; Dennis Lyxzén",
				"Refused",
				{661946813: "mus_q204_js_apartment_vinyl_01, during New Dawn Fades"},
				),
		Track(
				"SAMURAI",
				"Chippin' In",
				67866068,
				"David Sandström; Kristofer Steen; Dennis Lyxzén",
				"Refused",
				{
						1062521678: "mus_q110_chippinin",
						460511222: "mus_e3demo_end",
						350111750: "mus_q115_chippin_in",
						28560079: "mus_q001_v_apartment_chippin_in",
						961827496: "mus_q110_chippinin"
						}
				),
		Track(
				"SAMURAI",
				"The Ballad Of Buck Ravers",
				336551383,
				"David Sandström; Kristofer Steen; P.T. Adamczyk; Dennis Lyxzén",
				"Refused",
				{47509183: JOHNNY_KERRY},  # Also mus_q204_js_apartment_vinyl_01, during New Dawn Fades
				),
		]

# TODO: check against credits
#: 107.5 Dark Star
dark_star: list[Track] = [
		Track(
				"Mr. Kipper",
				"Choke Hold",
				30149432,
				'',
				"Idris Elba",
				{
						938547930: MUS_OW_PHONE,
						527795061: "mus_mq301_car_cmb_source",
						904203946: "mus_mq301_car_cmb_source"
						}
				),
		Track("BADPANNINI", "Headrush", 661309522, '', "Backxwash"),
		Track(
				"No Strings Attached",
				"Orbital Insertion",
				747444235,
				'',
				"Hagop Tchaparian", {150643485: "mus_q303_restaurant_01"}
				),
		Track("Bwana Mungu", "Cyko Arctic", 750285308, '', "Lord Spikeheart, Chrisman"),
		Track("OLO Y", "Pierwszy raz naprawdę", 22550244, '', "27.Fuckdemons", {211308495: MUS_OW_PHONE}),
		Track("DJ papergekko", "NUCLEAR DREAMLAND", 329846451, '', "julek ploski", {503455989: MUS_OW_PHONE}),
		Track("Mr. Kipper", "Rollacoaster", 569092571, '', "Idris Elba"),  # AKA Rolla
		Track(
				"Ecko Frequency",
				"IKARI",
				307219088,
				'',
				"Ecko Bazz, Silkback",
				{615284999: MUS_OW_PHONE},
				),  # AKA Zuuka
		Track("Her Mashewsky", "fabrica KOSMOS", 766230008, '', "Kuba Wandacjpwocz", {308385266: MUS_OW_PHONE}),
		Track("Walt Air", "dRk", 554215322, '', "Krzysztof Freeze Ostrowski"),
		Track("Mightonauts", "Minion Sex", 483528050, '', "T'len Lai"),
		Track("DJ papergekko", "Bigger Crimes", 71696280, '', "julek ploski"),
		Track("Łotr", "Memories of Mzuzu", 617780730, '', "Połoz"),
		]

#: Other songs.
misc: list[Track] = [
		Track(
				"P.T. Adamczyk & Sora Lion",
				"Hardest To Be",
				1032568254,
				"P.T. Adamczyk & Sora Lion",
				other_uses={
						762143559: HANGOUT_QUEST,
						44152296: "mus_ep1_credits",
						},  # 1032568254: "mus_q304_alex_heart_to_heart",
				),  # TODO: find correct main ID
		Track("P.T. Adamczyk & Dawid Podsiadło", "Phantom Liberty", 904740609, "P.T. Adamczyk, Dawid Podsiadło"),
		# TODO: Track("SAMURAI", "Archangel", 0, "David Sandström; Kristofer Steen; Dennis Lyxzén", "Refused"),
		Track("Kerry Eurodyne", "Boat Song", 341588624, '', ''),  # TODO: credits
		Track(
				"Kerry Eurodyne",
				"Chippin' In",
				750744602,
				"Borys Pugacz-Muraszkiewicz; P.T. Adamczyk",
				"Damian Ukeje; P.T. Adamczyk"
				),
		Track(
				"Footage Missing",
				"When It's War",
				925140962,
				"Trevor Samuels & Marek Walaszek",
				"Deadly Hunta & Maro Music"
				),  # TODO: check IDs; had extra ID but it was rain sounds
		Track("Erik Satie", "Gymnopédie No. 1", 776355648, "Erik Satie"),
		Track("Frédéric Chopin", "Nocturne Op. 55 No. 1", 768869823, "Frédéric Chopin"),
		Track("Claude Debussy", "Clair de Lune", 273382915, "Claude Debussy"),
		Track("P.T. Adamczyk feat. Olga Jankowska", "Never Fade Away", 1067066079, '', ''),  # TODO: credits
		Track(
				"SAMURAI",
				"A Like Supreme",
				905498026,  # mus_q204_js_apartment_vinyl_01, during New Dawn Fades
				"David Sandström; Kristofer Steen; Dennis Lyxzén",
				"Refused",
				),
		# TODO: Track("Nomad Spirit", "Katarzyna Kraińska", 0, "P.T. Adamczyk"),
		Track(
				"Baron Celine",
				"RATATATA",
				198353675,
				"Marek Aureliusz Teodoruk & Baron Black",
				"Baron Black & Auer"
				),  # mus_custom_radio_ratatata and mus_q110_voodooboys_market; plays on radio in Pacifica  # TODO: credits
		# TODO: Track("Guilt Code", "Neuron", 0, "Marek Aureliusz Teodoruk", "Auer"),
		Track(
				"CD Projekt Red",
				"Radio Synthwave GNH1",
				125084733,
				),  # TODO: find which station these play on (with copyrighted music disabled)
		Track(
				"CD Projekt Red",
				"Radio Synthwave GNH2",
				714642933,
				),  # TODO: find which station these play on (with copyrighted music disabled)
		Track(
				"CD Projekt Red",
				"Radio Synthwave GNH3",
				796147433,
				),  # TODO: find which station these play on (with copyrighted music disabled)
		Track(
				"CD Projekt Red",
				"Radio Synthwave GNH4",
				295168116,
				),  # TODO: find which station these play on (with copyrighted music disabled)
		Track(
				"CD Projekt Red",
				"Radio Synthwave GNH5",
				718643010,
				),  # TODO: find which station these play on (with copyrighted music disabled)
		Track(
				"CD Projekt Red",
				"mus_radio_03_electind_ppgame18",
				176501448,
				),  # TODO should be radio, maybe with copyrighted music disabled. Find station
		Track(
				"CD Projekt Red",
				"mus_radio_03_elec_ind_neuron",
				805938280,
				),  # TODO should be radio, maybe with copyrighted music disabled. Find station
		Track(
				"Stryjo",
				"Nieczuły parostatek",
				379273238,
				'',
				'',
				{594710394: HANGOUT_QUEST},
				),  # 1664 plays on Jazz station if copyrighted music disabled  # TODO: find main ID
		Track(
				"CD Projekt Red",
				"Laura (Instrumental)",
				1015556788,
				"David Raksin",
				),  # if copyrighted music disabled; mus_radio_08_jazz_laura  # TODO: artist
		Track(
				"CD Projekt Red",
				"You Don't Know What Love Is (Instrumental)",
				403896296,
				"Gene Depaul; Don Raye",
				other_uses={1041056699: HANGOUT_QUEST},
				),  # if copyrighted music disabled  # TODO: artist
		]

#: Mapping of station names to tracklists.
radio_stations: dict[str, list[Track]] = {
		"88.9 Pacific Dreams": pacific_dreams,
		"89.3 Radio Vexelstrom": radio_vexelstrom,
		"89.7 Growl FM": growl_fm,
		"91.9 Royal Blue Radio": royal_blue_radio,
		"92.9 Night FM": night_fm,
		"95.2 Samizdat Radio": samizdat_radio,
		"96.1 Ritual FM": ritual_fm,
		"98.7 Body Heat Radio": body_heat_radio,
		"99.9 Impulse": impulse,
		"101.9 The Dirge": the_dirge,
		"103.5 Radio PEBKAC": radio_pebkac,
		"106.9 30 Principales": principales,
		"107.3 Morro Rock Radio": morro_rock_radio,
		"107.5 Dark Star": dark_star,
		"misc": misc,
		}

radio_jingle_ids: dict[str, Sequence[int]] = {
		"101.9 The Dirge": (789210352, 53171054, 994411021),
		"107.5 Dark Star": (165565468, 771183218, 478850173, 99989307),
		"98.7 Body Heat Radio": (679337608, 936720723, 915927353),
		"95.2 Samizdat Radio": (789557574, 848658177, 957429891),
		"92.9 Night FM": (259224498, 236812550, 818146679, 837456452, 124957938),
		"96.1 Ritual FM": (752675320, 686466489, 88070376, 180892104),
		"88.9 Pacific Dreams": (128841128, 750587894, 1004904231),
		"89.3 Radio Vexelstrom": (130404871, 885647302, 339209955, 938562027),
		"106.9 30 Principales": (91143381, 922727393, 25396109),
		"91.9 Royal Blue Radio": (197336484, 66052711, 272220110, 119313970, 712496434),
		"103.5 Radio PEBKAC": (615874745, 493162163, 445903319),
		}
"""
Wem file names for radio station jingles.

Files are located in ``audio_2_soundbanks.archive`` at ``base\\sound\\soundbanks\\media\\{wem_name}.wem``
"""
