#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import pandas as pd
from os import path


# Create name shortlist or append existing name shortlist
def create_name_shortlist(file):
    df = pd.read_excel(file, index_col=0)

    # Get all names that have been marked "w" (for "whitelisted")
    df_shortlist = df.loc[df['Name and Domain check'] == 'w']

    #Remove unwanted columns
    df_shortlist.drop(['Name and Domain check', 'Keyword 1 check', 'Keyword 2 check'], axis=1, inplace=True)
    df_shortlist.fillna('', inplace=True)
    shortlist = df_shortlist.to_dict('records')

    # Load pre-exisiting name shortlist file if exists and add data. If not exists, make new shortlist file
    if path.exists('ref/name_shortlist.json'):
        with open('ref/name_shortlist.json', "rb") as name_shortlist_file:
            name_shortlist = json.loads(name_shortlist_file.read())
        for name in shortlist:
            if name not in shortlist:
                name_shortlist.append(name)
    else:
        name_shortlist = shortlist.copy()

    with open("ref/name_shortlist.json", "w+") as out_file:
        json.dump(name_shortlist, out_file, ensure_ascii=False, indent=1)


# Create keyword blacklist
def create_keyword_blacklist(file):
    df = pd.read_excel(file, index_col=0)

    # Get all keywords (in keyword1 column) that have been marked "b" (for "blacklisted")
    keyword_blacklist_df1 = df.loc[df['Keyword 1 check'] == 'b']
    # Remove unwanted columns
    keyword_blacklist_df1.drop(['Name and Domain check', 'Keyword 1 check', 'keyword2', 'Keyword 2 check'], axis=1, inplace=True)
    # Rename keyword1 column as 'keyword'
    keyword_blacklist_df1['keyword'] = keyword_blacklist_df1.pop('keyword1')
    # Get pos data from algorithm (For keyword 1, its first word in the algorithm column) and add to new pos column
    keyword_blacklist_df1['pos'] = keyword_blacklist_df1['algorithm'].map(lambda v: v.split(' + ')[0])

    # Get all keywords (in keyword2 column) that have been marked "b" (for "blacklisted")
    keyword_blacklist_df2 = df.loc[df['Keyword 2 check'] == 'b']
    # Remove unwanted columns
    keyword_blacklist_df2.drop(['Name and Domain check', 'Keyword 1 check', 'keyword1', 'Keyword 2 check'], axis=1, inplace=True)
    # Rename keyword2 column as 'keyword'
    keyword_blacklist_df2['keyword'] = keyword_blacklist_df2.pop('keyword2')
    # Get pos data from algorithm (For keyword 1, its first word in the algorithm column) and add to new pos column
    keyword_blacklist_df2['pos'] = keyword_blacklist_df2['algorithm'].map(lambda v: v.split(' + ')[-1])

    # Combine both keyword1 and keyword2 df
    keyword_blacklist_df = pd.concat([keyword_blacklist_df1, keyword_blacklist_df2])

    keyword_blacklist_df.fillna('', inplace=True)
    keyword_blacklist = keyword_blacklist_df.to_dict('records')

    with open("ref/keyword_blacklist.json", "w+") as out_file:
        json.dump(keyword_blacklist, out_file, ensure_ascii=False, indent=1)


file = 'samples/names_20210618_072058.xlsx'

create_name_shortlist(file)
create_keyword_blacklist(file)
