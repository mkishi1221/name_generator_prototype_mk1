#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re
import sys
import json
import itertools


def generate_names(data):
    
    pattern = re.compile(r"[^a-zA-Z]")  # compile before loop for speed
    temp_set = set(filter(None, [pattern.sub(r"", word["base"]) for word in data]))

    # list comprehensions are way faster than normal iterations; also itertools comes in handy for cartesian productions
    name_list = ["".join(pair) for pair in itertools.product(temp_set, temp_set)]

    # wipe temp_set memory
    temp_set = set()

    for combined_word in name_list:
        # this combines the old check if empty -> replace empty base -> add if not already in list; 
        # also it's more likely that base will be small than ten chars as it is not a char at all -> thus it's the first condition
        if len(combined_word) >= 10:
            temp_set.add(combined_word)

    # wipe name_list and save a list representation of temp_set
    name_list = list(temp_set)
    name_list.sort(key=str.lower)
    sorted_by_len_name_list = sorted(name_list, key=len)

    with open("ref/tmp_names.tsv", "w+") as out_file:
        out_file.write('\n'.join(sorted_by_len_name_list))
        out_file.closed

    return '\n'.join(sorted_by_len_name_list)