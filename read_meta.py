import os
from mongo import make_mongo_client
from pymongo.errors import DuplicateKeyError
import re

title_tag = "#TITLE:"
artist_tag = "#ARTIST:"
pack_root = "packs"
diff_re = r"^#NOTES:\s*(.+):\s+(.*):\s+(.+):\s+(\d+):$"

client = make_mongo_client()
db = client.itg
coll = db["meta"]

for root, dirs, files in os.walk(pack_root):
    for file in files:
        if file.endswith(".sm"):
            meta_lines = {}
            smf = os.path.join(root, file)
            pack_name = smf.split("/", 2)[1]
            with open(smf, "rt") as sm_file:
                sm_raw = sm_file.read()
                for line in sm_file:
                    meta_lines["pack_name"] = pack_name
                    if line.startswith(title_tag):
                        new_line = line[len(title_tag):]
                        meta_lines["song_name"] = new_line.rstrip(";\n")
                    if line.startswith(artist_tag):
                        new_line = line[len(artist_tag):]
                        meta_lines["song_artist"] = new_line.rstrip(";\n")

            print(meta_lines)
            print("Do a db insert here")
            try:
                coll.insert_one(meta_lines)
            except DuplicateKeyError:
                print(f"Skipping document {meta_lines} because of DuplicateKeyError")
