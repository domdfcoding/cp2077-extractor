#!/usr/bin/env python3
#
#  __init__.py
r"""
Data for radio stations, ambient music, etc.

Audio files are located in ``audio_2_soundbanks.archive`` at ``base\sound\soundbanks\media\{wem_name}.wem``
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

# stdlib
from collections.abc import Iterator
from typing import Any, Protocol, SupportsIndex, overload

# this package
from .radio_stations import (
		CLOUDS_MUSIC,
		DARK_MATTER,
		HANGOUT_QUEST,
		JOHNNY_KERRY,
		MUS_OW_PHONE,
		RACES,
		SOMEWHAT_DAMAGED_FLASHBACK,
		SOMEWHAT_DAMAGED_FLASHBACK_REED,
		radio_stations
		)

__all__ = [
		"SceneAudioData",
		"intro_ids",
		"nomad_bard_ids",
		"clouds_music_ids",
		"somewhat_damaged_flashback_ids",
		"sex_cutscene_music_ids",
		"hangout_music_ids",
		"race_music_ids",
		"mus_ow_phone_ids",
		"dark_matter_music_ids",
		"johnny_kerry_music_ids",
		]

#: Mapping of wem file names to languages for the game intro audio.
intro_ids: dict[int, str] = {
		# Intros in foreign languages
		193250534: "Korean",
		212033934: "German",
		228132900: "Japanese",
		521504529: "Russian",
		533464258: "English",
		634636526: "Spanish",
		731319179: "Chinese",
		835783005: "Polish",
		964673994: "Portugese",
		1038719001: "French",
		1052911782: "Italian",
		}

# mus_q114_nomad_bard_01_song_01, plays during We Gotta Live Together (Aldecaldos ending)
#: Mapping of wem file names to language (or the guitar part) for Jake Scooter playing during the quest *We Gotta Live Together*.
nomad_bard_ids: dict[int, str] = {
		422912739: "German",  # mus_q114_nomad_bard_01_song_01/mus_q114_nomad_bard_01_song
		717901062: "Korean",  # mus_q114_nomad_bard_01_song_01/mus_q114_nomad_bard_01_song
		788187980: "English",  # mus_q114_nomad_bard_01_song_01/mus_q114_nomad_bard_01_song
		791357735: "French",  # mus_q114_nomad_bard_01_song_01/mus_q114_nomad_bard_01_song
		804002160: "Spanish",  # mus_q114_nomad_bard_01_song_01/mus_q114_nomad_bard_01_song
		845132118: "Portugese",  # mus_q114_nomad_bard_01_song_01/mus_q114_nomad_bard_01_song
		85588625: "Chinese",  # mus_q114_nomad_bard_01_song_01/mus_q114_nomad_bard_01_song
		884356362: "Japanese",  # mus_q114_nomad_bard_01_song_01/mus_q114_nomad_bard_01_song
		992577309: "Polish",  # mus_q114_nomad_bard_01_song_01/mus_q114_nomad_bard_01_song
		113512491: "Italian",  # mus_q114_nomad_bard_01_song_01/mus_q114_nomad_bard_01_song
		223185989: "Russian",  # mus_q114_nomad_bard_01_song_01/mus_q114_nomad_bard_01_song
		274240532: "Korean (2)",  # mus_q114_nomad_bard_01_song_01/mus_q114_nomad_bard_01_song
		377542210: "guitar",  # mus_q114_nomad_bard_01_song_01/mus_q114_nomad_bard_01_song
		308885281: "guitar (2)",  # mus_q114_nomad_bard_01_song
		352828163: "guitar (3)",  # mus_q114_nomad_bard_01_song
		}

# mus_q105_dollhouse
#: Music that plays in Clouds.
clouds_music_ids: dict[int, str] = {
		394385544: "mus_q105_dollhouse_394385544",
		643987762: "mus_q105_dollhouse_643987762",
		}

#: Music that plays in the flashbacks during the quest *Somewhat Damaged*.
somewhat_damaged_flashback_ids: dict[int, str] = {
		180066973: "mus_q305_brooklyn_vinyl_01_180066973",
		22001095: "mus_q305_brooklyn_party_22001095",
		}

#: Music that plays in the flashbacks during sex cutscenes.
sex_cutscene_music_ids: dict[int, str] = {
		415608881: "mus_generic_sexcs_01_415608881",  # Joytoy fire?
		851644048: "mus_sq030_judy_csex_851644048",  # Guitar and drums and humming
		176338671: "mus_stout_sexcs_01_176338671",  # Hole In The Sun (excerpt)
		}

#: Music that plays during the *I Really Wanna Stay At Your House* quest.
hangout_music_ids: dict[int, str] = {}

#: Music that plays during the *The Beast In Me* quests.
race_music_ids: dict[int, str] = {}

#: Unknown
mus_ow_phone_ids: dict[int, str] = {}

#: Music that plays in Dark Matter during the *Off the Leash* quest.
dark_matter_music_ids: dict[int, str] = {}

#:
johnny_kerry_music_ids: dict[int, str] = {}

for station, station_data in radio_stations.items():
	for track in station_data:
		if not track.other_uses:
			continue
		for wem_name, use in track.other_uses.items():
			if use == HANGOUT_QUEST:
				hangout_music_ids[wem_name] = f"{use}_{wem_name}"
			elif use == RACES:
				race_music_ids[wem_name] = f"{use}_{wem_name}"
			elif use == MUS_OW_PHONE:
				mus_ow_phone_ids[wem_name] = f"{use}_{wem_name}"
			elif use in {SOMEWHAT_DAMAGED_FLASHBACK, SOMEWHAT_DAMAGED_FLASHBACK_REED}:
				somewhat_damaged_flashback_ids[wem_name] = f"{use}_{wem_name}"
			elif use == CLOUDS_MUSIC:
				clouds_music_ids[wem_name] = f"{use}_{wem_name}"
			elif use == DARK_MATTER:
				dark_matter_music_ids[wem_name] = f"{use}_{wem_name}"
			elif use == JOHNNY_KERRY:
				johnny_kerry_music_ids[wem_name] = f"{use}_{wem_name}"
			elif use in {"mus_sq027_panam_csex_01_pre_sex"}:
				sex_cutscene_music_ids[wem_name] = f"{use}_{wem_name}"
			elif use in {
					"mus_ep1_credits",
					"mus_q303_restaurant_01",
					"mus_mq301_car_cmb_source",
					"mus_q001_v_apartment_chippin_in",
					"mus_q115_chippin_in",
					"mus_e3demo_end",
					"mus_q110_chippinin",
					"mus_q204_js_apartment_vinyl_01, during New Dawn Fades",
					"mus_q108_concert_glitch",
					"mus_sq011_totentanz_01",
					"Phantom Liberty Black Sapphire performance",
					"Parade and Wako's briefing",
					"Konpeki Plaza Braindance",
					"mus_q105_fingers_01_source",
					"mus_q000_corpo_standoff_source"
					}:
				pass  # TODO
			else:
				raise NotImplementedError(use)


class SceneAudioData(Protocol):
	"""
	Protocol for classes such as :class:`~.AdvertData` and :class:`~.DJData`.
	"""

	@property
	def audio_filename_prefix(self) -> str: ...

	@property
	def scene_file(self) -> str: ...

	@property
	def general_audio(self) -> bool: ...

	@overload
	def __getitem__(self, __key: SupportsIndex) -> str | bool: ...

	@overload
	def __getitem__(self, __key: "slice[Any, Any, Any]") -> tuple[str | bool, ...]: ...

	def __iter__(self) -> Iterator: ...
