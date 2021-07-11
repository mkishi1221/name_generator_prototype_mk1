#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from classes.user_repository.repository import UserRepository
from classes.user_repository.mutations.user_preferences import UserPreferenceMutations
from models.bgwl_entry import BlackGreyWhiteListEntry
import pandas as pd
import glob
import sys
from classes.name import Name
from classes.keyword import Keyword
import orjson as json


# Create name shortlist or append existing name shortlist
def process_user_feedback(directory):

    count = 0
    UserRepository.init_user()
    UserPreferenceMutations._drop_shortlist()

    # Looping through multiple excel files is really slow :(
    # TODO: In the next update I'm thinking to output the names into the same excel spreadsheet to cut down on time.
    for file in glob.glob(f"{directory}/*.xlsx"):
        count += 1
        df = pd.read_excel(file, index_col=0)

        # Replace Nan with empty string
        df.fillna("", inplace=True)

        # Create name shortlist
        # Get all names that have been marked "w" (for "whitelisted")
        df_shortlist = df.loc[df["Name and Domain check"] == "w"].copy()
        # Remove unwanted columns
        df_shortlist.drop(
            ["Name and Domain check", "Keyword 1 check", "Keyword 2 check"],
            axis=1,
            inplace=True,
        )
        # Convert df to dict
        shortlist = df_shortlist.to_dict("records")
        UserPreferenceMutations.upsert_multiple_keywords_in_shortlist(
            list({Name(**word) for word in shortlist})
        )

        # Create keyword greylist
        # Greylist contains keywords that have neither been blacklisted or whitelisted and are assumed to be uninteresting to the user.
        # Multiple occurrences of greylisted keywords suggest that the keyword should be removed to mow down the number of possibilities.
        # Currently it's 3 times but that number is preliminary and can be changed.
        # TODO: Create shortlisted keyword functionality that will prevent whitelisted keywords from accidentally ending up in blacklist.
        # Get all keywords (in keyword1 column) that have not been marked (empty cells)
        kwgr_df1 = df.loc[df["Keyword 1 check"].isna()].copy()
        # Get keyword (the first entry in the keyword tuple) and add to new keyword column
        kwgr_df1.loc[:, "keyword"] = kwgr_df1.keyword1.str.lower().str[2:-2].str.split("', '").str.get(0)
        # Get pos data (the second entry in the keyword tuple) and add to new pos column
        kwgr_df1.loc[:, "wordsAPI_pos"] = kwgr_df1.keyword1.str.lower().str[2:-2].str.split("', '").str.get(1)
        # Remove unwanted columns
        kwgr_df1.drop(
            [
                "Name and Domain check",
                "keyword1",
                "Keyword 1 check",
                "keyword2",
                "Keyword 2 check",
                "length",
                "domain",
                "all_keywords",
            ],
            axis=1,
            inplace=True,
        )
        # Get all keywords (in keyword2 column) that have been marked "b" (for "blacklisted")
        kwgr_df2 = df.loc[df["Keyword 2 check"].isna()].copy()
        # Get keyword (the first entry in the keyword tuple) and add to new keyword column
        kwgr_df2.loc[:, "keyword"] = kwgr_df2.keyword2.str.lower().str[2:-2].str.split("', '").str.get(0)
        # Get pos data (the second entry in the keyword tuple) and add to new pos column
        kwgr_df2.loc[:, "wordsAPI_pos"] = kwgr_df2.keyword2.str.lower().str[2:-2].str.split("', '").str.get(1)
        # Remove unwanted columns
        kwgr_df2.drop(
            [
                "Name and Domain check",
                "Keyword 1 check",
                "keyword1",
                "Keyword 2 check",
                "keyword2",
                "length",
                "domain",
                "all_keywords",
            ],
            axis=1,
            inplace=True,
        )
        # Combine both keyword1 and keyword2 df
        keyword_greylist_df = pd.concat([kwgr_df1, kwgr_df2])
        keyword_greylist_df.fillna("", inplace=True)
        keyword_greylist_df["keyword_len"] = keyword_greylist_df["keyword"].str.len()
        keyword_greylist_df = keyword_greylist_df[
            ["keyword_len", "keyword", "wordsAPI_pos", "algorithm", "name"]
        ]
        greylist = keyword_greylist_df.to_json(orient="records")
        UserPreferenceMutations.upsert_multiple_keywords_in_greylist(
            list(set(BlackGreyWhiteListEntry.schema().loads(greylist, many=True)))
        )

        # Create keyword blacklist
        # Get all keywords (in keyword1 column) that have been marked "b" (for "blacklisted")
        kwbl_df1 = df.loc[df["Keyword 1 check"] == "b"].copy()
        # Get keyword (the first entry in the keyword tuple) and add to new keyword column
        kwbl_df1.loc[:, "keyword"] = kwbl_df1.keyword1.str.lower().str[2:-2].str.split("', '").str.get(0)
        # Get pos data (the second entry in the keyword tuple) and add to new pos column
        kwbl_df1.loc[:, "wordsAPI_pos"] = kwbl_df1.keyword1.str.lower().str[2:-2].str.split("', '").str.get(1)
        # Remove unwanted columns
        kwbl_df1.drop(
            [
                "Name and Domain check",
                "keyword1",
                "Keyword 1 check",
                "keyword2",
                "Keyword 2 check",
                "length",
                "domain",
                "all_keywords",
            ],
            axis=1,
            inplace=True,
        )
        # Get all keywords (in keyword2 column) that have been marked "b" (for "blacklisted")
        kwbl_df2 = df.loc[df["Keyword 2 check"] == "b"].copy()
        # Get keyword (the first entry in the keyword tuple) and add to new keyword column
        kwbl_df2.loc[:, "keyword"] = kwbl_df2.keyword2.str.lower().str[2:-2].str.split("', '").str.get(0)
        # Get pos data (the second entry in the keyword tuple) and add to new pos column
        kwbl_df2.loc[:, "wordsAPI_pos"] = kwbl_df2.keyword2.str.lower().str[2:-2].str.split("', '").str.get(1)
        # Remove unwanted columns
        kwbl_df2.drop(
            [
                "Name and Domain check",
                "Keyword 1 check",
                "keyword1",
                "Keyword 2 check",
                "keyword2",
                "length",
                "domain",
                "all_keywords",
            ],
            axis=1,
            inplace=True,
        )
        # Combine both keyword1 and keyword2 df
        keyword_blacklist_df = pd.concat([kwbl_df1, kwbl_df2])
        keyword_blacklist_df.fillna("", inplace=True)
        keyword_blacklist_df["keyword_len"] = keyword_blacklist_df["keyword"].str.len()
        keyword_blacklist_df = keyword_blacklist_df[
            ["keyword_len", "keyword", "wordsAPI_pos", "algorithm", "name"]
        ]
        blacklist = keyword_blacklist_df.to_json(orient="records")
        UserPreferenceMutations.upsert_multiple_keywords_in_blacklist(
            list(set(BlackGreyWhiteListEntry.schema().loads(blacklist, many=True)))
        )

        print(f"Processed {count} file...", end="\r")

    # If a keyword is neither blacklisted or whitelisted 3 times in a row, add to blacklist. (This helps to mow down uninteresting keywords)
    filtered_greylist = []
    UserRepository.init_user()
    keyword_greylist_db = UserPreferenceMutations.get_greylisted()

    for keyword in keyword_greylist_db:
        if keyword['occurrence'] >= 3:
            del keyword['occurrence']
            filtered_greylist.append(keyword)

    UserPreferenceMutations.upsert_multiple_keywords_in_blacklist(
        list(set(BlackGreyWhiteListEntry.schema().loads(json.dumps(filtered_greylist), many=True)))
    )


UserRepository.init_user()
try:
    directory = sys.argv[1]
except IndexError:
    directory = 'results/'

process_user_feedback(directory)
