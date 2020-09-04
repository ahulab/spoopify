import os
import json
from utils import Logger
from base import SpoopyClient, SpoopyManager
from db_utils import SqliteBoss

logger = Logger(caller_filepath=__file__)

def load_config():
    global API_CLIENT_ID
    global API_SECRET

    with open('../config/creds.json') as json_file:
        creds_json = json.load(json_file)

    API_CLIENT_ID = creds_json['client_id']
    API_SECRET = creds_json['client_secret']

def main():
    load_config()
    spoopy_client = SpoopyClient(API_CLIENT_ID, API_SECRET)
    sqlite_boss = SqliteBoss()

    spoopy_manager = SpoopyManager(spoopy_client, sqlite_boss)
    spoopy_manager.sync_artists_metadata()

if __name__ == '__main__':
    logger.log("Starting")
    main()