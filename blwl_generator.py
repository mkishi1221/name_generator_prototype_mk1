#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from classes.user_repository.repository import UserRepository
from classes.user_repository.mutations.user_preferences import UserPreferenceMutations
from models.bwl_entry import BlackWhiteListEntry
import pandas as pd
import glob
import sys
from classes.name import Name


# Create name shortlist or append existing name shortlist
def create_name_shortlist(directory):

    UserRepository.init_user()
    UserPreferenceMutations._drop_shortlist()

    for file in glob.glob(f"{directory}/*.xlsx"):
        df = pd.read_excel(file, index_col=0)

        # Get all names that have been marked "w" (for "whitelisted")
        df_shortlist = df.loc[df["Name and Domain check"] == "w"].copy()

        # Remove unwanted columns
        df_shortlist.drop(
            ["Name and Domain check", "Keyword 1 check", "Keyword 2 check"],
            axis=1,
            inplace=True,
        )
        # Replace Nan with empty string
        df_shortlist.fillna("", inplace=True)

        # Convert df to dict
        shortlist = df_shortlist.to_dict("records")
        UserPreferenceMutations.upsert_multiple_keywords_in_shortlist(
            list({Name(**word) for word in shortlist})
        )


# Create keyword blacklist
def create_keyword_blacklist(directory):

    UserRepository.init_user()
    UserPreferenceMutations._drop_blacklist()

    for file in glob.glob(f"{directory}/*.xlsx"):
        df = pd.read_excel(file, index_col=0)

        # Get all keywords (in keyword1 column) that have been marked "b" (for "blacklisted")
        kwbl_df1 = df.loc[df["Keyword 1 check"] == "b"].copy()

        # Get pos data from algorithm (For keyword 1, its first word in the algorithm column) and add to new pos column
        kwbl_df1.loc[:, "keyword"] = kwbl_df1.keyword1.str[1:-1].str.split("','").str.get(0)

        # Get pos data from algorithm (For keyword 1, its first word in the algorithm column) and add to new pos column
        kwbl_df1.loc[:, "wordsAPI_pos"] = kwbl_df1.keyword1.str[1:-1].str.split("','").str.get(1)

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

        # Get pos data from algorithm (For keyword 2, its first word in the algorithm column) and add to new pos column
        kwbl_df2.loc[:, "keyword"] = kwbl_df2.keyword2.str[1:-1].str.split("','").str.get(0)

        # Get pos data from algorithm (For keyword 2, its first word in the algorithm column) and add to new pos column
        kwbl_df2.loc[:, "wordsAPI_pos"] = kwbl_df2.keyword2.str[1:-1].str.split("','").str.get(1)

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

        records = keyword_blacklist_df.to_json(orient="records")

        UserPreferenceMutations.upsert_multiple_keywords_in_blacklist(
            list(set(BlackWhiteListEntry.schema().loads(records, many=True)))
        )


UserRepository.init_user()
directory = sys.argv[1]
create_name_shortlist(directory)
create_keyword_blacklist(directory)
