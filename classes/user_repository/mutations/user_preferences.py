from classes.keyword import Keyword
from classes.name import Name
from typing import List, Dict, Union
from models.user import User
from classes.user_repository.repository import UserRepository
from models.bgwl_entry import BlackGreyWhiteListEntry
import orjson as json


class UserPreferenceMutations(UserRepository):
    @staticmethod
    def user_specific_preference_list() -> Union[Dict, None]:
        return UserRepository.list_collection.find_one(
            {"username": UserRepository.username}
        )

    # region upserts
    @staticmethod
    def _upsert_keyword_in_list(
        list_entry: Union[BlackGreyWhiteListEntry, Name], list_id: str
    ):
        """
        General method to upsert (update or insert if not existent) a keyword in the lists document
        """
        user_list = UserPreferenceMutations.user_specific_preference_list()
        if isinstance(list_entry, BlackGreyWhiteListEntry):
            try:
                to_update = next(
                    (
                        entry
                        for entry in user_list[list_id]
                        if BlackGreyWhiteListEntry.from_dict(entry) == list_entry
                    ),
                    None,
                )  # filter for correct keyword
            except KeyError:
                to_update = None
        elif isinstance(list_entry, Name):
            to_update = next(
                (
                    entry
                    for entry in user_list[list_id]
                    if entry["name"] == list_entry.name
                ),
                None,
            )  # filter for correct keyword

        if not to_update:
            setattr(list_entry, "occurrence", 1)

            return UserRepository.list_collection.update_one(
                {"username": UserRepository.username}, {"$addToSet": {list_id: list_entry.__dict__}}
            )

        else:
            to_update["occurrence"] += 1

            return UserRepository.list_collection.update_one(
                {
                    "username": UserRepository.username,
                    f"{list_id}.{'keyword' if isinstance(list_entry, BlackGreyWhiteListEntry) else 'name'}": list_entry.keyword
                    if isinstance(list_entry, BlackGreyWhiteListEntry)
                    else list_entry.name,
                },
                {"$set": {f"{list_id}.$.occurrence": to_update["occurrence"]}},
            )

    ## blacklist
    @staticmethod
    def upsert_keyword_in_blacklist(keyword: BlackGreyWhiteListEntry):
        """
        Method to upsert keyword in blacklist of user; uses _upsert_keyword_in_list
        """
        return UserPreferenceMutations._upsert_keyword_in_list(keyword, "black")

    @staticmethod
    def upsert_multiple_keywords_in_blacklist(keywords: List[BlackGreyWhiteListEntry]):
        """
        Method to upsert multiple keywords in blacklist of user; uses _upsert_keyword_in_list
        """
        for keyword in keywords:
            UserPreferenceMutations._upsert_keyword_in_list(keyword, "black")

    ## greylist
    @staticmethod
    def upsert_keyword_in_greylist(keyword: BlackGreyWhiteListEntry):
        """
        Method to upsert keyword in greylist of user; uses _upsert_keyword_in_list
        """
        return UserPreferenceMutations._upsert_keyword_in_list(keyword, "grey")

    @staticmethod
    def upsert_multiple_keywords_in_greylist(keywords: List[BlackGreyWhiteListEntry]):
        """
        Method to upsert multiple keywords in greylist of user; uses _upsert_keyword_in_list
        """
        for keyword in keywords:
            UserPreferenceMutations._upsert_keyword_in_list(keyword, "grey")

    ## whitelist
    @staticmethod
    def upsert_keyword_in_whitelist(keyword: BlackGreyWhiteListEntry):
        """
        Method to upsert keyword in whitelist of user; uses _upsert_keyword_in_list
        """
        return UserPreferenceMutations._upsert_keyword_in_list(keyword, "white")

    @staticmethod
    def upsert_multiple_keywords_in_whitelist(keywords: List[BlackGreyWhiteListEntry]):
        """
        Method to upsert multiple keywords in whitelist of user; uses _upsert_keyword_in_list
        """
        for keyword in keywords:
            UserPreferenceMutations._upsert_keyword_in_list(keyword, "white")

    ## shortlist
    @staticmethod
    def upsert_keyword_in_shortlist(keyword: Name):
        """
        Method to upsert keyword in shortlist of user; uses _upsert_keyword_in_list
        """
        return UserPreferenceMutations._upsert_keyword_in_list(keyword, "short")

    @staticmethod
    def upsert_multiple_keywords_in_shortlist(keywords: List[Name]):
        """
        Method to upsert multiple keywords in shortlist of user; uses _upsert_keyword_in_list
        """
        for keyword in keywords:
            UserPreferenceMutations._upsert_keyword_in_list(keyword, "short")

    # endregion

    # region getters
    ## blacklist
    @staticmethod
    def get_blacklisted() -> List:
        """
        Returns all keywords in the blacklist of current user
        """
        return UserPreferenceMutations.user_specific_preference_list()["black"]

    ## greylist
    @staticmethod
    def get_greylisted() -> List:
        """
        Returns all keywords in the greylist of current user
        """
        return UserPreferenceMutations.user_specific_preference_list()["grey"]

    ## whitelist
    @staticmethod
    def get_whitelisted() -> List:
        """
        Returns all keywords in the whitelist of current user
        """
        return UserPreferenceMutations.user_specific_preference_list()["white"]

    ## shortlist
    @staticmethod
    def get_shortlisted() -> List:
        """
        Returns all keywords in the shortlist of current user
        """
        return UserPreferenceMutations.user_specific_preference_list()["short"]

    # endregion

    # region removers
    ## blacklist
    @staticmethod
    def remove_from_blacklist(keyword: str):
        UserRepository.list_collection.update_one(
            {"username": UserRepository.username},
            {"$pull": {"black": {"keyword": keyword}}},
        )

    ## greylist
    @staticmethod
    def remove_from_greylist(keyword: str):
        UserRepository.list_collection.update_one(
            {"username": UserRepository.username},
            {"$pull": {"grey": {"keyword": keyword}}},
        )

    ## whitelist
    @staticmethod
    def remove_from_whitelist(keyword: str):
        UserRepository.list_collection.update_one(
            {"username": UserRepository.username},
            {"$pull": {"white": {"keyword": keyword}}},
        )

    ## shortlist
    @staticmethod
    def remove_from_shortlist(keyword: str):
        UserRepository.list_collection.update_one(
            {"username": UserRepository.username},
            {"$pull": {"short": {"keyword": keyword}}},
        )

    # dev methods
    @staticmethod
    def _drop_blacklist():
        """
        Only use this method in a developer environment AND WHEN YOU'RE COMPLETELY SURE WHAT YOU ARE DOING!
        """
        UserRepository.list_collection.update_one(
            {"username": UserRepository.username}, {"$set": {"black": []}}
        )

    @staticmethod
    def _drop_greylist():
        """
        Only use this method in a developer environment AND WHEN YOU'RE COMPLETELY SURE WHAT YOU ARE DOING!
        """
        UserRepository.list_collection.update_one(
            {"username": UserRepository.username}, {"$set": {"grey": []}}
        )

    @staticmethod
    def _drop_whitelist():
        """
        Only use this method in a developer environment AND WHEN YOU'RE COMPLETELY SURE WHAT YOU ARE DOING!
        """
        UserRepository.list_collection.update_one(
            {"username": UserRepository.username}, {"$set": {"white": []}}
        )

    @staticmethod
    def _drop_shortlist():
        """
        Only use this method in a developer environment AND WHEN YOU'RE COMPLETELY SURE WHAT YOU ARE DOING!
        """
        UserRepository.list_collection.update_one(
            {"username": UserRepository.username}, {"$set": {"short": []}}
        )
