from classes.user_repository.mutations.user_preferences import UserPreferenceMutations
from classes.user_repository.repository import UserRepository
import orjson as json
import pandas as pd

UserRepository.init_user()
print("Exporting black list...")
blacklist_dict = { word.keyword:word.__dict__ for word in UserPreferenceMutations.get_blacklisted() }
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

print("Exporting grey list...")
greylist_dict = { word.keyword:word.__dict__ for word in UserPreferenceMutations.get_greylisted() }
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

print("Exporting white list...")
whitelist_dict = { word.keyword:word.__dict__ for word in UserPreferenceMutations.get_whitelisted() }
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

print("Exporting short list...")
shortlist_dict = { word.name:word.__dict__ for word in UserPreferenceMutations.get_shortlisted() }
shortlist_pd = pd.DataFrame.from_dict(shortlist_dict, orient="index")
shortlist_pd.sort_values(['name', 'length', 'algorithm'], ascending=[False, False, True], inplace=True)
shortlist_pd.to_excel("ref/mongo_entries/shortlist.xlsx", index=False)
