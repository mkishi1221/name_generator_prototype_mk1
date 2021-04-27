#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import regex as re
import sys
import json
from modules.create_names import create_names

def sort_data(wordlist_filepath):

    with open(wordlist_filepath) as wordlist_file:
        words = json.load(wordlist_file)

    print("Generating names...")
    names = create_names(words)

    with open(sys.argv[2], "w+") as out_file:
        out_file.write(names)

if __name__ == "__main__":
    sort_data(sys.argv[1])
