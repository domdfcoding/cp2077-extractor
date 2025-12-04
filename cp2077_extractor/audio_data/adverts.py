#!/usr/bin/env python3
#
#  advert_data.py
"""
Data for audio for adverts that play on animated billboards.
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
from typing import NamedTuple

__all__ = ["AdvertData", "adverts"]


class AdvertData(NamedTuple):
	"""
	Data for an advert's sound files.
	"""

	#: The filenames in the game files (in ``base/localization/en-us/vo`` or ``base\localization\common\vo``) for this advert all start with this string.
	audio_filename_prefix: str

	#: The name of the scene file in ``base/media/animated_billboards/scenes`` in the game files (with the suffix ``.scene``.)
	scene_file: str

	general_audio: bool = False
	"""
	Whether the audio is common too all game languages.

	:py:obj:`False` for localised audio, :py:obj:`True` for files in ``audio_1_general.archive``.
	"""


#: Data for audio for adverts that play on animated billboards.
adverts: dict[str, AdvertData] = {
		"all_foods": AdvertData("ad_all_foods_ab_ad_caliente", "ab_q003_01_all_foods_meat_ad"),
		"arasaka": AdvertData(
				"ad_arasaka_ab_ad_caliente",
				"ab_sq032_01_arasaka_propaganda",
				),  # ab_q115_01_arasaka_propaganda
		"captain_caliente": AdvertData("ad_captain_caliente_ab_ad_caliente", "ab_ad_caliente"),  # TODO: Check
		"chromanticore": AdvertData("ad_chromanticore_ab_ad_chromanticore", "ab_ad_chromanticore"),
		"foreign_body": AdvertData("ad_foreign_body_ab_ad_foreign_body", "ab_ad_foreign_body"),
		"kang_tao": AdvertData("ad_kang_tao_ab_ad_caliente", "ab_q104_01_kang_tao_ad"),
		"lizzies_bar": AdvertData("ad_lizzies_bar_ab_ad_caliente", "ab_q004_01_lizzies_bar_ad"),
		"mrstud": AdvertData("ad_mrstud_ab_ad_mrstud", "ab_ad_mrstud"),
		"mrwhitey": AdvertData("ad_mrwhitey_ab_ad_mrwhitey", "ab_ad_mrwhitey"),
		"nicola": AdvertData("ad_nicola_female_ab_ad_nicola", "ab_ad_nicola"),
		"night_corp": AdvertData("ad_night_corp_ab_ad_caliente", "ab_q114_01_night_corp_ad"),
		"orgiatic": AdvertData("ad_orgiatic_male_ab_ad_orgiatic", "ab_ad_orgiatic"),
		"slaughterhouse": AdvertData("ad_slaughterhouse_ab_ad_slaughterhouse", "ab_ad_slaughterhouse"),
		"sojasil": AdvertData("ad_sojasil_ab_ad_sojasil", "ab_ad_sojasil"),
		"televangelist": AdvertData("ad_televangelist_ab_ad_caliente", "ab_sts_wat_nid_04_televangelist_ad"),
		"thrud": AdvertData("ad_thrud_ab_ad_thrud", "ab_ad_thrud"),
		"tiancha": AdvertData("ad_tiancha_ab_ad_tiancha", "ab_ad_tiancha"),
		"vargas": AdvertData("ad_vargas_ab_ad_vargas", "ab_ad_vargas"),
		"watson_whore": AdvertData("ad_watson_whore_ab_ad_caliente", "ab_ad_watson_whore"),
		"us_cracks": AdvertData("civ_mid_f_60_jap_25_ab_ad_caliente", "ab_sq017_01_us_cracks_ad"),
		"crystal_palace": AdvertData("ziggy_q_q203_01_crystal_palace_info", "q203_01_crystal_palace_info"),
		"delamain": AdvertData("delamain_ab_ad_caliente", "ab_sq025_01_delamain_ad"),  #
		# TODO: 'jefferson_peralez': AdvertData('jefferson_peralez_jefferson_peralez_ad', ),
		}
