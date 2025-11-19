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
import networkx  # type: ignore[import]
from networkx import Graph, all_simple_paths

if TYPE_CHECKING:
	# 3rd party
	from matplotlib.figure import Figure  # type: ignore[import]  # nodep

__all__ = [
		"EventData",
		"load_events_dict",
		"find_graph_entry_points",
		"get_link_paths",
		"parse_radio_scene_graph",
		"parse_subtitles",
		"plot_graph",
		"remove_intermediate_nodes"
		]


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
	from matplotlib import pyplot as plt  # type: ignore[import]  # nodep
	from networkx.drawing.nx_agraph import graphviz_layout  # type: ignore[import]

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


def parse_subtitles(scene_json: dict[str, Any]) -> dict[str, str]:
	"""
	Parse subtitle data.

	:param scene_json: JSON representation of a REDengine ``.scene`` file (as parsed by Wolvenkit).
	"""

	# TODO: handle non-localised scene files with separate subtitles file.

	vp_entries = {}
	subtitles = {}
	for entry in scene_json["Data"]["RootChunk"]["locStore"]["vpEntries"]:
		vp_entries[entry["variantId"]["ruid"]] = entry["content"]
	for entry in scene_json["Data"]["RootChunk"]["locStore"]["vdEntries"]:
		subtitles[entry["locstringId"]["ruid"]] = vp_entries[entry["variantId"]["ruid"]]

	return subtitles


def parse_radio_scene_graph(scene_json: dict[str, Any]) -> tuple[Graph, dict[int, list[EventData]]]:
	"""
	Partial parsing of scene graph.

	Only finds dialogue events and the paths between them; no conditional logic.

	:param scene_json: JSON representation of a REDengine ``.scene`` file (as parsed by Wolvenkit).
	"""

	root_chunk = scene_json["Data"]["RootChunk"]

	screenplay_store_lines = root_chunk["screenplayStore"]["lines"]
	screenplay_store_dict = {}

	for line in screenplay_store_lines:
		screenplay_store_dict[line["itemId"]["id"]
								] = (line["femaleLipsyncAnimationName"]["$value"], line["locstringId"]["ruid"])

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
