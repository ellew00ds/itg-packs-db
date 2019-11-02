from models import Pack
ddr = Pack.from_path("/Users/lewis/workspace/itg-packs-db/packs/Dance Dance Revolution 3rd Mix/")
print(ddr.songs)
print(ddr.name)
print(ddr.path)
print(ddr.songfiles)