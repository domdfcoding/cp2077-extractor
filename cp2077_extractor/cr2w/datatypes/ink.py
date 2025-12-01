#!/usr/bin/env python3
#
#  ink.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``ink``).
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
from dataclasses import dataclass

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.datatypes.base import Chunk

__all__ = ["inkCreditsResource", "inkCreditsSectionEntry"]


@dataclass
class inkCreditsSectionEntry(Chunk):
	"""
	A section in the game credits.
	"""

	#: The names to credit.
	names: list[bytes]

	display_mode: enums.inkDisplayMode

	#: A heading (e.g. "Programming") or a role title (e.g. "Senior Programmer")
	section_title: str = ''


@dataclass
class inkCreditsResource(Chunk):
	"""
	Data for the game's credits.
	"""

	cooking_platform: enums.ECookingPlatform
	sections: list[inkCreditsSectionEntry]
