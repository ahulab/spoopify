# spoopify

## Desc

I found that spotify was doing a bad job of showing me actually random music.
Often, it'd just show me music that is similar but different than the music
I already listen to. I wrote this to make it easier to find music in spotify 
that is truly unlike anything I already listen to.

The project will crawl around the spotify api and persists artist 
metadata into a sqlite database. I used this database to find weird genres 
that I'd never heard of before.

## Configuration

Get creds and put them here
```
# config/creds.json
{
    "client_id": "foo",
    "client_secret": "bar"
}

```

Then run it, it was developed with python 3.8

```
touch db/db.sqlite
python3 -m venv ./env
source ./env/bin/activate
pip install -r requirements.txt
cd src
python3 main.py
```

--

### Some Caveats
- doesn't handle rate limits
- doesn't reauthenticate if the token expires
- for some reason the api returns a 404 as soon as you try to paginate past the 2000th page
with an offset of 50. So idk if they just don't make it possible to search all 1million + artists, 
or if I'm overlooking something
