from models.list_entry import ListEntry
from models.user import User
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from urllib.parse import quote_plus
from typing import Union
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

    # collections
    keyword_collection = user_cache_db.get_collection("keywords")
    sentence_collection = user_cache_db.get_collection("sentences")
    list_collection = user_cache_db.get_collection("lists")
    profile_collection = user_cache_db.get_collection("profiles")
    pricing_collection = user_cache_db.get_collection("pricing")

    # collection shortcuts for user
    @staticmethod
    def get_keyword_prefrence_list():
        return UserRepository.list_collection.find_one(
            {"username": UserRepository.username}
        )

    # mutations
    ## general
    @staticmethod
    def create_user(username: str, pw: str):
        return UserRepository.user_cache_db.command("createUser", username, pwd=pw, roles=["defaultUser"])

    @staticmethod
    def change_user_pw(pw: str):
        return UserRepository.user_cache_db.command("updateUser", UserRepository.username, pwd=pw)

    @staticmethod
    def init_user():
        if not UserRepository.get_keyword_prefrence_list():
            UserRepository.list_collection.update_one(
                {"username": UserRepository.username},
                {
                    "$set": {
                        "username": UserRepository.username,
                        "black": [],
                        "white": [],
                    }
                },
                upsert=True,
            )

    @staticmethod
    def get_user_by_name(username: str) -> Union[User, None]:
        user_dump = UserRepository.user_cache_db.command("usersInfo")
        users = list(
            map(lambda user: User(user["user"], user["userId"]), user_dump["users"])
        )
        return next((user for user in users if user.name == username), None)

    ## keyword preferences
    @staticmethod
    def _upsert_keyword_in_list(keyword: str, list: str):
        """
        General method to upsert (update or insert if not existent) a keyword in the lists document
        """
        user_list = UserRepository.get_keyword_prefrence_list()
        to_update = next((keyword for keyword in user_list[list]), None)

        if not to_update:
            update = ListEntry(keyword, 1)

            user_list[list].append(update.__dict__)
        else:
            update = ListEntry.from_json(to_update)
            update.occurence += 1

            for indx, list_entry in enumerate(user_list[list]):
                if list_entry["keyword"] == update.keyword:
                    user_list[list][indx] = update.__dict__

        return UserRepository.list_collection.update_one(
            {"username": UserRepository.username}, {"$set": user_list}
        )

    @staticmethod
    def upsert_keyword_in_blacklist(keyword: str):
        """
        Method to upsert keyword in blacklist of user; uses _upsert_keyword_in_list
        """
        return UserRepository._upsert_keyword_in_list(keyword, "black")

    @staticmethod
    def upsert_keyword_in_whitelist(keyword: str):
        """
        Method to upsert keyword in whitelist of user; uses _upsert_keyword_in_list
        """
        return UserRepository._upsert_keyword_in_list(keyword, "white")

    ## keyword cache
    @staticmethod
    def add_keyword_to_cache(keyword: str):
        return UserRepository.keyword_collection.update_one(
            {"username": UserRepository.username},
            {
                "$push": {
                    "cache": keyword
                }
            },
            upsert=True
        )

    ## sentence cache
    @staticmethod
    def add_sentence_to_cache(keyword: str):
        return UserRepository.sentence_collection.update_one(
            {"username": UserRepository.username},
            {
                "$push": {
                    "cache": keyword
                }
            },
            upsert=True
        )
