from pymongo import MongoClient
from pymongo.errors import OperationFailure
from urllib.parse import quote_plus
import os


class UserRepository:

    client: MongoClient = MongoClient(
        f"mongodb://{quote_plus(os.environ['DB_USER'])}:{quote_plus(os.environ['DB_PASSWD'])}@199.231.189.38:27017/user_cache"
    )
    user_cache_db = client["user_cache"]
    try:
        username = user_cache_db.command("connectionStatus")["authInfo"][
            "authenticatedUsers"
        ][0]["user"]
    except OperationFailure:
        print("Error: tried to call user repository without init_user call!")
        exit()

    # collections
    keyword_collection = user_cache_db.get_collection("keywords")
    sentence_collection = user_cache_db.get_collection("sentences")
    list_collection = user_cache_db.get_collection("lists")
    profile_collection = user_cache_db.get_collection("profiles")
    pricing_collection = user_cache_db.get_collection("pricing")

    # collection getters
    @staticmethod
    def init_user():
        if not UserRepository.list_collection.find_one(
            {"username": UserRepository.username}
        ):
            UserRepository.list_collection.update_one(
                {"username": UserRepository.username},
                {
                    "$set": {
                        "username": UserRepository.username,
                        "black": [],
                        "grey": [],
                        "white": [],
                        "short": [],
                    }
                },
                upsert=True,
            )
