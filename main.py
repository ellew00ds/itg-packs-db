import argparse
from models import Pack, FaunaDBLoader, MongoLoader
from pathlib import Path
import logging


logging.basicConfig()

EXCLUDED_FILENAMES = {'.DS_Store'}

parser = argparse.ArgumentParser(description='Simfile Parser')
group = parser.add_mutually_exclusive_group()
group.add_argument('--packs_path',
                   help="Specify path to packs parent dir, if not './packs'",
                   default='packs/')
group.add_argument('--pack',
                   help="Specify path to individual pack - typically for testing purposes")
parser.add_argument('--load',
                    help="Specifies which database to populate. Possible arguments:\nmongo\nfauna")
parser.add_argument('--drop',
                    help="If specified with --load, will drop\
                    the relevant mongo or fauna collection before loading again. \
                    You must specify whether you want to drop the fauna or mongo collection")
args = parser.parse_args()
#from pdb import set_trace
#set_trace()

if args.drop and not args.load:
    if args.drop == 'mongo':
        loader = MongoLoader()
        loader.drop()
        print(f"Dropped {loader.coll.full_name} collection from MongoDB")
    elif args.drop == 'fauna':
        print("--drop fauna: not yet implemented")
    else:
        print("When --drop is used, you must specify 'mongo' or 'fauna'")
elif args.pack:
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

if args.load == 'mongo' and not args.drop:
    loader = MongoLoader()
    loader.load()
    print("Loaded MongoDB")
elif args.load == 'mongo' and args.drop:
    loader = MongoLoader()
    loader.drop()
    print("Dropped simfiles coll from MongoDB")
    loader.load()
    print("Loaded MongoDB")
elif args.load == 'fauna' and not args.drop:
    print("--load fauna: not implemented yet")
elif args.load == 'fauna' and args.drop:
    print("--load fauna: not implemented yet")
    print("--drop fauna: not implemented yet")
elif not args.load and not args.drop:
    print("No database drops or loads were performed.")


"""
loader = FaunaDBLoader()
# Ultimately this will load these songs into FaunaDB
loader.load(dimo.songs)

for song in dimo.songs:
    print(song.to_json())
"""