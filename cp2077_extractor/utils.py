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
import random
from collections import deque
from io import BytesIO
from typing import Deque, Generic, TypeVar

# 3rd party
import lameenc  # type: ignore[import-not-found]
import regex as re  # type: ignore[import-untyped]
from domdf_python_tools.paths import PathPlus
from miniaudio import SoundFileInfo, vorbis_get_info, vorbis_read  # type: ignore[import-untyped]
from mutagen.id3 import ID3, TLEN
from wem2ogg import wem_to_ogg

__all__ = ["InfiniteList", "StringReader", "to_snake_case", "transcode_file"]

try:
	# 3rd party
	from kraken_decompressor import decompress
except ImportError:

	def decompress(src: bytes, dst_len: int) -> bytes:
		raise NotImplementedError(
				"Kraken decompression unavailable ('kraken-decompressor' not installed or unsupported platform)"
				)


def transcode_file(
		wem_filename: PathPlus,
		mp3_filename: PathPlus,
		length_range: tuple[int, int] | None = None,
		) -> None:
	"""
	Transcode a WWise ``.wem`` file to mp3 at 256kbps.

	Requires ``ffmpeg`` to be installed.

	:param wem_filename:
	:param mp3_filename:
	:param length_range: Files with durations in seconds outside this range will be skipped.
	"""

	# TODO: see how vgmstream gets length; probably in file header

	# print(wem_filename, "->", mp3_filename)
	ogg_data = wem_to_ogg(wem_filename.read_bytes())
	ogg_info: SoundFileInfo = vorbis_get_info(ogg_data)
	# print("nchannels =", ogg_info.nchannels)
	# print("sample_rate =", ogg_info.sample_rate)
	# print("sample_width =", ogg_info.sample_width)
	# print("num_frames =", ogg_info.num_frames)
	# print("duration =", ogg_info.duration)  # Seconds
	# print("sub_format =", ogg_info.sub_format)

	length = ogg_info.duration
	if not length_range or (length_range[1] >= length >= length_range[0]):

		pcm_data = bytes(vorbis_read(data=ogg_data).samples)

		encoder = lameenc.Encoder()
		encoder.set_bit_rate(256)
		# encoder.set_in_sample_rate(sample_rate)
		# encoder.set_channels(2)
		encoder.set_in_sample_rate(ogg_info.sample_rate)
		encoder.set_channels(ogg_info.nchannels)
		encoder.set_quality(2)  # 2-highest, 7-fastest
		mp3_data = encoder.encode(pcm_data)
		mp3_data += encoder.flush()  # Flush when finished encoding the entire stream

		tags = ID3()
		tags.add(TLEN(encoding=0, data=length * 1000))
		data = tags._prepare_data(BytesIO(mp3_data), 0, 0, 4, '/', None)

		mp3_filename.write_bytes(data + mp3_data)

	# else:
	# 	print("Skip ogg; too short or too long")


_T = TypeVar("_T")


class InfiniteList(Generic[_T]):
	"""
	List-like object that refills with a random order once empty.
	"""

	_items: list[_T]
	_recent: Deque[_T]
	_working_items: list[_T]

	def __init__(self, items: list[_T]) -> None:
		self._items = items[:]
		if items:
			# self._recent = deque(maxlen=min(len(items) - 1, 5))
			self._recent = deque(maxlen=min(len(items) - 1, 5))
		else:
			self._recent = deque()

		self.repopulate()

	def repopulate(self) -> None:
		"""
		Repopulate the list with a new random order, avoiding recent items occuring soon.
		"""

		# print("Starting repopulate")
		self._working_items = []
		remaining_items = self._items[:]
		while remaining_items:
			# item = random.choice(remaining_items)
			# if len(self._working_items) < self._recent.maxlen:
			# 	if item in self._recent:
			# 		continue
			choices = []
			for item in remaining_items:
				assert self._recent.maxlen is not None
				if len(self._working_items) < self._recent.maxlen:
					if item in self._recent:
						continue
				choices.append(item)
			if not choices:
				choices = remaining_items
			item = random.choice(choices)
			self._working_items.append(item)
			remaining_items.remove(item)

		self._working_items.reverse()

	def pop(self) -> _T:
		"""
		Get the next item from the back of the list.
		"""

		if not self._working_items:
			self.repopulate()

		item = self._working_items.pop()
		self._recent.append(item)

		return item


_case_boundary_re = re.compile("(\\p{Ll})(\\p{Lu})")
_single_letters_re = re.compile("(\\p{Lu}|\\p{N})(\\p{Lu})(\\p{Ll})")


def to_snake_case(value: str) -> str:
	"""
	Convert the given string into ``snake_case``.

	:param value:
	"""

	# Matches VSCode behaviour
	case_boundary = _case_boundary_re.findall(value)
	single_letters = _single_letters_re.findall(value)
	if not case_boundary and not single_letters:
		return value.lower()
	value = _case_boundary_re.sub(r"\1_\2", value)
	value = _case_boundary_re.sub(r"\1_\2\3", value)
	return value.lower()


class StringReader(BytesIO):
	"""
	Reader for REDengine sized strings.
	"""

	vlq_value_mask = 0b01111111
	vlq_continuation = 0b10000000

	def parse_string_and_size(self) -> tuple[int, str]:
		"""
		Parse a length-prefixed string (as bytes) to a Python string.

		:param value: The string with a VLQ i32 length prefix.

		:returns: Tuple of length prefix and the string.
		"""

		size_prefix = self.read_vlq_int32()

		# The string length is the absolute value of the size prefix
		string_length = abs(size_prefix)

		if not string_length:
			return size_prefix, ''

		# Sign bit indicates whether UTF-16 (0) or UTF-8 (1)
		if size_prefix > 0:
			encoding = "UTF-16"
		else:
			encoding = "UTF-8"

		return size_prefix, self.read(string_length).decode(encoding)

	def parse_string(self) -> str:
		"""
		Parse a length-prefixed string (as bytes) to a Python string.

		:param value: The string with a VLQ i32 length prefix.
		"""

		return self.parse_string_and_size()[1]

	def read_vlq_int32(self) -> int:
		"""
		Parse modified 32 bit VLQ to int.

		The first bit is the sign bit, the 2nd bit tells whether there are more octets to read,
		and the next 6 bytes are the least significant bits of the number data.
		Remaining octets are 1+7 continuation and data.
		"""

		b = self.read(1)[0]
		is_negative = bool(b & 0b10000000)

		# Take the initial value from the lower 6 bits
		value = b & 0b00111111

		# Is the value larger than 6 bits?
		if (b & 0b01000000):  # The first octet stores the continuation flag in the 6th bit
			b = self.read(1)[0]
			# Mask and add the next 7 bits
			value |= (b & self.vlq_value_mask) << 6

			# Is the value larger than 13 bits?
			if (b & self.vlq_continuation):
				b = self.read(1)[0]
				value |= (b & self.vlq_value_mask) << 13

				# Is the value larger than 20 bits?
				if (b & self.vlq_continuation):
					b = self.read(1)[0]
					value |= (b & self.vlq_value_mask) << 20

					# Is the value larger than 27 bits?
					if (b & self.vlq_continuation):
						b = self.read(1)[0]
						value |= (b & self.vlq_value_mask) << 27

						# Is the value larger than 34 bits? That seems bad
						if (b & self.vlq_continuation):
							raise ValueError("Continuation bit set on 5th byte")

		if is_negative:
			return -value
		else:
			return value
