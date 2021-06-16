#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import json
from modules.combine_words import combine_words
from classes.names import NameEncoder
from classes.algorithm import Algorithm
from numpy import nan
import pandas as pd


# Generate name ideas
def sort_data(wordlist_filepath):

    # Access keyword list and sort words into verbs, nouns or adjectives
    with open(wordlist_filepath) as wordlist_file:
        words = json.load(wordlist_file)
    verbs = []
    nouns = []
    adjectives = []
    for word in words:
        if word["wordsAPI_pos"] == "verb":
            verbs.append(word["base"].title())
        elif word["wordsAPI_pos"] == "noun":
            nouns.append(word["base"].title())
        elif word["wordsAPI_pos"] == "adjective":
            adjectives.append(word["base"].title())

    # Access prefix dictionary and load data into prefix list
    with open("dict/prefix.json") as prefixlist_file:
        prefixes_json = json.load(prefixlist_file)
    prefixes = [prefix_obj["prefix"] for prefix_obj in prefixes_json]

    # Access suffix dictionary and load data into suffix list
    with open("dict/suffix.json") as suffixlist_file:
        suffixes_json = json.load(suffixlist_file)
    suffixes = [suffix_obj["suffix"] for suffix_obj in suffixes_json]

    # Add all lists into dict form
    keyword_dict = {'verb': verbs, 'noun': nouns, 'adjective': adjectives, 'prefix': prefixes, 'suffix': suffixes}

    # Import algorithm list from xlsx file
    df = pd.read_excel('algorithm_list.xlsx', index_col=0)
    algorithm_df = df[df['deactivate'].isna()]

    algorithm_list = []
    for index, row in algorithm_df.iterrows():
        algorithm = Algorithm(row['keyword_1'], row['keyword_2'], row['joint'])
        if algorithm not in algorithm_list:
            algorithm_list.append(algorithm)

    # Generate names by combining two keywords together

    all_names = []

    for algorithm in algorithm_list:

        keyword_1 = str(algorithm.keyword_1)
        keyword_2 = str(algorithm.keyword_2)

        # Check if keyword exists in keyword_dict:
        if keyword_1 not in keyword_dict or keyword_2 not in keyword_dict:
            if keyword_1 not in keyword_dict:
                print(f"{keyword_1} not a valid type of keyword!")
            if keyword_2 not in keyword_dict:
                print(f"{keyword_2} not a valid type of keyword!")
        else:
            if str(algorithm.joint) == 'nan':
                print(f"Generating names with {keyword_1} + {keyword_2}...")
                all_names += combine_words(keyword_dict[keyword_1], keyword_dict[keyword_2], f"{keyword_1} + {keyword_2}")             
            else:
                joint = str(algorithm.joint)
                print(f"Generating names with {keyword_1} + {joint} + {keyword_2}...")
                all_names += combine_words(keyword_dict[keyword_1], keyword_dict[keyword_2], f"{keyword_1} + {keyword_2}", joint)

    with open(sys.argv[2], "w+") as out_file:
        json.dump(all_names, out_file, cls=NameEncoder, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sort_data(sys.argv[1])
