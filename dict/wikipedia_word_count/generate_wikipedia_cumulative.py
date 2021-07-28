#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import orjson as json

directory = "dict/wikipedia_word_count/original_data/wikipedia-en-words.tsv"
output = "dict/wikipedia_word_count/wikipedia-en-words-cumulative"

def get_total_word_count(directory, output):

    print("Parsing original file...")
    df_original = pd.read_csv(directory, delimiter='\t', header=None, names=['word', 'occurrence'])
    list_original = [list(row) for row in df_original.values]
    list_original.sort(key=lambda x: str(x[0]).casefold())

    print("Reducing list...")
    list_reduced = []
    prev_word = ""
    prev_occurrence = 0
    for row in list_original:
        word = str(row[0]).lower()
        if prev_word != word and len(word) > 2:
            list_reduced.append([prev_word, prev_occurrence])
            prev_word = str(row[0]).lower()
            prev_occurrence = row[1]
        elif prev_word == word:
            prev_occurrence += row[1]
    list_reduced.append([prev_word, prev_occurrence])
    list_reduced.sort(key=lambda x: int(x[1]), reverse=True)
    df = pd.DataFrame.from_records(list_reduced, columns=['word', 'occurrence'])

    print("Calculating cumulative data and assigning keyword scores...                  ")
    total = df['occurrence'].sum()
    df['cumulative_sum'] = df['occurrence'].cumsum()
    df['percentage'] = round(df['occurrence'] / total, 10)
    df['cumulative_percentage'] = round(df['percentage'].cumsum(), 3)

    # list of keyword score conditions
    conditions = [
        (df['cumulative_percentage'].astype(float) <= 0.70),
        (df['cumulative_percentage'].astype(float) > 0.70) & (df['cumulative_percentage'].astype(float) <= 0.80),
        (df['cumulative_percentage'].astype(float) > 0.80) & (df['cumulative_percentage'].astype(float) <= 0.90),
        (df['cumulative_percentage'].astype(float) > 0.90) & (df['cumulative_percentage'].astype(float) <= 0.99),
        (df['cumulative_percentage'].astype(float) > 0.99)
    ]
    # keyword_scores for each condition
    values = [1, 2, 3, 2, 1]
    # create a new column containing keyword scores
    df['keyword_score'] = np.select(conditions, values)

    df.insert(0, 'id', range(1, 1 + len(df)))
    df = df[['id', 'word', 'occurrence', 'cumulative_sum', 'percentage', 'cumulative_percentage', 'keyword_score']]

    print("Creating dict format...")
    wiki_dict = {}
    wiki_dict_tmp = df.to_dict('records')
    for data in wiki_dict_tmp:
        keyword = data['word']
        del data['word']
        wiki_dict[keyword] = data

    print("Exporting output files...")
    df.to_csv(f"{output}.tsv", sep="\t")
    with open(f"{output}.json", "wb+") as out_file:
        out_file.write(json.dumps(wiki_dict, option=json.OPT_INDENT_2))


get_total_word_count(directory, output)
