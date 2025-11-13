#!/usr/bin/env python3
#
#  track.py
"""
Track metadata.
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
from collections.abc import Mapping, Sequence
from types import MappingProxyType
from typing import NamedTuple

# 3rd party
from domdf_python_tools.paths import PathPlus
from mutagen.id3 import ID3, TALB, TCMP, TCOM, TDRC, TIT2, TOA, TPE1, TPE2, Encoding

__all__ = ["Track"]


class Track(NamedTuple):
	artist: str
	title: str
	wem_name: int
	extra_ids: Sequence[int] = ()
	writer: str = ''
	real_artist: str = ''
	other_uses: Mapping[int, str] = MappingProxyType({})  # Mapping of wem_name to usage.

	def set_id3_metadata(self, mp3_filename: PathPlus, station: str) -> None:
		tags = ID3(mp3_filename)
		tags.add(TPE1(encoding=Encoding.UTF8, text=self.artist))
		tags.add(TIT2(encoding=Encoding.UTF8, text=self.title))
		tags.add(TOA(encoding=Encoding.UTF8, text=self.real_artist))
		tags.add(TCOM(encoding=Encoding.UTF8, text=self.writer))
		tags.add(TALB(encoding=Encoding.UTF8, text=station))
		tags.add(TCMP(encoding=Encoding.UTF8, text='1'))
		tags.add(TDRC(encoding=Encoding.UTF8, text="2023"))
		tags.add(TPE2(encoding=Encoding.UTF8, text="Various Artists"))
		# TODO: only save if changes made from tags read in.
		tags.save(mp3_filename)
