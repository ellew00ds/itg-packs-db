"""
parser.py - This parses .scc and .sm files to extract metadata

TODO: add .sm parsing functionality
"""
import os
from pprint import pprint

# TODO: document what these do
EXCLUDED_KEYS = (
    'bpms',
    'steps',
    'stops',
    'radarvalues',
    'notes',
    'notedata',
    'chartname',
    )
REPEATED_KEYS = (
    'stepstype',
    'description',
    'chartstyle',
    'difficulty',
    'meter',
    'credit',
    'displaybpm',
    )

"""
This function grabs the simfile from a directory. May or may not currently work
"""
def grab_simfiles(rootdir, path_array=[], simfile_array=[]):
    for subdir, dirs, files in os.walk(rootdir):
        path = subdir.split('/')
        print("\n****** - Next Song Dir -", '*' * 50)
        if len(path) > 2:
            path_array.append(path)
            for path in path_array:
                #print(f"pack_name: {path[1]} -- song_name: {path[2]}")
                pass

        for file in files:
            #print("os.path.join(subdir, file):", os.path.join(subdir, file))
            if file.lower().endswith(('.ssc', '.sm')):
                print(f"KICKASS BRO: '{file}' is a simfile")
                simfile_array.append(os.path.join(subdir, file))
                #print("simfile_array:", simfile_array)
            else:
                print(f"IGNORED: '{file}' is not a simfile")
        print('*' * 75, '\n')
    print("simfile_array at end of grab_simfiles():", simfile_array)
    return simfile_array

"""
This function parses a .ssc file, given a filename
TODO: document how this parser actually works
"""
def parse_ssc_file(filename=None):
    with open(filename, "r") as fp:
        raw = fp.read()
    parsed = {}
    repeated = {}
    """
    Each "key" in the .ssc file is separated by a semicolon.
    We use semicolons to delimit
    """
    for value in raw.split(';'):
        value = value.strip('\r\n')
        if not value:
            continue
        """
        Check if there are instances of values without keys, i.e. there are 2 colons in a row
        if len(value.split(":")) > 2:
            # print("Too many values to unpack in:", value)
            # honestly not sure if this return should be in here, but keeping here for now for debugging
            return
        
        else:
        """
        k, v = value.split(':')
        if not v:
            continue
        

        k = k.strip('#').lower()
        # print("k:", k)
        # print("value:", value)
        if k in EXCLUDED_KEYS:
            continue
        if k in REPEATED_KEYS:
            if k not in repeated.keys():
                repeated[k] = [v]
            else:
                repeated[k].append(v)
        else:
            parsed[k] = v

    repeated_parsed = [None for _ in list(repeated.values())[0]]
    
    for k, v in repeated.items():
        for pos, val in enumerate(v):
            item = repeated_parsed[pos] or {}
            item[k] = val
            repeated_parsed[pos] = item

    repeated_parsed = list(
        filter(
            lambda x: all(
                [key in x for key in repeated.keys()]
            ), repeated_parsed)
        )
    parsed['sequences'] = repeated_parsed
       
    """
    final_data is JSON/dictionary that will be loaded 
    into MongoDB
    """
    final_data = {
        "song_name": None,
        "song_artist": None,
        "bpm": None,
        # read_meta.py will be updated and eventually fill this in at the db_insert level
        "pack_name": None,
        "pack_link": None,
        "difficulty": {
            "Challenge": None,
            "Hard": None,
            "Medium": None,
            "Easy": None,
            "Beginner": None,
            "Edit": None
        }
    }

    """
    Expected structure:
    {
        "song_name": "Dream a Dream",
        "song_artist": "Captain Jack",
        "bpm": "120",
        "pack_name": "DDR MAX 2",
        "pack_link": "drive.google.com/onemoretimeimbackwithanewrhyme",
        "difficulty": {
            "light": "3",
            "standard": "5",
            "heavy": "7"
        }
    }
    """

    final_data["song_name"] = parsed["title"]
    final_data["song_artist"] = parsed["artist"]
    # Cast BPM to int and round
    final_data["bpm"] = int(float(repeated["displaybpm"][0]))

    """
    ### TODO: ensure BPM is correctly represented
    bpm = repeated["displaybpm"][0]
    for i in repeated["displaybpm"]:
        if repeated["displaybpm"][i] != bpm:
            final_data["bpm"] = 'various'
    """

    """
    # NOTE: there could be duplicated difficulties. 
    This code assumes that there are not.
    """
    num_diffs = len(repeated["difficulty"])
    i = 0
    while i < num_diffs:
        # Find the current difficulty in the array
        current_diff = repeated["difficulty"][i]
        # Assign the respective meter value to that difficulty, in our final_data dictionary
        final_data["difficulty"][current_diff]=repeated["meter"][i]
        i+=1

    return final_data


# Run the parser
parsed_ssc = parse_ssc_file('night.ssc')

# Test: print object to terminal
pprint("parsed object:")
pprint(parsed_ssc)

"""
# Test: see if parser automatically works for .sm files
parsed_sm = parse_ssc_file('30MinutesHarder.sm')
pprint("parsed_sm below:")
pprint(parsed_sm)
"""