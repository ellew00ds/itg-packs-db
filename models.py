from pathlib import Path
from typing import List, Union
from mongo import make_mongo_client
import re
import logging
import json

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

    def __str__(self):
        # This formats a string for displaying song; {} is a wildcard
        return '<Song {} - {}: ({} @ {})>'.format(self.artist, self.name, self.pack_name, hex(id(self)))

    def __repr__(self):
        # This formats the interal 'representation' for displaying song; {} is a wildcard
        # For in the REPL, as opposed to calling print or str on something
        return self.__str__()

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
        """Loads k/v pair formatted file into a multidict.

        @classmethod uses a passed class, in this case returns a configured instance
        TODO: learn how this works
        """
        with open(filename, "r") as fp:
            raw = fp.read()

        raw = re.sub(r'\/\/.*$', '', raw, flags=re.MULTILINE)

        # if a BOM is present, ignore it
        if raw.startswith('\ufeff'):
            raw = raw[1:]

        parsed = cls()
        """
        Each "key" in the file is separated by a semicolon.
        We use semicolons to delimit
        """
        for value in raw.split(';'):
            value = value.strip('\n').strip()
            if not value:
                continue
            """
            Takes only the first k/v pair in a given semicolon grouping
            In case there are instances of values without keys, i.e. there are 2 colons in a row
            """
            try:
                k, v = value.split(":", 1)
            except ValueError:
                from pdb import set_trace
                set_trace()
            if not v:
                continue

            k = k.strip().strip('\n').strip('#').lower()
            parsed.add(k, v)
        return parsed


class Parser(object):
    def get_song_name(self, multidict):
        return multidict.getone('title')

    def get_song_artist(self, multidict):
        return multidict.getone('artist')

    def get_bpm(self, multidict):
        ''' special handling for bpm here'''
        if multidict.get('bpm'):
            return multidict.get('bpm')
        elif multidict.get('bpms'):
            return int(float(re.sub(r'^0.0*=', '', multidict.get('bpms').split(',')[0])))
        else:
            print("get_bpm couldn't find no bpms muchacho")
            print(multidict.get('title'))
            return None

    def get_difficulty(self, multidict):
        raise NotImplementedError

    def parse(self, filename, pack_name, pack_link):
        loaded_multidict = ParsedMultiDict.load(filename)

        parsed_song = Song(
            name=self.get_song_name(loaded_multidict),
            artist=self.get_song_artist(loaded_multidict),
            bpm=self.get_bpm(loaded_multidict),
            pack_name=pack_name,
            pack_link=pack_link,
            difficulty=self.get_difficulty(loaded_multidict)
        )

        # We're putting cleanup logic here. Maybe belongs in another place.
        if parsed_song.bpm:
            # from pdb import set_trace
            # set_trace()
            parsed_song.bpm = int(float(parsed_song.bpm))

        song_name = parsed_song.name
        if song_name.startswith("["):
            parsed_song.difficulty["Challenge"] = song_name.split('] ')[0][1:]
            if song_name.split('] ')[1].startswith("["):
                parsed_song.bpm = song_name.split('] ')[1][1:]
            parsed_song.name = song_name.split('] ')[2]

        return parsed_song


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
            difficulty, meter, _ = item.split(':')
            parsed_difficulties[difficulty.lower()] = int(meter)

        return parsed_difficulties


class SMParser(Parser):
    def get_difficulty(self, multidict):
        difficulties = {}
        notes_all = multidict.getall('notes')
        for note_blob in notes_all:
            notes = ''.join([n for n in note_blob if n != '\n' and n != ' '])
            notes_type, _, difficulty, meter, _ = notes.split(':', 4)
            if notes_type == 'dance-single':
                difficulties[difficulty.lower()] = int(meter)

        return difficulties


EXTENSIONS_TO_PARSER_MAP = {
    '.ssc': SSCParser(),
    '.sm': SMParser(),
    '.dwi': DWIParser(),
}


def get_priority_for_filename(filename):
    for extension, priority in PRIORITIES.items():
        if filename.suffix.lower() == extension:
            return priority
    else:
        raise ValueError('Improper filename {}. should be one of: {}'.format(filename, set(PRIORITIES.keys())))

# given foo.ssc, bar.sm, fizz.dwi, will return foo.ssc
# given fizz.dwi, bar.sm, will return bar.sm
# given fizz.dwi, buzz.dwi, will return an arbitary one
def get_highest_priority_filename(filenames):
    if len(filenames) == 0:
        return None
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
            raise ValueError('Must be passed a directory of a song rather than a file: {}'.format(path))

        simfiles = list(filter(lambda x: x.is_file() and x.suffix.lower().endswith(FILE_SUFFIXES),
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
        self.songs = list(filter(None, [self.build_song(s) for s in self.songfiles]))

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
            raise ValueError('Must be passed a directory of a pack rather than a file: {}'.format(path))

        # iterdir returns a list of all subfiles in a particular directory, in one level
        # list of the name ...
        songfiles = [SongFiles.from_path(p) for p in path.iterdir() if p.is_dir()]

        name = path.name

        return cls(name, path, songfiles)

    def build_song(self, songfile):
        highest_priority = songfile.get_highest_priority_simfile()
        if not highest_priority:
            logging.warning("Could not find any valid simfiles in directory: %s", songfile.path)
            return None
        parser = EXTENSIONS_TO_PARSER_MAP[highest_priority.suffix.lower()]
        try:
            return parser.parse(
                filename=highest_priority,
                pack_name=self.name,
                pack_link=None)
        except UnicodeDecodeError:
            logging.error("Could not determine encoding / bad byte in file: %s", highest_priority)
            return None


class Loader(object):
    """docstring for Loader"""
    def load(self, songs):
        pass


class MongoLoader(Loader):
    """docstring for MongoLoader"""
    def __init__(self):
        self.client = make_mongo_client()
        self.db = self.client['itg']
        self.coll = self.db['simfiles']
    #from pdb import set_trace
    #set_trace()

    def drop(self):
        from pdb import set_trace
        #set_trace()
        #self.coll.drop()

    def load(self, simfile_json='songinfo.json'):
        with open(simfile_json, 'r') as fp:
            for line in fp:
                json_doc = json.loads(line)
                self.coll.insert_one(json_doc)


class FaunaDBLoader(Loader):
    """docstring for FaunaDBLoader"""
    def load(self, songs):
        pass
