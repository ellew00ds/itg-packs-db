from pathlib import Path
from typing import List, Union

from multidict import MultiDict

FILE_SUFFIXES = ('.ssc', '.sm', '.dwi')


# priority list: higher = higher priority
PRIORITIES = {
    '.ssc': 100,
    '.sm': 50,
    '.dwi': 1,
}


class Song:
    def __init__(self, name, artist, bpm, pack_name, pack_link, difficulty):
        self.name = name
        self.artist = artist
        self.bpm = bpm
        self.pack_name = pack_name
        self.pack_link = pack_link
        self.difficulty = difficulty

    def to_dict(self):
        return {
            'song_name': self.name,
            'song_artist': self.artist,
            'bpm': self.bpm,
            'pack_name': self.pack_name,
            'pack_link': self.pack_link,
            'difficulty': self.difficulty,
        }

    def to_json(self):
        from json import dumps
        return dumps(self.to_dict())

class ParsedMultiDict(MultiDict):
    @classmethod
    def load(cls, filename):
        with open(filename, "r") as fp:
            raw = fp.read()
        parsed = cls()
        """
        Each "key" in the file is separated by a semicolon.
        We use semicolons to delimit
        """
        for value in raw.split(';'):
            value = value.strip('\n')
            if not value:
                continue
            """
            Takes only the first k/v pair in a given semicolon grouping
            In case there are instances of values without keys, i.e. there are 2 colons in a row
            """
            k, v = value.split(":", 1)
            if not v:
                continue

            k = k.strip('#').lower()
            parsed.add(k, v)
        return parsed


class Parser(object):
    def get_song_name(self, multidict):
        return multidict.getone('title')

    def get_song_artist(self, multidict):
        return multidict.getone('artist')

    def get_bpm(self, multidict):
        ''' special handling for bpm here'''
        return multidict.getone('bpm', None)

    def get_difficulty(self, multidict):
        raise NotImplementedError

    def parse(self, filename, pack_name, pack_link):
        loaded_multidict = ParsedMultiDict.load(filename)

        return Song(
            name=self.get_song_name(loaded_multidict),
            artist=self.get_song_artist(loaded_multidict),
            bpm=self.get_bpm(loaded_multidict),
            pack_name=pack_name,
            pack_link=pack_link,
            difficulty=self.get_difficulty(loaded_multidict)
        )


class SSCParser(Parser):
    def get_difficulty(self, multidict):
        difficulties = list(map(lambda x: x.lower(), multidict.getall('difficulty')))
        meters = multidict.getall('meter')

        if len(difficulties) != len(meters):
            raise Exception("Length mismatch in difficulties")

        return dict(zip(difficulties, meters))


class DWIParser(Parser):
    def get_difficulty(self, multidict):
        single_difficulties = multidict.getall('single')
        parsed_difficulties = {}

        for item in single_difficulties:
            difficulty, level, _ = item.split(':')
            parsed_difficulties[difficulty.lower()] = int(level)

        return parsed_difficulties


class SMParser(Parser):
    def get_difficulty(self, multidict):
        print("I haven't been configured yet!")
        print("my name: {}".format(self.get_song_name(multidict)))

        return {}


EXTENSIONS_TO_PARSER_MAP = {
    '.ssc': SSCParser,
    '.sm': SMParser,
    '.dwi': DWIParser,
}


def get_priority_for_filename(filename):
    for extension, priority in PRIORITIES.items():
        if filename.suffix == extension:
            return priority
    else:
        raise ValueError('Improper filename {}. should be one of: {}'.format(filename, set(PRIORITIES.keys())))

# given foo.ssc, bar.sm, fizz.dwi, will return foo.ssc
# given fizz.dwi, bar.sm, will return bar.sm
# given fizz.dwi, buzz.dwi, will return an arbitary one
def get_highest_priority_filename(filenames):
    return sorted(filenames, key=get_priority_for_filename, reverse=True)[0]


class SongFiles:
    def __init__(self, name, path, simfiles):
        self.name = name
        self.path = path
        self.simfiles = simfiles

    def __str__(self):
        return '<SongFiles {}: ({} @ {})>'.format(self.name, self.path, hex(id(self)))

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_path(cls, path):
        if isinstance(path, str):
            path = Path(path)

        path = path.resolve()

        if not path.is_dir():
            raise ValueError('Must be passed a directory of a pack rather than a file')

        simfiles = list(filter(lambda x: x.is_file() and x.suffix.endswith(FILE_SUFFIXES),
                        path.rglob('*.*')))

        name = path.name.lower()

        return cls(name, path, simfiles)

    def get_highest_priority_simfile(self):
        return get_highest_priority_filename(self.simfiles)


class Pack:
    def __init__(self, name: str, path: Path, songfiles: List[Path]):
        self.name = name
        self.path = path
        self.songfiles = songfiles
        self.songs = [self.build_song(s) for s in self.songfiles]

    def __str__(self):
        return '<Pack {}: ({} @ {})>'.format(self.name, self.path, hex(id(self)))

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_path(cls, path: Union[str, Path]):
        if isinstance(path, str):
            path = Path(path)

        path = path.resolve()

        if not path.is_dir():
            raise ValueError('Must be passed a directory of a pack rather than a file')

        songfiles = [SongFiles.from_path(p) for p in path.iterdir() if p.is_dir()]

        name = path.name

        return cls(name, path, songfiles)

    def build_song(self, songfile):
        highest_priority = songfile.get_highest_priority_simfile()
        parser = EXTENSIONS_TO_PARSER_MAP[highest_priority.suffix]()
        return parser.parse(
            filename=highest_priority,
            pack_name=self.name,
            pack_link=None)
