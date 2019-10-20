# In The Groove Packs Database
Source code for In The Groove packs database, containing song information by pack. [This site can be used](https://search.stepmaniaonline.net/) as inspiration.

## Installing
From the Terminal, clone this repo onto your computer with:

```
git clone https://github.com/lewisisgood/itg-packs-db
```

Move into the new directory:

```
cd itg-packs-db/
```

Run the parser on a `packs` directory:
```
python3 parser.py
```

## Steps to project completion

* Manually download all packs in `spreadsheet` to one of the hard drives on `the server`
	* These are a mix of GDrive, Dropbox, etc. links

* Unzip packs

* Run parser on all packs

* Load each song as a single record in one cloud database

* Create front-end for database using React

Document structure:
```json
{
    "song_name": "Dream a Dream",
    "song_artist": "Captain Jack",
    "bpm": "120",
    "pack_name": "DDR MAX 2",
    "pack_link": "drive.google.com/heyohcaptainjack",
    "difficulty": {
        "light": "3",
        "standard": "5",
        "heavy": "7"
    }
}
```

## Built With

* Python 3
* [FaunaDB](https://fauna.com/)

## Contributors

* **Lewis King** - [Github](https://github.com/lewisisgood)
* **Chandler Wyatt** - [Github](https://github.com/chandlerwyatt)
* **Gene Peters** - [Github](https://github.com/gene-telligent)
