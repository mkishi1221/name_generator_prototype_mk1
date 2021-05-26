#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import json
from modules.find_unique_lines import find_unique_lines
from modules.extract_words_with_spacy import extract_words_with_spacy
from modules.get_wordAPI import verify_words_with_wordsAPI
from modules.filter_keywords import filter_keywords

def generate_word_list(text_file):

    data = open(text_file, "r").read()

    # Filter out unique lines from source data
    print("Finding unique lines...")
    unique_lines = find_unique_lines(data)

    # Run lines through Spacy to obtain keywords and categorize them according to their POS
    print("Extracting keywords using spacy...")
    spacy_keywords = extract_words_with_spacy(unique_lines)

    with open("ref/tmp_keywords_spacy.json", "w+") as out_file:
        json.dump(spacy_keywords, out_file, ensure_ascii=False, indent=1)

    # Run keywords through wordsAPI dictionary to verify and expand keyword dictionary
    print("Verifying keywords using wordAPI dictionary...")
    wordsAPI_keywords = verify_words_with_wordsAPI(spacy_keywords)

    # Run keywords through keywords filter
    print("Running keywords through keyword filter...")
    keywords = filter_keywords(wordsAPI_keywords)

    with open(sys.argv[2], "w+") as out_file:
        json.dump(keywords, out_file, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    generate_word_list(sys.argv[1])
