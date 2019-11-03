from models import Pack, FaunaDBLoader
from pathlib import Path

EXCLUDED_FILENAMES = {'.DS_Store'}
packs_path = Path('packs/')

with open('songinfo.json', 'w') as fp:
	for pack_path in filter(lambda x: x.name not in EXCLUDED_FILENAMES, packs_path.iterdir()):
		pack = Pack.from_path(pack_path)
		for song in pack.songs:
			fp.write(song.to_json())
			fp.write('\n')

"""
loader = FaunaDBLoader()
# Ultimately this will load these songs into FaunaDB
loader.load(dimo.songs)

for song in dimo.songs:
	print(song.to_json())
"""