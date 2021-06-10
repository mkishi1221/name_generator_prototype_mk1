#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import json
from modules.combine_words import combine_words
from classes.names import NameEncoder

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

    all_names = []

    # Generate names by combining two keywords together

    print("Generating names with adjectives + nouns...")
    all_names += combine_words(adjectives, nouns, "adjective + noun")

    print("Generating names with verbs + nouns...")
    all_names += combine_words(verbs, nouns, "verb + noun")

    print("Generating names with verbs + verbs...")
    all_names += combine_words(verbs, verbs, "verb + verb")

    print("Generating names with prefixes + nouns...")
    all_names += combine_words(prefixes, nouns, "prefix + noun")

    print("Generating names with nouns + suffixes...")
    all_names += combine_words(nouns, suffixes, "noun + suffix")

    # Generate names by combining two keywords together and insert "AND" inbetween them

    print("Generating names with nouns + & + nouns...")
    all_names += combine_words(nouns, nouns, "noun + AND + noun", "And")

    print("Generating names with nouns + To + nouns...")
    all_names += combine_words(nouns, nouns, "noun + TO + noun", "To")

    with open(sys.argv[2], "w+") as out_file:
        json.dump(all_names, out_file, cls=NameEncoder, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sort_data(sys.argv[1])
