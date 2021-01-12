#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import regex as re
import sys
import json
from modules.find_uniq_lines import find_uniq_lines
from modules.extract_words_with_spacy import extract_words_with_spacy
from modules.generate_names import generate_names

def sort_data(text_file):

    #Open file
    data = open(text_file, "r").read()

    print("Finding unique lines...")
    #Find unique lines (modules/find_uniq_lines.py)
    uniq_lines = find_uniq_lines(data)

    print("Extracting words using spacy...")
    #Extract words using spacy
    words = extract_words_with_spacy(uniq_lines)

    print("Generating names...")
    #Generate names
    names = generate_names(words)

    #Save file
    with open(sys.argv[2], "w+") as out_file:
        out_file.write(names)
        out_file.closed

if __name__ == "__main__":
    sort_data(sys.argv[1])