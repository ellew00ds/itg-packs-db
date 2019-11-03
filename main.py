from models import Pack, FaunaDBLoader
# ddr = Pack.from_path("/Users/lewis/workspace/itg-packs-db/packs/Dance Dance Revolution 3rd Mix/")
dimo = Pack.from_path("/Users/lewis/workspace/itg-packs-db/packs/dimo/")
loader = FaunaDBLoader()
# Ultimately this will load these songs into FaunaDB
loader.load(dimo.songs)

for song in dimo.songs:
	print(song.to_json())