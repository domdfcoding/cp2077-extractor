#!/usr/bin/env python3
#
#  radio_dj.py
"""
Helpers for handling radio DJ logic and audio files.
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
from collections.abc import Collection, Iterator
from typing import TYPE_CHECKING, Any, NamedTuple

# 3rd party
import networkx  # type: ignore[import-untyped]
from networkx import Graph, all_simple_paths

# this package
from cp2077_extractor.cr2w.datatypes.base import HandleData
from cp2077_extractor.cr2w.datatypes.scn import (
		scnDialogLineEvent,
		scnRewindableSectionNode,
		scnSceneGraph,
		scnSceneResource,
		scnscreenplayDialogLine,
		scnSectionNode
		)
from cp2077_extractor.cr2w.header_structs import CR2WFile

if TYPE_CHECKING:
	# 3rd party
	from matplotlib.figure import Figure  # nodep

__all__ = [
		"DJData",
		"EventData",
		"find_graph_entry_points",
		"get_link_paths",
		"load_events_dict",
		"parse_radio_scene_graph",
		"parse_subtitles",
		"plot_graph",
		"remove_intermediate_nodes",
		]


class DJData(NamedTuple):
	"""
	Data for a radio DJ's sound files.
	"""

	#: The filenames in the game files (in ``base/localization/en-us/vo`` or ``base\localization\common\vo``) for this advert all start with this string.
	audio_filename_prefix: str

	#: The name of the scene file in ``base/media/animated_billboards/scenes`` in the game files (with the suffix ``.scene``.)
	scene_file: str

	#: The name of the radio station etc.
	station_name: str

	general_audio: bool = False
	"""
	Whether the audio is common too all game languages.

	:py:obj:`False` for localised audio, :py:obj:`True` for files in ``audio_1_general.archive``.
	"""


class EventData(NamedTuple):
	"""
	Metadata for an event triggered by a node in a scene.
	"""

	event_id: str

	#: Identifier of the ``scnscreenplayDialogLine`` for this event (which indicates the file to play and the subtitle line).
	screenplay_line_id: int

	#: The suffix of the audio file, to give the file to play. e.g. `f_1BAAA2A79044D000`.
	audio_file_suffix: str

	#: Identifier of the subtitles for the event.
	subtitle_ruid: str


def load_events_dict(events_dict: dict[str, list[tuple[str, int, str, str]]]) -> dict[int, list[EventData]]:
	"""
	Load a JSON serialised mapping of node numbers to :class:`~.EventData`.

	Converts string keys back into integers and value tuples bacm into :class:`EventData`.

	:param events_dict:
	"""

	return {int(k): [EventData(*vv) for vv in v] for k, v in events_dict.items()}


def remove_intermediate_nodes(graph: Graph, audio_nodes: Collection[int]) -> None:
	"""
	Remove non-audio nodes from a networkx graph, and reconnect edges.

	:param graph:
	:param audio_nodes:
	"""

	audio_nodes_set = set(audio_nodes)
	intermediate_nodes = set(graph.nodes()) - audio_nodes_set

	for node in intermediate_nodes:

		for in_src, _ in graph.in_edges(node):
			for _, out_dst in graph.out_edges(node):
				graph.add_edge(in_src, out_dst)

		graph.remove_node(node)

	assert not set(graph.nodes()) - audio_nodes_set


def plot_graph(graph: Graph) -> "Figure":
	"""
	Plot the graph, in a hierarchy from start nodes down to finish nodes.

	Requires ``matplotlib`` and ``pygraphviz``.

	:param graph:
	"""

	# 3rd party
	from matplotlib import pyplot as plt  # nodep
	from networkx.drawing.nx_agraph import graphviz_layout  # type: ignore[import-untyped]

	pos = graphviz_layout(graph, "dot")
	fig, ax1 = plt.subplots()
	networkx.draw(graph, ax=ax1, with_labels=True, font_weight="bold", pos=pos)
	return fig


def find_graph_entry_points(graph: Graph) -> tuple[list[int], list[int], list[int]]:
	"""
	Find entry points into the radio logic graph.

	That is, any lone nodes, any start nodes, and any end nodes (skipping chatter).

	:param graph:
	"""

	lone_nodes = []
	start_nodes = []
	end_nodes = []
	for node in graph.nodes():
		if graph.in_degree(node) == 0:
			if graph.out_degree(node) == 0:
				lone_nodes.append(node)
			else:
				start_nodes.append(node)
		elif graph.out_degree(node) == 0:
			end_nodes.append(node)
		# else:
		# 	raise ValueError(node, "Intermediate node")

	return lone_nodes, start_nodes, end_nodes


def parse_subtitles(data: dict[str, Any] | CR2WFile) -> dict[str, str]:
	"""
	Parse subtitle data.

	:param data: A REDengine ``.scene`` file, either as a JSON representation as parsed by Wolvenkit, or as a :class:`~.CR2WFile` instance.
	"""

	# TODO: handle non-localised scene files with separate subtitles file.

	if isinstance(data, CR2WFile):
		return _parse_subtitles_cr2wfile(data)
	else:
		return _parse_subtitles_json(data)


def _parse_subtitles_json(scene_json: dict[str, Any]) -> dict[str, str]:
	"""
	Parse subtitle data.

	:param scene_json: JSON representation of a REDengine ``.scene`` file (as parsed by Wolvenkit).
	"""

	vp_entries = {}
	subtitles = {}
	for entry in scene_json["Data"]["RootChunk"]["locStore"]["vpEntries"]:
		vp_entries[entry["variantId"]["ruid"]] = entry["content"]
	for entry in scene_json["Data"]["RootChunk"]["locStore"]["vdEntries"]:
		subtitles[entry["locstringId"]["ruid"]] = vp_entries[entry["variantId"]["ruid"]]

	return subtitles


def _parse_subtitles_cr2wfile(cr2w_file: CR2WFile) -> dict[str, str]:
	"""
	Parse subtitle data.

	:param cr2w_file: Parsed REDengine ``.scene`` file.
	"""

	assert isinstance(cr2w_file.root_chunk, scnSceneResource)
	root_chunk: scnSceneResource = cr2w_file.root_chunk

	vp_entries = {}
	subtitles = {}
	for vp_entry in root_chunk.loc_store.vp_entries:
		vp_entries[str(vp_entry.variant_id.ruid)] = vp_entry.content
	for vd_entry in root_chunk.loc_store.vd_entries:
		subtitles[str(vd_entry.locstring_id.ruid)] = vp_entries[str(vd_entry.variant_id.ruid)]

	return subtitles


def parse_radio_scene_graph(data: dict[str, Any] | CR2WFile) -> tuple[Graph, dict[int, list[EventData]]]:
	"""
	Partial parsing of scene graph.

	Only finds dialogue events and the paths between them; no conditional logic.

	:param data: A REDengine ``.scene`` file, either as a JSON representation as parsed by Wolvenkit, or as a :class:`~.CR2WFile` instance.
	"""

	if isinstance(data, CR2WFile):
		return _parse_radio_scene_graph_cr2wfile(data)
	else:
		return _parse_radio_scene_graph_json(data)


def _parse_radio_scene_graph_json(scene_json: dict[str, Any]) -> tuple[Graph, dict[int, list[EventData]]]:
	"""
	Partial parsing of scene graph.

	Only finds dialogue events and the paths between them; no conditional logic.

	:param scene_json: JSON representation of a REDengine ``.scene`` file (as parsed by Wolvenkit).
	"""

	root_chunk = scene_json["Data"]["RootChunk"]

	screenplay_store_dict: dict[int, tuple[str, str]] = {}

	for line in root_chunk["screenplayStore"]["lines"]:
		line_data = (line["femaleLipsyncAnimationName"]["$value"], line["locstringId"]["ruid"])
		screenplay_store_dict[line["itemId"]["id"]] = line_data

	scene_graph_json = root_chunk["sceneGraph"]
	graph = networkx.DiGraph()
	audio_nodes: set[int] = set()
	audio_events: dict[int, list[EventData]] = {}

	for node in scene_graph_json["Data"]["graph"]:
		# pprint.pprint(node)
		# node_type = node["Data"]["$type"]
		# if node_type != "scnSectionNode":
		# 	print(node["Data"]["$type"])
		destinations = []
		for socket in node["Data"]["outputSockets"]:
			for destination in socket["destinations"]:
				destinations.append(destination["nodeId"]["id"])
				graph.add_edge(node["Data"]["nodeId"]["id"], destination["nodeId"]["id"])

		events = []
		for event in node["Data"].get("events", ()):
			if event["Data"]["$type"] == "scnDialogLineEvent":
				# events.append(event)
				events.append(
						EventData(
								event["Data"]["id"]["id"],
								event["Data"]["screenplayLineId"]["id"],
								*screenplay_store_dict[event["Data"]["screenplayLineId"]["id"]]
								)
						)
			# else:
			# 	print(event)
		if events:
			# print(">>>", node["Data"]["nodeId"]["id"], pprint.pformat(events ))
			node_id = node["Data"]["nodeId"]["id"]
			audio_nodes.add(node_id)
			audio_events[node_id] = events
		# else:
		# 	print(node)

	remove_intermediate_nodes(graph, audio_nodes)

	return graph, audio_events


def _parse_radio_scene_graph_cr2wfile(cr2w_file: CR2WFile) -> tuple[Graph, dict[int, list[EventData]]]:
	"""
	Partial parsing of scene graph.

	Only finds dialogue events and the paths between them; no conditional logic.

	:param cr2w_file: Parsed REDengine ``.scene`` file.
	"""

	assert isinstance(cr2w_file.root_chunk, scnSceneResource)
	root_chunk: scnSceneResource = cr2w_file.root_chunk

	screenplay_store_dict: dict[int, tuple[str, str]] = {}

	line: scnscreenplayDialogLine
	for line in root_chunk.screenplay_store.lines:
		line_data = (line.female_lipsync_animation_name.decode("UTF-8"), str(line.locstring_id.ruid))
		screenplay_store_dict[line.item_id.id] = line_data

	scene_graph: HandleData[scnSceneGraph] = root_chunk.scene_graph
	graph = networkx.DiGraph()
	audio_nodes: set[int] = set()
	audio_events: dict[int, list[EventData]] = {}

	for node in scene_graph["data"].graph:
		# pprint.pprint(node)
		destinations = []
		for socket in node["data"].output_sockets:
			for destination in socket.destinations:
				destinations.append(destination.node_id.id)
				graph.add_edge(node["data"].node_id.id, destination.node_id.id)

		if not isinstance(node["data"], (scnSectionNode, scnRewindableSectionNode)):  # TODO: other valid types
			continue

		events = []
		for event in node["data"].events:
			if isinstance(event["data"], scnDialogLineEvent):
				# events.append(event)
				events.append(
						EventData(
								str(event["data"].id.id),
								event["data"].screenplay_line_id.id,
								*screenplay_store_dict[event["data"].screenplay_line_id.id],
								)
						)
			# else:
			# 	print(event)
		if events:
			node_id = node["data"].node_id.id
			audio_nodes.add(node_id)
			audio_events[node_id] = events
		# else:
		# 	print(node)

	remove_intermediate_nodes(graph, audio_nodes)

	return graph, audio_events


def get_link_paths(graph: Graph) -> Iterator[list[int]]:
	"""
	Returns an iterator over possible paths through the various link segments.
	"""

	lone_nodes, start_nodes, end_nodes = find_graph_entry_points(graph)

	for node in lone_nodes:
		yield [node]
		# print(">>>", [node])

	for start, end in itertools.product(start_nodes, end_nodes):
		yield from all_simple_paths(graph, start, end)
