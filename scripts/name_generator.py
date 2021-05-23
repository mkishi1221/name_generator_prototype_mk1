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
            verbs.append(word["base"].title())
        elif word["pos"] == "NOUN":
            nouns.append(word["base"].title())
        elif word["pos"] == "ADJ":
            adjectives.append(word["base"].title())


    with open("dict/prefix.json") as prefixlist_file:
        prefixes_json = json.load(prefixlist_file)
    prefixes = []
    for prefix in prefixes_json:
        prefixes.append(prefix["prefix"])


    with open("dict/suffix.json") as suffixlist_file:
        suffixes_json = json.load(suffixlist_file)
    suffixes = []
    for suffix in suffixes_json:
        suffixes.append(suffix["suffix"])

    all_names = []

    print("Generating names with adjectives + nouns...")
    all_names += combine_words(adjectives, nouns)

    print("Generating names with verbs + nouns...")
    all_names += combine_words(verbs, nouns)

    print("Generating names with prefixes + nouns...")
    all_names += combine_words(prefixes, nouns)

    print("Generating names with prefixes + nouns...")
    all_names += combine_words(nouns, suffixes)
    
    print("Generating names with nouns + & + nouns...")
    all_names += combine_words(nouns, nouns, "AND")

    names = "\n".join(all_names)

    with open(sys.argv[2], "w+") as out_file:
        out_file.write(names)

if __name__ == "__main__":
    sort_data(sys.argv[1])
