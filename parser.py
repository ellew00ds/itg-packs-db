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

    print(repeated)

    return parsed


parsed_ssc = parse_ssc_file('night.ssc')
pprint(parsed_ssc)
