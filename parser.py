"""
parser.py - This shit parses .scc and .sm files to extract metadata
"""
from pprint import pprint

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


def parse_ssc_file(filename=None):
    with open(filename, "r") as fp:
        raw = fp.read()
    parsed = {}
    repeated = {}
    for value in raw.split(';'):
        value = value.strip('\r\n')
        if not value:
            continue
        k, v = value.split(':')
        if not v:
            continue

        k = k.strip('#').lower()
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
    print("repeated_parsed:", repeated_parsed)
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
    #print(repeated)
    #return parsed
    #final_data contains the JSON/dictionary that will be put into MongoDB
    final_data = {
        "song_name": None,
        "song_artist": None,
        "bpm": None,
        "pack_name": None,   # read_meta.py will be updated and eventually fill this in at the db_insert level
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
    #cast to int and round
    final_data["bpm"] = repeated["displaybpm"][0]
    """
    ### ensuring BPM is correctly represented
    bpm = repeated["displaybpm"][0]
    for i in repeated["displaybpm"]:
        if repeated["displaybpm"][i] != bpm:
            final_data["bpm"] = 'various'
    """
    #there could be dupe difficulties. this assumes there are not.
    num_diffs = len(repeated["difficulty"])
    i = 0
    while i < num_diffs:
        # Find the current difficulty in the array
        current_diff = repeated["difficulty"][i]
        #Assign the respective meter value to that difficulty, in our final_data dictionary
        final_data["difficulty"][current_diff]=repeated["meter"][i]
        i+=1

    return final_data


parsed_ssc = parse_ssc_file('night.ssc')
pprint("parsed_ssc below:")
pprint(parsed_ssc)
