#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pandas as pd

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

    print("Calculating cumulative data...                  ")
    total = df['occurrence'].sum()
    df['cumulative_sum'] = df['occurrence'].cumsum()
    df['percentage'] = round(df['occurrence'] / total, 10)
    df['cumulative_percentage'] = round(df['percentage'].cumsum(), 3)
    df.insert(0, 'id', range(1, 1 + len(df)))

    df = df[['id', 'word', 'occurrence', 'cumulative_sum', 'percentage', 'cumulative_percentage']]

    print("Exporting output file...")
    df.to_csv(f"{output}.tsv", sep="\t")
    df.to_json(f"{output}.json", orient="records", indent=2)

get_total_word_count(directory, output)
