#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
from modules.combine_words import combine_words

# This is a basic name generator that only combines 2 keywords together. 
# This script may become redundant in the future after single keywords are categorized into different parts of speech using wordsAPI.
def sort_data(wordlist_filepath):

    with open(wordlist_filepath) as wordlist_file:
        raw_data = wordlist_file.read()
        words = raw_data.split("\n")

    all_names = []

    print("Generating names...")
    all_names += combine_words(words, words)

    names = "\n".join(all_names)

    with open(sys.argv[2], "w+") as out_file:
        out_file.write(names)


if __name__ == "__main__":
    sort_data(sys.argv[1])
