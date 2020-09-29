# StepMania Packs Database
Source code for the song pack parser for a StepMania packs database called [Fit Up Your Style](https://fitupyourstyle.com/), containing song information by pack. [This site was used](https://search.stepmaniaonline.net/) as inspiration.

## Installing
From the Terminal, clone this repo onto your computer with:

```
git clone https://github.com/lewisisgood/itg-packs-db
```

Move into the new directory:

```
cd itg-packs-db/
```

Add your `t.py` credentials file to the top-level directory.

Run the parser on a `packs` directory to load data into MongoDB:
```
python3 main.py --load mongo
```

## Document Structure
```json
{
    "name": "Dream a Dream",
    "artist": "Captain Jack",
    "bpm": 120,
    "pack": {
        "name" : "DDR MAX 2",
        "link": "drive.google.com/heyohcaptainjack",
    },
    "difficultyMap": {
        "light": "3",
        "standard": "5",
        "heavy": "7"
    },
    "difficulties": [
        3, 7, 5
    ]
}

```

## Built With

* Python 3

## Contributors

* **Lewis King** - [Github](https://github.com/lewisisgood)
* **Chandler Wyatt** - [Github](https://github.com/chandlerwyatt)
* **Gene Peters** - [Github](https://github.com/gene-telligent)
* **Chandler Wyatt** - [Github](https://github.com/ryanxgraham)
