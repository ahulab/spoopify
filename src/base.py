import requests
import datetime
import inspect
import time
from utils import Logger
from db_utils import ArtistDao
from requests.auth import HTTPBasicAuth

from base64 import b64encode
class SpoopyClient:

    auth_base_url = "https://accounts.spotify.com"
    TOKEN_ENDPOINT = "/api/token"

    API_BASE_URL = "https://api.spotify.com"
    ARTISTS_ENDPOINT = "/v1/artists"
    SEARCH_ENDPOINT = "/v1/search"

    def __init__(self, client_id, client_secret):
        self.logger = Logger(caller_filepath=__file__, clazz=self.__class__)
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = {}
        self.get_auth_token()

    def get_auth_token(self):
        get_token_endpoint = "{}{}".format(self.auth_base_url, self.TOKEN_ENDPOINT)
        self.logger.log('Fetching new token')
        r = requests.post(
            get_token_endpoint, 
            auth = HTTPBasicAuth(self.client_id, self.client_secret),
            data = {
                'grant_type': 'client_credentials'
            },
        )

        r.raise_for_status()
        self.logger.log(r.json())
        self.token = r.json()
    
    def get_artist(self):
        get_artists_endpoint = "{}{}".format(self.API_BASE_URL, self.ARTISTS_ENDPOINT)
        self.logger.log("Fetching artist details from {}".format(get_artists_endpint))
        r = requests.get(
            get_artists_endpoint, 
            headers={
                "Authorization": f"Bearer {self.token['access_token']}"
            }
        )
        self.logger.log(r.json())
    
    def page_through_all_artist_results(self, query_val):
        get_search_endpoint = "{}{}".format(self.API_BASE_URL, self.SEARCH_ENDPOINT)
        more_pages = True
        while more_pages:
            r = requests.get(
                get_search_endpoint,
                headers={
                    "Authorization": f"Bearer {self.token['access_token']}"
                },
                params = {
                    "query": query_val,
                    "type": "artist",
                    "limit": 50
                }
            )
            if r.status_code == 404:
                return
            else:
                r.raise_for_status()

            more_pages = 'https://' in r.json()['artists']['next']
            get_search_endpoint = r.json()['artists']['next']

            if more_pages:
                self.logger.info(f"More pages available for query val '{query_val}', getting {get_search_endpoint} next")
            else:
                self.logger.info(f"No more pages available for query '{query_val}'")

            self.logger.info(f"Sleeping 1...")
            time.sleep(1)

            yield r

    def get_artists_by_search_terms(self, **kwargs):
        search_terms = kwargs.get('search_terms', ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'q', 'x', 'y', 'z', 
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])

        limit = kwargs.get('limit', 50)

        get_search_endpoint = "{}{}".format(self.API_BASE_URL, self.SEARCH_ENDPOINT)
        for i in search_terms:
            for j in self.page_through_all_artist_results(i):
                yield j.json()

    
class SpoopyManager:
    def __init__(self, spoopy_client, sqlite_boss):
        self.logger = Logger(caller_filepath=__file__, clazz=self.__class__)
        self.spoopy_client = spoopy_client
        self.sqlite_boss = sqlite_boss
        self.setup()

    def setup(self):
        self.sqlite_boss.create_db()
    
    def sync_artists_metadata(self):
        self.logger.log("Starting to sync artist metadata")
        for results in self.spoopy_client.get_artists_by_search_terms():
            for result in results['artists']['items']:
                artist = ArtistDao(
                    result['id'],
                    result['name'], 
                    result['popularity'],
                    result['followers']['total'], 
                    result['genres'], 
                )
                self.logger.debug(f"Inserting record for artist {result['name']}")
                artist.insert()

