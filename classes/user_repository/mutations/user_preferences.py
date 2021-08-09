import asyncio
from classes.name import Name
from classes.keyword import Keyword
from typing import List, Dict, Union
from classes.user_repository.repository import UserRepository
from concurrent.futures import ProcessPoolExecutor
import multiprocessing


def add_keywords(words: List[Keyword], list_id: str):
    for keyword in words:
        UserPreferenceMutations._upsert_keyword_in_list(keyword, list_id)


class UserPreferenceMutations(UserRepository):
    @staticmethod
    def user_specific_preference_list() -> Union[Dict, None]:
        return UserRepository.list_collection.find_one(
            {"project_id": UserRepository.project_id}
        )

    # region upserts
    @staticmethod
    def _upsert_keyword_in_list(list_entry: Union[Keyword, Name], list_id: str):
        """
        General method to upsert (update or insert if not existent) a keyword in the lists document
        """
        user_list = UserPreferenceMutations.user_specific_preference_list()
        if isinstance(list_entry, Keyword):
            try:
                to_update = next(
                    (
                        entry
                        for entry in user_list[list_id]
                        if Keyword.from_dict(entry) == list_entry
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
                {"project_id": UserRepository.project_id},
                {"$addToSet": {list_id: list_entry.__dict__}},
            )

        else:
            to_update["occurrence"] += 1

            return UserRepository.list_collection.update_one(
                {
                    "project_id": UserRepository.project_id,
                    f"{list_id}.{'keyword' if isinstance(list_entry, Keyword) else 'name'}": list_entry.keyword
                    if isinstance(list_entry, Keyword)
                    else list_entry.name,
                },
                {"$set": {f"{list_id}.$.occurrence": to_update["occurrence"]}},
            )

    @staticmethod
    async def _upsert_multiple_keywords(keywords: List[Keyword], list_id: str):
        num_workers = multiprocessing.cpu_count()
        executor = ProcessPoolExecutor()

        if (num_batches := int(len(keywords) / num_workers)) == 0:
            num_batches = 1

        loop = asyncio.get_event_loop()

        await asyncio.wait(
            [
                loop.run_in_executor(
                    executor,
                    add_keywords,
                    keywords[batch * num_workers : (batch + 1) * num_workers],
                    list_id,
                )
                for batch in range(num_batches)
            ]
        )

    ## blacklist
    @staticmethod
    def upsert_keyword_in_blacklist(keyword: Keyword):
        """
        Method to upsert keyword in blacklist of user; uses _upsert_keyword_in_list
        """
        return UserPreferenceMutations._upsert_keyword_in_list(keyword, "black")

    @staticmethod
    async def upsert_multiple_keywords_in_blacklist(keywords: List[Keyword]):
        """
        Method to upsert multiple keywords in blacklist of user; uses _upsert_keyword_in_list
        """
        await UserPreferenceMutations._upsert_multiple_keywords(keywords, "black")

    ## greylist
    @staticmethod
    def upsert_keyword_in_greylist(keyword: Keyword):
        """
        Method to upsert keyword in greylist of user; uses _upsert_keyword_in_list
        """
        return UserPreferenceMutations._upsert_keyword_in_list(keyword, "grey")

    @staticmethod
    async def upsert_multiple_keywords_in_greylist(keywords: List[Keyword]):
        """
        Method to upsert multiple keywords in greylist of user; uses _upsert_keyword_in_list
        """
        await UserPreferenceMutations._upsert_multiple_keywords(keywords, "grey")

    ## whitelist
    @staticmethod
    def upsert_keyword_in_whitelist(keyword: Keyword):
        """
        Method to upsert keyword in whitelist of user; uses _upsert_keyword_in_list
        """
        return UserPreferenceMutations._upsert_keyword_in_list(keyword, "white")

    @staticmethod
    async def upsert_multiple_keywords_in_whitelist(keywords: List[Keyword]):
        """
        Method to upsert multiple keywords in whitelist of user; uses _upsert_keyword_in_list
        """
        await UserPreferenceMutations._upsert_multiple_keywords(keywords, "white")

    ## shortlist
    @staticmethod
    def upsert_keyword_in_shortlist(keyword: Name):
        """
        Method to upsert keyword in shortlist of user; uses _upsert_keyword_in_list
        """
        return UserPreferenceMutations._upsert_keyword_in_list(keyword, "short")

    @staticmethod
    async def upsert_multiple_keywords_in_shortlist(keywords: List[Name]):
        """
        Method to upsert multiple keywords in shortlist of user; uses _upsert_keyword_in_list
        """
        await UserPreferenceMutations._upsert_multiple_keywords(keywords, "short")

    # endregion

    # region getters
    ## blacklist
    @staticmethod
    def get_blacklisted() -> List[Keyword]:
        """
        Returns all keywords in the blacklist of current user
        """
        return [
            Keyword(**word)
            for word in UserPreferenceMutations.user_specific_preference_list()["black"]
        ]

    ## greylist
    @staticmethod
    def get_greylisted() -> List[Keyword]:
        """
        Returns all keywords in the greylist of current user
        """
        return [
            Keyword(**word)
            for word in UserPreferenceMutations.user_specific_preference_list()["grey"]
        ]

    ## whitelist
    @staticmethod
    def get_whitelisted() -> List[Keyword]:
        """
        Returns all keywords in the whitelist of current user
        """
        return [
            Keyword(**word)
            for word in UserPreferenceMutations.user_specific_preference_list()["white"]
        ]

    ## shortlist
    @staticmethod
    def get_shortlisted() -> List[Name]:
        """
        Returns all names in the shortlist of current user
        """

        def remove_occurence(word: Dict):
            del word["occurrence"]
            return Name(**word)

        return [
            remove_occurence(word)
            for word in UserPreferenceMutations.user_specific_preference_list()["short"]
        ]

    # endregion

    # region removers
    ## blacklist
    @staticmethod
    def remove_from_blacklist(keyword: str):
        UserRepository.list_collection.update_one(
            {"project_id": UserRepository.project_id},
            {"$pull": {"black": {"keyword": keyword}}},
        )

    ## greylist
    @staticmethod
    def remove_from_greylist(keyword: str):
        UserRepository.list_collection.update_one(
            {"project_id": UserRepository.project_id},
            {"$pull": {"grey": {"keyword": keyword}}},
        )

    ## whitelist
    @staticmethod
    def remove_from_whitelist(keyword: str):
        UserRepository.list_collection.update_one(
            {"project_id": UserRepository.project_id},
            {"$pull": {"white": {"keyword": keyword}}},
        )

    ## shortlist
    @staticmethod
    def remove_from_shortlist(keyword: str):
        UserRepository.list_collection.update_one(
            {"project_id": UserRepository.project_id},
            {"$pull": {"short": {"keyword": keyword}}},
        )

    # endregion

    # dev methods
    @staticmethod
    def _drop_blacklist():
        """
        Only use this method in a developer environment AND WHEN YOU'RE COMPLETELY SURE WHAT YOU ARE DOING!
        """
        UserRepository.list_collection.update_one(
            {"project_id": UserRepository.project_id}, {"$set": {"black": []}}
        )

    @staticmethod
    def _drop_greylist():
        """
        Only use this method in a developer environment AND WHEN YOU'RE COMPLETELY SURE WHAT YOU ARE DOING!
        """
        UserRepository.list_collection.update_one(
            {"project_id": UserRepository.project_id}, {"$set": {"grey": []}}
        )

    @staticmethod
    def _drop_whitelist():
        """
        Only use this method in a developer environment AND WHEN YOU'RE COMPLETELY SURE WHAT YOU ARE DOING!
        """
        UserRepository.list_collection.update_one(
            {"project_id": UserRepository.project_id}, {"$set": {"white": []}}
        )

    @staticmethod
    def _drop_shortlist():
        """
        Only use this method in a developer environment AND WHEN YOU'RE COMPLETELY SURE WHAT YOU ARE DOING!
        """
        UserRepository.list_collection.update_one(
            {"project_id": UserRepository.project_id}, {"$set": {"short": []}}
        )
