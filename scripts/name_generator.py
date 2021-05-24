#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import json
from modules.combine_words import combine_words

# Generate name ideas
def sort_data(wordlist_filepath):

    # Access keyword list and sort words into verbs, nouns or adjectives
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

    # Access prefix dictionary and load data into prefix list
    with open("dict/prefix.json") as prefixlist_file:
        prefixes_json = json.load(prefixlist_file)
    prefixes = [prefix_obj["prefix"] for prefix_obj in prefixes_json]

    # Access suffix dictionary and load data into suffix list
    with open("dict/suffix.json") as suffixlist_file:
        suffixes_json = json.load(suffixlist_file)
    suffixes = [suffix_obj["suffix"] for suffix_obj in suffixes_json]

    all_names = []

    # Generate names by combining two keywords together

    print("Generating names with adjectives + nouns...")
    all_names += combine_words(adjectives, nouns)

    print("Generating names with verbs + nouns...")
    all_names += combine_words(verbs, nouns)

    print("Generating names with prefixes + nouns...")
    all_names += combine_words(prefixes, nouns)

    print("Generating names with prefixes + nouns...")
    all_names += combine_words(nouns, suffixes)
    
    # Generate names by combining two keywords together and insert "AND" inbetween them

    print("Generating names with nouns + & + nouns...")
    all_names += combine_words(nouns, nouns, "AND")

    # Export all generated names
    names = "\n".join(all_names)
    with open(sys.argv[2], "w+") as out_file:
        out_file.write(names)

if __name__ == "__main__":
    sort_data(sys.argv[1])
