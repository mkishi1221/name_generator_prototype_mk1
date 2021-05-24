#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import json
from modules.find_unique_lines import find_unique_lines
from modules.extract_words_with_spacy import extract_words_with_spacy


def generate_word_list(text_file):

    data = open(text_file, "r").read()

    # Filter out unique lines from source data
    print("Finding unique lines...")
    unique_lines = find_unique_lines(data)

    # Run lines through Spacy to obtain keywords and categorize them according to their POS
    print("Extracting words using spacy...")
    words = extract_words_with_spacy(unique_lines)

    with open(sys.argv[2], "w+") as out_file:
        json.dump(words, out_file, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    generate_word_list(sys.argv[1])
