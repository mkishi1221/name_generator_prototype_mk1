#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import json
from datetime import datetime
from modules.find_unique_lines import find_unique_lines
from modules.extract_words_with_spacy import extract_words_with_spacy
from modules.import_keyword_list import import_keyword_list
from modules.get_wordAPI import verify_words_with_wordsAPI
from modules.filter_keywords import filter_keywords


def generate_word_list(text_file, user_keywords_file):

    all_keywords = []

    # Check if sentences exists
    sentences = open(text_file, "r").read()
    if sentences != "":

        # Filter out unique lines from source data containing sentences
        print("Finding unique lines...")
        unique_lines = find_unique_lines(sentences)

        # Run lines through Spacy to obtain keywords and categorize them according to their POS
        print("Extracting keywords from sentences using spacy...")
        spacy_keywords = extract_words_with_spacy(unique_lines)
        all_keywords += spacy_keywords
        with open("ref/keywords_from_sentences_.json", "w+") as out_file:
            json.dump(spacy_keywords, out_file, ensure_ascii=False, indent=1)
    else:
        spacy_keywords = []

    # Check if keywords exists
    user_keywords = open(user_keywords_file, "r").read().splitlines()
    if user_keywords != "":

        # Get keywords from user keyword list
        print("Extracting keywords from keyword list...")
        keyword_list_keywords = import_keyword_list(user_keywords)
        all_keywords += keyword_list_keywords
        with open("ref/keywords_from_keyword-list.json", "w+") as out_file:
            json.dump(keyword_list_keywords, out_file, ensure_ascii=False, indent=1)
    else:
        user_keywords = []

    # Quit if both files are empty
    if sentences == "" and user_keywords == "":
        print("No sentences and keywords detetcted! Please add source data to the \"data\" folder.")
        quit()

    # Run keywords through wordsAPI dictionary to verify and expand keyword dictionary
    print("Verifying keywords using wordAPI dictionary...")
    wordsAPI_keywords = verify_words_with_wordsAPI(all_keywords)

    # Run keywords through keywords filter
    print("Running keywords through keyword filter...")
    keywords = filter_keywords(wordsAPI_keywords)

    with open(sys.argv[3], "w+") as out_file:
        json.dump(keywords, out_file, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    generate_word_list(sys.argv[1], sys.argv[2])
