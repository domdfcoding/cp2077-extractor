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
from mutagen.id3 import (
		APIC,
		COMM,
		ID3,
		TALB,
		TCMP,
		TCOM,
		TDRC,
		TIT2,
		TOPE,
		TPE1,
		TPE2,
		Encoding,
		Frame,
		ID3NoHeaderError
		)

__all__ = ["Track", "set_tag"]


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

		transmap = {ord(k): ord('_') for k in '\\?%*:|"<>'}
		return f"{self.artist} - {self.title}".replace('/', ' ').translate(transmap)

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

		try:
			tags = ID3(mp3_filename)
		except ID3NoHeaderError:
			tags = ID3()

		tags_changed: bool = any([
				set_tag(TPE1, self.artist, tags),
				set_tag(TIT2, self.title, tags),
				set_tag(TOPE, self.real_artist, tags),
				set_tag(TCOM, self.writer, tags),
				set_tag(TALB, station, tags),
				set_tag(TCMP, '1', tags),
				set_tag(TDRC, "2023", tags),
				set_tag(TPE2, "Various Artists", tags),
				])

		if "COMM::XXX" not in tags or str(tags["COMM::XXX"]) != "From Cyberpunk 2077":
			tags.add(COMM(encoding=Encoding.UTF8, text="From Cyberpunk 2077"))
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


def set_tag(
		tag: type[Frame],
		value: str,
		tags: ID3,
		) -> bool:
	"""
	Set the tag if the value in the existing tags differs.

	:param tag:
	:param value:
	:param tags:

	:returns: Whether the value in the tags has been changed, to inform whether to write tags to file.
	"""

	if not value.strip():
		return False

	tag_name = tag.__name__

	if tag_name not in tags or str(tags[tag_name]) != value:
		tags.add(tag(encoding=Encoding.UTF8, text=value))
		return True

	return False
