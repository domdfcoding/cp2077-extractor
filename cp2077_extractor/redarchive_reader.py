#!/usr/bin/env python3
#
#  redarchive_reader.py
"""
Partial parser for REDEngine ``.archive`` files.
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
import hashlib
import struct
from dataclasses import dataclass
from pathlib import PureWindowsPath
from typing import IO

# 3rd party
from domdf_python_tools.typing import PathLike
from fnvhash import fnv1a_64  # type: ignore[import-untyped]

# this package
from cp2077_extractor.utils import decompress

__all__ = ["FileList", "FileRecord", "FileSegment", "REDArchive"]


@dataclass
class FileRecord:
	"""
	Represents a FileRecord in a ``.archive`` file.
	"""

	#: FNV1A64 hash of the filename
	name_hash: int

	#: Windows filetime of file creation
	timestamp: int

	#: Number of inline buffers
	num_inline_buffer_segs: int

	#: Index of the first file segment
	segs_start: int

	#: Index of the last file segment
	segs_end: int

	#: Index of the first resource dependency
	res_deps_start: int

	#: Index of the last resource dependency
	res_deps_end: int

	#: SHA1 hash of the file  # TODO: compressed files?
	sha1_hash: bytes


@dataclass
class FileSegment:
	"""
	Represents a FileSegment in a ``.archive`` file.
	"""

	#: Offset of the data
	offset: int

	#: Size of compressed data
	zsize: int

	#: Size of uncompressed data
	size: int


@dataclass
class FileList:
	"""
	Represents a FileList in a ``.archive`` file.
	"""

	#: Always 8
	file_table_offset: int

	file_table_size: int

	#: Checksum of ???
	crc: int

	#: Number of files
	file_entry_count: int

	#: Number of file segments
	file_segment_count: int

	#: Number of resource dependencies
	resource_dep_count: int

	file_records: list[FileRecord]
	file_segments: list[FileSegment]
	resource_dependencies: list[int]

	def find_filename(self, filename: str) -> FileRecord:
		"""
		Find the record for the given filename, relative to the root of the archive (usually starting ``base``).

		:param filename:
		"""

		# TODO: cache hashes and mapping of hash to records for speed
		name_hash = fnv1a_64(bytes(PureWindowsPath(filename)))
		for record in self.file_records:
			if record.name_hash == name_hash:
				return record

		raise FileNotFoundError(filename)

	def get_segments(self, file: FileRecord) -> list[FileSegment]:
		"""
		Returns the segments for the given file.

		:param file:
		"""

		return self.file_segments[file.segs_start:file.segs_end]


@dataclass
class REDArchive:
	"""
	Represents a REDEngine ``.archive`` file.
	"""

	#: Constant: "RDAR"
	magic: str

	#: Currently 12
	version: int

	#: Offset of beginning of file list
	index_pos: int

	#: Size of file list
	index_size: int

	#: Always 0
	debug_pos: int

	#: Always 0
	debug_size: int

	#: Size of file (excluding Filesize)
	filesize: int

	#: Files created with WolvenKit only
	custom_data_length: int

	file_list: FileList

	@classmethod
	def load_archive(cls, archive_file: PathLike) -> "REDArchive":
		"""
		Load metadata for an ``.archive`` file.

		:param archive_file:
		"""

		with open(archive_file, "rb") as fp:
			magic: bytes
			magic, version, index_pos, index_size, debug_pos, debug_size, filesize, custom_data_length = struct.unpack("<4sIQIQIQI", fp.read(44))

			fp.seek(index_pos)

			file_table_offset, file_table_size, crc, file_entry_count, file_segment_count, resource_dep_count = struct.unpack("<IIQIII", fp.read(28))

			# f.read(file_table_offset)
			file_records = []
			file_segments = []

			for _ in range(file_entry_count):

				name_hash, timestamp, num_inline_buffer_segs, segs_start, segs_end, res_deps_start, res_deps_end = struct.unpack("<QqIIIII", fp.read(36))
				sha1_hash = fp.read(20)

				file_records.append(
						FileRecord(
								name_hash=name_hash,
								timestamp=timestamp,
								num_inline_buffer_segs=num_inline_buffer_segs,
								segs_start=segs_start,
								segs_end=segs_end,
								res_deps_start=res_deps_start,
								res_deps_end=res_deps_end,
								sha1_hash=sha1_hash,
								)
						)

			for _ in range(file_segment_count):
				offset, zsize, size = struct.unpack("<QII", fp.read(16))
				file_segments.append(FileSegment(offset=offset, zsize=zsize, size=size))

			resource_dependencies = list(struct.unpack(f"<{resource_dep_count}Q", fp.read(8 * resource_dep_count)))

			# remainder = fp.read(9999)
			# print(len(remainder))

			file_list = FileList(
					file_table_offset=file_table_offset,
					file_table_size=file_table_size,
					crc=crc,
					file_entry_count=file_entry_count,
					file_segment_count=file_segment_count,
					resource_dep_count=resource_dep_count,
					file_records=file_records,
					file_segments=file_segments,
					resource_dependencies=resource_dependencies,
					)

			return cls(
					magic=magic.decode("UTF-8"),
					version=version,
					index_pos=index_pos,
					index_size=index_size,
					debug_pos=debug_pos,
					debug_size=debug_size,
					filesize=filesize,
					custom_data_length=custom_data_length,
					file_list=file_list,
					)

	def extract_file(self, fp: IO, file: FileRecord) -> bytes:
		"""
		Extract a file from the archive.

		:param fp: File handle for the opened archive.
		:param file: The file to extract.
		"""

		segments = self.file_list.get_segments(file)
		compressed = False

		file_content = b''
		for segment in segments:
			fp.seek(segment.offset, 0)
			signature = fp.read(4)
			if signature == b"KARK":
				compressed = True
				# Compressed with kraken
				size = struct.unpack("<i", fp.read(4))[0]
				assert segment.size == size

				file_content += decompress(fp.read(segment.zsize - 8), size)

			else:
				file_content += signature
				assert segment.size == segment.zsize
				file_content += fp.read(segment.zsize - 4)

		if not compressed:
			# TODO: is it the sha1 of the compressed data?
			sha1_hash = hashlib.sha1(file_content).digest()
			assert sha1_hash == file.sha1_hash, (sha1_hash, file.sha1_hash)

		return file_content
