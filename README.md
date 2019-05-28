# In The Groove Packs Database
Source code for In The Groove packs database, containing song information by pack

This is currently a non-working project. [This can be used](https://search.stepmaniaonline.net/) as inspiration.

### Prerequesites
TBD

### Steps to completion

* Manually download all packs in [spreadsheet](www.secretsryboutit.com) to an AWS S3 bucket
	* These are a mix of GDrive, Dropbox, etc. links

* Unzip packs

* Determine where and how metadata is stored for artist name, step difficulties, etc.

* Create a Postgres database in AWS

* Each song will be a row in a single database

* Database columns will be:
	* song_name
	* song_artist
	* song_link
	* pack_name
	* difficulty/num_feet (for now, a JSON blob)


## Built With

* Python 3
* Flask

## Contributors

* **Lewis King** - [Github](https://github.com/lewisisgood)
* **Chandler Wyatt** - [Github](https://github.com/chandlerwyatt)
