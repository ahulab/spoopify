# spoopify

Get creds and put them here
```
# config/creds.json
{
    "client_id": "foo",
    "client_secret": "bar"
}

```

Then run the stuff, I'm using python 3.8

```
touch db/db.sqlite
python3 -m venv ./env
source ./env/bin/activate
pip install -r requirements.txt
cd src
python3 main.py
```

--

- doesn't handle rate limits
- doesn't reauthenticate if the token expires
- for some reason the api returns a 404 as soon as you try to paginate past the 2000th page
with an offset of 50. So idk if they just don't make it possible to search all 1million + artists, 
or if I'm overlooking something
