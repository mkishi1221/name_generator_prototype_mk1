from classes.user_repository.mutations.user_preferences import UserPreferenceMutations
from classes.user_repository.repository import UserRepository
import orjson as json
import pandas as pd
import os

try:
    os.mkdir("ref/mongo_entries")
except FileExistsError:
    pass

UserRepository.init_user()
print("Project ID:" + str(UserRepository.project_id))
print("Exporting black list...")
blacklist_dict = {word.keyword: word.__dict__ for word in UserPreferenceMutations.get_blacklisted()}
if blacklist_dict:
    blacklist_pd = pd.DataFrame.from_dict(blacklist_dict, orient="index")
    blacklist_pd.drop(
        [
            "word",
            "origin",
            "spacy_pos",
            "lemma",
            "algorithm"
        ],
        axis=1,
        inplace=True,
    )
    blacklist_pd.sort_values(['occurrence', 'keyword', 'wordsAPI_pos'], ascending=[False, True, False], inplace=True)
    blacklist_pd.to_excel("ref/mongo_entries/blacklist.xlsx", index=False)
else:
    print("No entries in black list")

print("Exporting grey list...")
greylist_dict = {word.keyword: word.__dict__ for word in UserPreferenceMutations.get_greylisted()}
if greylist_dict:
    greylist_pd = pd.DataFrame.from_dict(greylist_dict, orient="index")
    greylist_pd.drop(
        [
            "word",
            "origin",
            "spacy_pos",
            "lemma",
            "algorithm"
        ],
        axis=1,
        inplace=True,
    )
    greylist_pd.sort_values(['occurrence', 'keyword', 'wordsAPI_pos'], ascending=[False, True, False], inplace=True)
    greylist_pd.to_excel("ref/mongo_entries/greylist.xlsx", index=False)
else:
    print(" No entries in grey list")

print("Exporting white list...")
whitelist_dict = {word.keyword: word.__dict__ for word in UserPreferenceMutations.get_whitelisted()}
if whitelist_dict:
    whitelist_pd = pd.DataFrame.from_dict(whitelist_dict, orient="index")
    whitelist_pd.drop(
        [
            "word",
            "origin",
            "spacy_pos",
            "lemma",
            "algorithm"
        ],
        axis=1,
        inplace=True,
    )
    whitelist_pd.sort_values(['occurrence', 'keyword', 'wordsAPI_pos'], ascending=[False, True, False], inplace=True)
    whitelist_pd.to_excel("ref/mongo_entries/whitelist.xlsx", index=False)
else:
    print(" No entries in white list")

print("Exporting short list...")
shortlist_dict = {word.name: word.__dict__ for word in UserPreferenceMutations.get_shortlisted()}
if shortlist_dict:
    shortlist_pd = pd.DataFrame.from_dict(shortlist_dict, orient="index")
    shortlist_pd.sort_values(['name', 'length', 'algorithm'], ascending=[False, False, True], inplace=True)
    shortlist_pd.to_excel("ref/mongo_entries/shortlist.xlsx", index=False)
else:
    print(" No entries in short list")
