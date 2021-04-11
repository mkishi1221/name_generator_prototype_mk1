#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re
import sys
import json
import itertools
import random


def generate_names(data):
    
    pattern = re.compile(r"[^a-zA-Z]")  # compile before loop for speed
    temp_set = set(filter(None, [pattern.sub(r"", word["base"]) for word in data]))

    name_list = ["".join(pair) for pair in itertools.product(temp_set, temp_set)]

    temp_set = set()

    for combined_word in name_list:
        if len(combined_word) >= 8 and len(combined_word) <= 12:
            temp_set.add(combined_word)

    # wipe name_list and save a list representation of temp_set
    name_list = list(temp_set)
    name_list.sort(key=str.lower)
    sorted_by_len_name_list = sorted(name_list, key=len)

    with open("ref/tmp_names.tsv", "w+") as out_file:
        out_file.write('\n'.join(sorted_by_len_name_list))
        out_file.closed

    sorted_by_len_name_list = []

    random.shuffle(name_list)
    # sorted_by_len_random_list = sorted(name_list, key=len)

    return '\n'.join(name_list)