from models.user import User
from classes.user_repository.repository import UserRepository
from models.list_entry import ListEntry


class UserPreferenceMutations(UserRepository):
    @staticmethod
    def _upsert_keyword_in_list(keyword: str, list_id: str):
        """
        General method to upsert (update or insert if not existent) a keyword in the lists document
        """
        user_list = UserPreferenceMutations.user_specific_preference_list()
        to_update = next(
            (entry for entry in user_list[list_id] if entry["keyword"] == keyword), None
        )  # filter for correct keyword

        if not to_update:
            update = ListEntry(keyword, 1)
            user_list[list_id].append(update.__dict__)
        else:
            update = ListEntry.from_json(to_update)
            update.occurence += 1

            for indx, list_entry in enumerate(user_list[list_id]):
                if list_entry["keyword"] == update.keyword:
                    user_list[list_id][indx] = update.__dict__

        return UserRepository.list_collection.update_one(
            {"username": UserRepository.username}, {"$set": user_list}, upsert=True
        )

    @staticmethod
    def user_specific_preference_list():
        return UserRepository.list_collection.find_one(
            {"username": UserRepository.username}
        )

    @staticmethod
    def upsert_keyword_in_blacklist(keyword: str):
        """
        Method to upsert keyword in blacklist of user; uses _upsert_keyword_in_list
        """
        return UserPreferenceMutations._upsert_keyword_in_list(keyword, "black")

    @staticmethod
    def upsert_keyword_in_whitelist(keyword: str):
        """
        Method to upsert keyword in whitelist of user; uses _upsert_keyword_in_list
        """
        return UserPreferenceMutations._upsert_keyword_in_list(keyword, "white")

    @staticmethod
    def get_blacklisted():
        """
        Returns all keywords in the blacklist of current user
        """
        return UserPreferenceMutations.user_specific_preference_list()["black"]

    @staticmethod
    def _drop_blacklist():
        """
        Only use this method in a developer environment AND WHEN YOU'RE COMPLETELY SURE WHAT YOU ARE DOING!
        """
        UserRepository.list_collection.update_one({"username": UserRepository.username}, { "$set" : { "black": [] }})

    @staticmethod
    def get_whitelisted():
        """
        Returns all keywords in the whitelist of current user
        """
        return UserPreferenceMutations.user_specific_preference_list()["white"]

    @staticmethod
    def _drop_whitelist():
        """
        Only use this method in a developer environment AND WHEN YOU'RE COMPLETELY SURE WHAT YOU ARE DOING!
        """
        UserRepository.list_collection.update_one({"username": UserRepository.username}, { "$set" : { "white": [] }})

    @staticmethod
    def get_shortlisted():
        """
        Returns all keywords in the shortlist of current user
        """
        return UserPreferenceMutations.user_specific_preference_list()["short"]
