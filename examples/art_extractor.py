# stdlib
from io import BytesIO
from pathlib import PureWindowsPath

# 3rd party
from domdf_python_tools.paths import PathPlus

# this package
from cp2077_extractor.cr2w.io import parse_cr2w_buffer
from cp2077_extractor.cr2w.textures import texture_to_image
from cp2077_extractor.redarchive_reader import REDArchive

archive = "basegame_4_gamedata"

archive_file = PathPlus("/path/to/cyberpunk/install/Cyberpunk 2077/archive/pc/content/") / f"{archive}.archive"
assert archive_file.is_file()

output_dir = PathPlus("artwork")
output_dir.maybe_make()

archive = REDArchive.load_archive(archive_file)

target_files = [
		"base/gameplay/gui/world/internet/templates/growl_fm/growl_fm.xbm",
		]

with archive_file.open("rb") as fp:
	for filename in target_files:
		file = archive.file_list.find_filename(filename)
		segments = archive.file_list.get_segments(file)
		cr2w_file = parse_cr2w_buffer(BytesIO(archive.extract_file(fp, file)))
		img = texture_to_image(cr2w_file.root_chunk)

		output_filename = output_dir / PureWindowsPath(filename).with_suffix(".png").name
		img.save(output_filename)
		print(f"{archive_file.name}:{filename} -> {output_filename}")
