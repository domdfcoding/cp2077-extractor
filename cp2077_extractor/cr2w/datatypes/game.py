#!/usr/bin/env python3
#
#  game.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``game``).
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
from dataclasses import dataclass, field

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.datatypes.base import Chunk

__all__ = ["gameEntityReference"]


@dataclass
class gameEntityReference(Chunk):
	type: enums.gameEntityReferenceType = enums.gameEntityReferenceType.EntityRef
	reference: str = ''
	names: list[str] = field(default_factory=list)
	slot_name: str = ''
	scene_actor_context_name: str = ''
	dynamic_entity_unique_name: str = ''
