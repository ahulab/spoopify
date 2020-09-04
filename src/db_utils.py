import sqlite3
import datetime
from utils import Logger

class ArtistDao:
    TABLE_NAME = "artists"
    ARTIST_TO_GENRE_TABLE = "artist_to_genre"
    GENRE_TABLE = "genres"

    def __init__(self, id, name, popularity, follower_count, genres):
        self.id = id
        self.name = name
        self.popularity = popularity
        self.follower_count = follower_count
        if not isinstance(genres, list):
            ValueError(f'var "genres" must be a list, got {genres}')
        else:
            self.genres = genres
        self.logger = Logger(caller_filepath=__file__, clazz=self.__class__)
        
    def _insert_genres(self):
        conn = SqliteBoss.get_conn()
        c = conn.cursor()

        genre_ids = []
        self.logger.debug(f"Inserting genres: {self.genres}")
        for i in self.genres:
            self.logger.debug(f"Inserting genre: {i}")
            c.execute('INSERT OR IGNORE INTO genres VALUES (?)', (i,))

        conn.commit()
        conn.close()
       
    def _insert_genre_mappings(self):
        conn = SqliteBoss.get_conn()
        c = conn.cursor()

        for i in self.genres:
            c.execute('INSERT OR REPLACE INTO artist_to_genre VALUES (?,?)', (self.id, i,))

        conn.commit()
        conn.close()

    def insert(self):
        conn = SqliteBoss.get_conn()
        c = conn.cursor()

        self._insert_genres()
        self._insert_genre_mappings()
        happened_at = datetime.datetime.now()
        c.execute(
            'INSERT OR IGNORE INTO artists VALUES (?,?,?,?,?,?)', 
            (self.id, self.name, self.popularity, self.follower_count, happened_at, happened_at,)
        )

        conn.commit()
        conn.close()

class SqliteBoss:
    logger = Logger(caller_filepath=__file__)

    @classmethod
    def get_conn(self):
        return sqlite3.connect('../db/db.sqlite')

    def create_db(self):
        conn = SqliteBoss.get_conn()
        c = conn.cursor()

        self.logger.log('Creating db...')

        c.executescript('''
        CREATE TABLE IF NOT EXISTS artists
            (
                id VARCHAR NOT NULL constraint primary_key PRIMARY KEY, 
                name VARCHAR NOT NULL, 
                popularity INTEGER NOT NULL, 
                follower_count INTEGER NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP NOT NULL
            );

        CREATE TABLE IF NOT EXISTS artist_to_genre
            (
                artist_id VARCHAR NOT NULL,
                genre_id VARCHAR NOT NULL,
                FOREIGN KEY(artist_id) REFERENCES artists(id),
                FOREIGN KEY(genre_id) REFERENCES genres(name),
                UNIQUE(artist_id, genre_id)
            
            );

        CREATE TABLE IF NOT EXISTS genres 
            (
                name VARCHAR NOT NULL constraint primary_key PRIMARY KEY
            );
        ''')

        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()
        self.logger.log('DB created')
