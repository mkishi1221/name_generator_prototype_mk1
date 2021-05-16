#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re
import sys
import json
import itertools
import random


def combine_words(wordlist1, wordlist2):

    name_list = ["".join(pair) for pair in itertools.product(wordlist1, wordlist2)]

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

    sorted_by_len_name_list = []

    random.shuffle(name_list)
    # sorted_by_len_random_list = sorted(name_list, key=len)

    return name_list