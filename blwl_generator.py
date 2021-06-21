#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import orjson as json
import pandas as pd
from os import path
import os
from classes.name import Name


# Create name shortlist or append existing name shortlist
def create_name_shortlist(directory):

    # Load pre-exisiting name shortlist file if exists and add data. If not exists, make new shortlist file
    if path.exists('ref/name_shortlist.json'):
        with open('ref/name_shortlist.json', "rb") as name_shortlist_file:
            master_shortlist = json.loads(name_shortlist_file.read())
        master_shortlist = [Name(**x) for x in master_shortlist]
    else:
        master_shortlist = []

    # Loop through all result files ending with .xlsx
    directory = os.fsencode(directory)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".xlsx"):
            file = str(directory, 'utf-8') + str(file, 'utf-8')
            df = pd.read_excel(file, index_col=0)

            # Get all names that have been marked "w" (for "whitelisted")
            df_shortlist = df.loc[df['Name and Domain check'] == 'w']

            # Remove unwanted columns
            df_shortlist.drop(['Name and Domain check', 'Keyword 1 check', 'Keyword 2 check'], axis=1, inplace=True)
            # Replace Nan with empty string
            df_shortlist.fillna('', inplace=True)

            # Convert df to dict
            shortlist = df_shortlist.to_dict('records')
            shortlist = [Name(**x) for x in shortlist]

            # Add shortlisted names to master shortlist
            for name in shortlist:
                if name not in master_shortlist:
                    master_shortlist.append(name)

    # Export master name shortlist as json file
    with open("ref/name_shortlist.json", "wb+") as out_file:
        out_file.write(json.dumps(master_shortlist, option=json.OPT_INDENT_2))

# Create keyword blacklist
def create_keyword_blacklist(directory):

    # Load pre-exisiting keyword blacklist file if exists and add data. If not exists, make new blacklist file
    if path.exists('ref/keyword_blacklist.json'):
        with open('ref/keyword_blacklist.json', "rb") as keyword_blacklist_file:
            keyword_blacklist = json.loads(keyword_blacklist_file.read())
    else:
        keyword_blacklist = []

    # Loop through all result files ending with .xlsx
    directory = os.fsencode(directory)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".xlsx"):
            file = str(directory, 'utf-8') + str(file, 'utf-8')
            df = pd.read_excel(file, index_col=0)

            # Get all keywords (in keyword1 column) that have been marked "b" (for "blacklisted")
            keyword_blacklist_df1 = df.loc[df['Keyword 1 check'] == 'b']
            # Remove unwanted columns
            keyword_blacklist_df1.drop(
                ['Name and Domain check', 'Keyword 1 check', 'keyword2', 'Keyword 2 check', 'length', 'domain', 'all_keywords'],
                axis=1,
                inplace=True
            )
            # Rename keyword1 column as 'keyword'
            keyword_blacklist_df1['keyword'] = keyword_blacklist_df1.pop('keyword1')
            # Get pos data from algorithm (For keyword 1, its first word in the algorithm column) and add to new pos column
            keyword_blacklist_df1['wordsAPI_pos'] = keyword_blacklist_df1['algorithm'].map(lambda v: v.split(' + ')[0])

            # Get all keywords (in keyword2 column) that have been marked "b" (for "blacklisted")
            keyword_blacklist_df2 = df.loc[df['Keyword 2 check'] == 'b']
            # Remove unwanted columns
            keyword_blacklist_df2.drop(
                ['Name and Domain check', 'Keyword 1 check', 'keyword1', 'Keyword 2 check', 'length', 'domain', 'all_keywords'],
                axis=1,
                inplace=True
            )
            # Rename keyword2 column as 'keyword'
            keyword_blacklist_df2['keyword'] = keyword_blacklist_df2.pop('keyword2')
            # Get pos data from algorithm (For keyword 1, its first word in the algorithm column) and add to new pos column
            keyword_blacklist_df2['wordsAPI_pos'] = keyword_blacklist_df2['algorithm'].map(lambda v: v.split(' + ')[-1])

            # Combine both keyword1 and keyword2 df
            keyword_blacklist_df = pd.concat([keyword_blacklist_df1, keyword_blacklist_df2])
            keyword_blacklist_df.fillna('', inplace=True)
            keyword_blacklist_df['keyword_len'] = keyword_blacklist_df['keyword'].str.len()
            keyword_blacklist_df = keyword_blacklist_df[['keyword_len', 'keyword', 'wordsAPI_pos', 'algorithm', 'name']]
            tmp_keyword_blacklist = keyword_blacklist_df.to_dict('records')
            
            # Add blacklisted keywords to master blacklist
            for keyword in tmp_keyword_blacklist:
                if keyword not in keyword_blacklist:
                    keyword_blacklist.append(keyword)

    with open("ref/keyword_blacklist.json", "wb+") as out_file:
        out_file.write(json.dumps(keyword_blacklist, option=json.OPT_INDENT_2))

directory = 'samples/'
create_name_shortlist(directory)
create_keyword_blacklist(directory)
