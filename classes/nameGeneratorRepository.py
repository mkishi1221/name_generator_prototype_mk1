from pymongo import MongoClient
from urllib.parse import quote_plus
import os


class NameGeneratorRepository:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NameGeneratorRepository, cls).__new__(
                cls, *args, **kwargs
            )
        return cls._instance

    def __init__(self):
        self.client = MongoClient(
            f"mongodb://{quote_plus('mainAdmin')}:{quote_plus(os.environ['DB_PASSWD'])}@199.231.189.38:27017/admin"
        )
        self.keywordsDB = self.client["keyword_cache"]

    def read_keywords(self):
        return self.keywordsDB.command("usersInfo")
