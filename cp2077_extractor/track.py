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
from mutagen.id3 import APIC, COMM, ID3, TALB, TCMP, TCOM, TDRC, TIT2, TOPE, TPE1, TPE2, Encoding

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
		tags_changed: bool = False

		if "TPE1" not in tags or str(tags["TPE1"]) != self.artist:
			tags.add(TPE1(encoding=Encoding.UTF8, text=self.artist))
			# print("TPE1 changed")
			tags_changed = True

		if "TIT2" not in tags or str(tags["TIT2"]) != self.title:
			tags.add(TIT2(encoding=Encoding.UTF8, text=self.title))
			# print("TIT2 changed")
			tags_changed = True

		if self.real_artist:
			if "TOPE" not in tags or str(tags["TOPE"]) != self.real_artist:
				tags.add(TOPE(encoding=Encoding.UTF8, text=self.real_artist))
				# print("TOA changed")
				tags_changed = True

		if self.writer:
			if "TCOM" not in tags or str(tags["TCOM"]) != self.writer:
				tags.add(TCOM(encoding=Encoding.UTF8, text=self.writer))
				# print("TCOM changed")
				tags_changed = True

		if "TALB" not in tags or str(tags["TALB"]) != station:
			tags.add(TALB(encoding=Encoding.UTF8, text=station))
			# print("TALB changed")
			tags_changed = True

		if "TCMP" not in tags or str(tags["TCMP"]) != '1':
			tags.add(TCMP(encoding=Encoding.UTF8, text='1'))
			# print("TCMP changed")
			tags_changed = True

		if "TDRC" not in tags or str(tags["TDRC"]) != "2023":
			tags.add(TDRC(encoding=Encoding.UTF8, text="2023"))
			# print("TDRC changed")
			tags_changed = True

		if "TPE2" not in tags or str(tags["TPE2"]) != "Various Artists":
			tags.add(TPE2(encoding=Encoding.UTF8, text="Various Artists"))
			# print("TPE2 changed")
			tags_changed = True

		if "COMM::XXX" not in tags or str(tags["COMM::XXX"]) != "From Cyberpunk 2077":
			tags.add(COMM(encoding=Encoding.UTF8, text="From Cyberpunk 2077"))
			# print("COMM changed")
			tags_changed = True

		if album_art:
			if isinstance(album_art, bytes):
				album_art_bytes = album_art
			else:
				album_art_bytes = PathPlus(album_art).read_bytes()

			if "APIC:Cover" not in tags or tags["APIC:Cover"].data != album_art_bytes:
				tags.delall("APIC")  # TODO: APCI:Cover?
				tags.add(APIC(encoding=0, mime="image/png", type=3, desc="Cover", data=album_art_bytes))
				tags_changed = True

		if tags_changed:
			tags.save(mp3_filename)
