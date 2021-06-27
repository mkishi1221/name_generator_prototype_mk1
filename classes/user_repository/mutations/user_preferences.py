from classes.name import Name
from typing import List, Union
from models.user import User
from classes.user_repository.repository import UserRepository
from models.bwl_entry import BlackWhiteListEntry


class UserPreferenceMutations(UserRepository):
    @staticmethod
    def user_specific_preference_list():
        return UserRepository.list_collection.find_one(
            {"username": UserRepository.username}
        )

    # region upserts
    @staticmethod
    def _upsert_keyword_in_list(list_entry: Union[BlackWhiteListEntry, Name], list_id: str):
        """
        General method to upsert (update or insert if not existent) a keyword in the lists document
        """
        user_list = UserPreferenceMutations.user_specific_preference_list()
        if isinstance(list_entry, BlackWhiteListEntry):
            to_update = next(
                (
                    entry
                    for entry in user_list[list_id]
                    if BlackWhiteListEntry.from_dict(entry) == list_entry
                ),
                None,
            )  # filter for correct keyword
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
            setattr(list_entry, "occurence", 1)
            user_list[list_id].append(list_entry.__dict__)
        else:

            def update_list(identifier):
                to_update["occurence"] += 1

                for indx, list_entry in enumerate(user_list[list_id]):
                    if list_entry[identifier] == to_update[identifier]:
                        user_list[list_id][indx] = to_update

            if isinstance(list_entry, BlackWhiteListEntry):
                update_list("keyword")
            else:
                update_list("name")

        return UserRepository.list_collection.update_one(
            {"username": UserRepository.username}, {"$set": user_list}, upsert=True
        )

    ## blacklist
    @staticmethod
    def upsert_keyword_in_blacklist(keyword: BlackWhiteListEntry):
        """
        Method to upsert keyword in blacklist of user; uses _upsert_keyword_in_list
        """
        return UserPreferenceMutations._upsert_keyword_in_list(keyword, "black")

    @staticmethod
    def upsert_multiple_keywords_in_blacklist(keywords: List[BlackWhiteListEntry]):
        """
        Method to upsert multiple keywords in blacklist of user; uses _upsert_keyword_in_list
        """
        for keyword in keywords:
            UserPreferenceMutations._upsert_keyword_in_list(keyword, "black")

    ## whitelist
    @staticmethod
    def upsert_keyword_in_whitelist(keyword: BlackWhiteListEntry):
        """
        Method to upsert keyword in whitelist of user; uses _upsert_keyword_in_list
        """
        return UserPreferenceMutations._upsert_keyword_in_list(keyword, "white")

    @staticmethod
    def upsert_multiple_keywords_in_whitelist(keywords: List[BlackWhiteListEntry]):
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
    def get_blacklisted():
        """
        Returns all keywords in the blacklist of current user
        """
        return UserPreferenceMutations.user_specific_preference_list()["black"]

    ## whitelist
    @staticmethod
    def get_whitelisted():
        """
        Returns all keywords in the whitelist of current user
        """
        return UserPreferenceMutations.user_specific_preference_list()["white"]

    ## shortlist
    @staticmethod
    def get_shortlisted():
        """
        Returns all keywords in the shortlist of current user
        """
        return UserPreferenceMutations.user_specific_preference_list()["short"]

    # endregion

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
