#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import orjson as json
from modules.combine_words import combine_words
from classes.permanent_repository.repository import PermanentRepository
from classes.algorithm import Algorithm
import pandas as pd


# Generate name ideas
def sort_data(wordlist_filepath):

    # Access keyword list and sort words into verbs, nouns or adjectives
    with open(wordlist_filepath, "rb") as wordlist_file:
        words = json.loads(wordlist_file.read())
    verbs = []
    nouns = []
    adjectives = []
    for word in words:
        if word["wordsAPI_pos"] == "verb":
            verbs.append(word)
        elif word["wordsAPI_pos"] == "noun":
            nouns.append(word)
        elif word["wordsAPI_pos"] == "adjective":
            adjectives.append(word)

    # Access prefix dictionary and load data into prefix list
    prefixes = [prefix_obj for prefix_obj in PermanentRepository.prefixes.find()]

    # Access suffix dictionary and load data into suffix list
    suffixes = [suffix_obj for suffix_obj in PermanentRepository.suffixes.find()]

    # Add all lists into dict form
    keyword_dict = {
        "verb": verbs,
        "noun": nouns,
        "adjective": adjectives,
        "prefix": prefixes,
        "suffix": suffixes,
    }

    # Import algorithm list from xlsx file
    df = pd.read_excel("algorithm_list.xlsx", index_col=0)
    algorithm_df = df[df["deactivate"].isna()]

    # keep, in case we move away from xlsx
    def rmv_uknown_type(type: str):
        if type not in keyword_dict:
            print(f"{type} not a valid type of keyword!")
            return False
        return True

    algorithms = {
        Algorithm(row["keyword_type_1"], row["keyword_type_2"], row["joint"])
        for index, row in algorithm_df.iterrows()
    }  # if rmv_uknown_type(row['keyword_type_1']) and rmv_uknown_type(row['keyword_type_2'])

    # Generate names by combining two keywords together
    def combine(alg: Algorithm):
        print(
            f"Generating names with {alg}..."
        )
        return combine_words(
            keyword_dict[alg.keyword_type_1],
            alg.keyword_type_1,
            keyword_dict[alg.keyword_type_2],
            alg.keyword_type_2,
            alg,
        )

    all_names = [name for alg in algorithms for name in combine(alg)]
    all_names = sorted(all_names, key=lambda k: (k.name_score * -1, k.name))

    with open(sys.argv[2], "wb+") as out_file:
        # remove below indent when no further debug needed for more speeeeeed
        out_file.write(json.dumps(all_names, option=json.OPT_SERIALIZE_DATACLASS | json.OPT_INDENT_2))


if __name__ == "__main__":
    sort_data(sys.argv[1])
