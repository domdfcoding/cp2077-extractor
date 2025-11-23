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
import os
import pathlib
from collections.abc import Mapping
from types import MappingProxyType
from typing import NamedTuple

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from mutagen.id3 import APIC, COMM, ID3, TALB, TCMP, TCOM, TDRC, TIT2, TOA, TPE1, TPE2, Encoding

__all__ = ["Track"]


class Track(NamedTuple):
	"""
	Represents an audio track played on the radio etc.
	"""

	artist: str
	title: str
	wem_name: int
	writer: str = ''
	real_artist: str = ''

	#: Mapping of WEM file names to usage.
	other_uses: Mapping[int, str] = MappingProxyType({})

	@property
	def filename_stub(self) -> str:
		"""
		Track filename (without suffix), comprising the artist and track title and made filename safe.
		"""

		return f"{self.artist} - {self.title}".replace('/', ' ')

	def set_id3_metadata(
			self,
			mp3_filename: PathLike,
			station: str,
			album_art: str | pathlib.Path | os.PathLike[str] | bytes | None = None,
			) -> None:
		"""
		Set ID3 tags on the file (artist, title, performer, writer/composer, album/station, etc.).

		:param mp3_filename: The file to set metadata on.
		:param station: The name of the radio station, used as the album name.
		:param album_art: Either the path to the album art file or the raw bytes of the album art, in PNG format. Optional.
		"""

		tags = ID3(mp3_filename)
		tags.add(TPE1(encoding=Encoding.UTF8, text=self.artist))
		tags.add(TIT2(encoding=Encoding.UTF8, text=self.title))
		tags.add(TOA(encoding=Encoding.UTF8, text=self.real_artist))
		tags.add(TCOM(encoding=Encoding.UTF8, text=self.writer))
		tags.add(TALB(encoding=Encoding.UTF8, text=station))
		tags.add(TCMP(encoding=Encoding.UTF8, text='1'))
		tags.add(TDRC(encoding=Encoding.UTF8, text="2023"))
		tags.add(TPE2(encoding=Encoding.UTF8, text="Various Artists"))
		tags.add(COMM(encoding=Encoding.UTF8, text="From Cyberpunk 2077"))

		if album_art:
			if isinstance(album_art, bytes):
				album_art_bytes = album_art
			else:
				album_art_bytes = PathPlus(album_art).read_bytes()

			tags.delall("APIC")
			tags.add(APIC(encoding=0, mime="image/png", type=3, desc="Cover", data=album_art_bytes))

		# TODO: only save if changes made from tags read in.
		tags.save(mp3_filename)
