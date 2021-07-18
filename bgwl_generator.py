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
    UserPreferenceMutations._drop_greylist()
    UserPreferenceMutations._drop_blacklist()

    shortlist = []
    whitelist = []
    greylist = []
    blacklist = []

    # Loop through multiple excel files
    # TODO: In the next update I'm thinking to output the names into the same excel spreadsheet to cut down on time.
    for file in glob.glob(f"{directory}/*.xlsx"):
        count += 1
        df = pd.read_excel(file, index_col=0)

        # Create name shortlist
        # Get all names that have been marked "w" (for "whitelisted")
        df_shortlist = df.loc[df["Name and Domain check"] == "w"].copy()

        # Replace Nan with empty string
        df_shortlist.fillna("", inplace=True)

        # Remove unwanted columns
        df_shortlist.drop(
            ["Name and Domain check", "Keyword 1 check", "Keyword 2 check"],
            axis=1,
            inplace=True,
        )
        # Convert df to dict and add to local shortlist
        shortlist += df_shortlist.to_dict(orient="records")

        # Create keyword whitelist
        # Get all keywords (in keyword1 column) that have been marked "b" (for "blacklisted")
        kwwl_df1 = df.loc[(df["Keyword 1 check"] == "w") & (df["Name and Domain check"] == "w")].copy()
        # Replace Nan with empty string
        kwwl_df1.fillna("", inplace=True)
        # Get keyword (the first entry in the keyword tuple) and add to new keyword column
        kwwl_df1.loc[:, "keyword"] = kwwl_df1.keyword1.str.lower().str[2:-2].str.split("', '").str.get(0)
        # Get pos data (the second entry in the keyword tuple) and add to new pos column
        kwwl_df1.loc[:, "wordsAPI_pos"] = kwwl_df1.keyword1.str.lower().str[2:-2].str.split("', '").str.get(1)
        # Remove unwanted columns
        kwwl_df1.drop(
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
        kwwl_df2 = df.loc[df["Keyword 2 check"] == "b"].copy()
        # Replace Nan with empty string
        kwwl_df2.fillna("", inplace=True)
        # Get keyword (the first entry in the keyword tuple) and add to new keyword column
        kwwl_df2.loc[:, "keyword"] = kwwl_df2.keyword2.str.lower().str[2:-2].str.split("', '").str.get(0)
        # Get pos data (the second entry in the keyword tuple) and add to new pos column
        kwwl_df2.loc[:, "wordsAPI_pos"] = kwwl_df2.keyword2.str.lower().str[2:-2].str.split("', '").str.get(1)
        # Remove unwanted columns
        kwwl_df2.drop(
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
        keyword_whitelist_df = pd.concat([kwwl_df1, kwwl_df2])
        keyword_whitelist_df.fillna("", inplace=True)
        keyword_whitelist_df["keyword_len"] = keyword_whitelist_df["keyword"].str.len()
        keyword_whitelist_df = keyword_whitelist_df[
            ["keyword_len", "keyword", "wordsAPI_pos", "algorithm", "name"]
        ]
        # Convert df to json and add to local shortlist
        whitelist += keyword_whitelist_df.to_dict(orient="records")

        # Create keyword greylist
        # Greylist contains keywords that have neither been blacklisted or whitelisted and are assumed to be uninteresting to the user.
        # Multiple occurrences of greylisted keywords suggest that the keyword should be removed to mow down the number of possibilities.
        # Currently it's 3 times but that number is preliminary and can be changed.
        # TODO: Create shortlisted keyword functionality that will prevent whitelisted keywords from accidentally ending up in blacklist.
        # Get all keywords (in keyword1 column) that have not been marked (empty cells)
        kwgl_df1 = df.loc[df["Keyword 1 check"].isna()].copy()
        # Replace Nan with empty string
        kwgl_df1.fillna("", inplace=True)
        # Get keyword (the first entry in the keyword tuple) and add to new keyword column
        kwgl_df1.loc[:, "keyword"] = kwgl_df1.keyword1.str.lower().str[2:-2].str.split("', '").str.get(0)
        # Get pos data (the second entry in the keyword tuple) and add to new pos column
        kwgl_df1.loc[:, "wordsAPI_pos"] = kwgl_df1.keyword1.str.lower().str[2:-2].str.split("', '").str.get(1)
        # Remove unwanted columns
        kwgl_df1.drop(
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
        kwgl_df2 = df.loc[df["Keyword 2 check"].isna()].copy()
        # Replace Nan with empty string
        kwgl_df2.fillna("", inplace=True)
        # Get keyword (the first entry in the keyword tuple) and add to new keyword column
        kwgl_df2.loc[:, "keyword"] = kwgl_df2.keyword2.str.lower().str[2:-2].str.split("', '").str.get(0)
        # Get pos data (the second entry in the keyword tuple) and add to new pos column
        kwgl_df2.loc[:, "wordsAPI_pos"] = kwgl_df2.keyword2.str.lower().str[2:-2].str.split("', '").str.get(1)
        # Remove unwanted columns
        kwgl_df2.drop(
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
        keyword_greylist_df = pd.concat([kwgl_df1, kwgl_df2])
        keyword_greylist_df.fillna("", inplace=True)
        keyword_greylist_df["keyword_len"] = keyword_greylist_df["keyword"].str.len()
        keyword_greylist_df = keyword_greylist_df[
            ["keyword_len", "keyword", "wordsAPI_pos", "algorithm", "name"]
        ]
        greylist += keyword_greylist_df.to_dict(orient="records")

        # Create keyword blacklist
        # Get all keywords (in keyword1 column) that have been marked "b" (for "blacklisted")
        kwbl_df1 = df.loc[df["Keyword 1 check"] == "b"].copy()
        # Replace Nan with empty string
        kwbl_df1.fillna("", inplace=True)
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
        # Replace Nan with empty string
        kwbl_df2.fillna("", inplace=True)
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
        # Convert df to json and add to local shortlist
        for keyword in keyword_blacklist_df.to_dict(orient="records"):
            if not any(d['keyword'] == keyword['keyword'] for d in whitelist):
                blacklist.append(keyword)

        print(f"Processed {count} file...", end="\r")

    print(f"All {count} files processed. Preparing to upsert data...")
    # Upload shortlist to database
    print("Upserting shortlist...")
    UserPreferenceMutations.upsert_multiple_keywords_in_shortlist(
        list({Name(**word) for word in shortlist})
    )

    # Upload whitelist to database
    print("Upserting whitelist...")
    UserPreferenceMutations.upsert_multiple_keywords_in_whitelist(
        list(BlackGreyWhiteListEntry.schema().loads(json.dumps(whitelist), many=True))
    )

    # Upload greylist to database
    print("Upserting greylist...")
    UserPreferenceMutations.upsert_multiple_keywords_in_greylist(
        list(BlackGreyWhiteListEntry.schema().loads(json.dumps(greylist), many=True))
    )

    # If a keyword is neither blacklisted or whitelisted 3 times in a row, add to blacklist. (This helps to mow down uninteresting keywords)
    filtered_greylist = []
    keyword_greylist_db = UserPreferenceMutations.get_greylisted()

    for keyword in keyword_greylist_db:
        if keyword['occurrence'] >= 3 and not any(d['keyword'] == keyword['keyword'] for d in whitelist):
            del keyword['occurrence']
            filtered_greylist.append(keyword)
    blacklist += filtered_greylist

    # Upload blacklist to database
    print("Upserting blacklist...")
    UserPreferenceMutations.upsert_multiple_keywords_in_blacklist(
        list(BlackGreyWhiteListEntry.schema().loads(json.dumps(filtered_greylist), many=True))
    )


UserRepository.init_user()
try:
    directory = sys.argv[1]
except IndexError:
    directory = 'results/'

process_user_feedback(directory)

