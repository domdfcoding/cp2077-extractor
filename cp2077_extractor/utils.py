#!/usr/bin/env python3
#
#  utils.py
"""
General utility functions.
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
import itertools
import os
import pprint
import re
import subprocess
from collections import Counter
from typing import Any

# 3rd party
import regex as re
import sox  # type: ignore[import]
from domdf_python_tools.paths import PathPlus

__all__ = [
		"prepare_ids",
		"remove_extra_files",
		"set_id_filename_in_directory",
		"to_snake_case",
		"transcode_file"
		]


def prepare_ids(radio_stations: dict[str, Any], *other_ids) -> tuple[
		set[int],
		set[int],
		set[int],
		]:
	target_file_ids: set[int] = set(itertools.chain(*(station.keys() for station in radio_stations.values())))
	extra_file_ids: set[int] = set()
	for station in radio_stations.values():
		for track_data in station.values():
			try:
				extra_file_ids.update(track_data[3])
			except:
				print(track_data)
				raise

	all_ids: list[int] = [int(i) for i in (*target_file_ids, *extra_file_ids) if i]
	for id_set in other_ids:
		all_ids.extend(map(int, id_set))

	res = {num: freq for num, freq in Counter(all_ids).items() if freq > 1}
	if res:
		raise ValueError(f"Error: duplicated IDs (with frequency)\n{pprint.pformat(res)}")

	return target_file_ids, extra_file_ids, set(all_ids)


def transcode_file(
		wem_filename: PathPlus,
		mp3_filename: PathPlus,
		length_range: tuple[int, int],
		) -> None:
	"""
	Transcode a WWise ``.wem`` file to mp3 at 256kbps.

	:param wem_filename:
	:param mp3_filename:
	:param length_range: Files with durations in seconds outside this range will be skipped.
	"""

	ogg_filename = wem_filename.with_suffix(".ogg")

	wem_meta = subprocess.check_output(["./vgmstream-cli", "-m", wem_filename]).decode("UTF-8")
	m = re.match(r": \d+ samples \((.*) seconds\)", wem_meta.split("play duration", 1)[1])
	if m:
		length_mins, length_secs = map(float, m.group(1).split(':'))
		length = length_mins * 60 + length_secs
		if length < length_range[0] or length > length_range[1]:
			# print("Skip wem; too short or too long")
			return

	print(wem_filename, "->", mp3_filename)
	# TODO: subprocess
	os.system(f"./vgmstream-cli -o {ogg_filename} {wem_filename}")
	length = sox.file_info.duration(ogg_filename)
	if length_range[1] >= length >= length_range[0]:
		subprocess.check_output([
				"ffmpeg",
				"-i",
				ogg_filename,
				"-c:a",
				"libmp3lame",
				"-b:a",
				"256k",
				mp3_filename,
				])
	# else:
	# 	print("Skip ogg; too short or too long")


def remove_extra_files(directory: PathPlus, target_ids: set[int]) -> None:
	for file_id in {int(x.stem) for x in directory.iterdir()} - target_ids:
		directory.joinpath(str(file_id) + ".mp3").unlink()


def set_id_filename_in_directory(
		directory: PathPlus,
		mp3_filename: PathPlus,
		file_id: str,
		) -> PathPlus:
	new_filename = directory.joinpath(str(file_id) + ".mp3")
	if mp3_filename.is_file():
		mp3_filename.rename(new_filename)
	return new_filename


_case_boundary_re = re.compile("(\\p{Ll})(\\p{Lu})")
_single_letters_re = re.compile("(\\p{Lu}|\\p{N})(\\p{Lu})(\\p{Ll})")


def to_snake_case(value: str):
	# Matches VSCode behaviour
	case_boundary = _case_boundary_re.findall(value)
	single_letters = _single_letters_re.findall(value)
	if not case_boundary and not single_letters:
		return value
	value = _case_boundary_re.sub(r"\1_\2", value)
	value = _case_boundary_re.sub(r"\1_\2\3", value)
	return value.lower()
