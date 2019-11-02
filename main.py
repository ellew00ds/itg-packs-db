from models import Pack, FaunaDBLoader
ddr = Pack.from_path("/Users/lewis/workspace/itg-packs-db/packs/Dance Dance Revolution 3rd Mix/")
loader = FaunaDBLoader()
# Ultimately this will load these songs into FaunaDB
loader.load(ddr.songs)

for song in ddr.songs:
	print(song.to_json())