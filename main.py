import argparse
from models import Pack, FaunaDBLoader
from pathlib import Path
import logging


logging.basicConfig()

EXCLUDED_FILENAMES = {'.DS_Store'}

parser = argparse.ArgumentParser(description='Simfile Parser')
group = parser.add_mutually_exclusive_group()
group.add_argument('--packs_path', default='packs/')
group.add_argument('--pack')
args = parser.parse_args()
if args.pack:
    pack_dir = Pack.from_path(args.pack)
    with open('songinfo.json', 'w') as fp:
        for song in pack_dir.songs:
            fp.write(song.to_json())
            fp.write('\n')
    #from pdb import set_trace
    #set_trace()
elif args.packs_path:
    pack_dir = args.packs_path
    with open('songinfo.json', 'w') as fp:
        packs_path = Path(pack_dir)
        for pack_path in filter(lambda x: x.is_dir(), packs_path.iterdir()):
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