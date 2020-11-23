#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re
import sys
import json
import itertools


def generate_names():
    
    # it's faster to read onetime from a json file than deserializing every entry
    data = json.load(open("tmp/words.json"))  # be cautious file path depends on cwd of create_names
    
    word_list = set()  # set ensures word occures only once
    for analyzed_word in data:
        # this combines the old check if empty -> replace empty base -> add if not already in list; 
        # also it's more likely that base will be small than ten chars as it is not a char at all -> thus it's the first condition
        if len(analyzed_word["base"]) >= 10 and re.match(r"[a-zA-Z]+", analyzed_word["base"]):
            word_list.add(analyzed_word["base"])

    # list comprehensions are way faster than normal iterations; also itertools comes in handy for cartesian productions
    name_list = ["".join(pair) for pair in itertools.product(word_list, word_list)]

    name_list.sort(key=str.lower)
    sorted_by_len_name_list = sorted(name_list, key=len)

    return '\n'.join(sorted_by_len_name_list)


if __name__ == '__main__':
    print(generate_names())