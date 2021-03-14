#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import regex as re
import sys
import json
from modules.generate_names import generate_names

def sort_data(wordlist_filepath):

    #Open file
    with open(wordlist_filepath) as wordlist_file:
        words = json.load(wordlist_file)

    print("Generating names...")
    # generate names
    names = generate_names(words)

    # save file
    with open(sys.argv[2], "w+") as out_file:
        out_file.write(names)

if __name__ == "__main__":
    sort_data(sys.argv[1])
