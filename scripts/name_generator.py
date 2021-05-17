#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import json
from modules.combine_words import combine_words


def sort_data(wordlist_filepath):

    with open(wordlist_filepath) as wordlist_file:
        words = json.load(wordlist_file)

    verbs = []
    nouns = []
    adjectives = []
    for word in words:
        if word["pos"] == "VERB":
            verbs.append(word["base"])
        elif word["pos"] == "NOUN":
            nouns.append(word["base"])
        elif word["pos"] == "ADJ":
            adjectives.append(word["base"])

    all_names = []

    print("Generating names with adjectives + nouns...")
    all_names += combine_words(adjectives, nouns)

    print("Generating names with verbs + nouns...")
    all_names += combine_words(verbs, nouns)

    names = "\n".join(all_names)

    with open(sys.argv[2], "w+") as out_file:
        out_file.write(names)


if __name__ == "__main__":
    sort_data(sys.argv[1])
