#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import itertools

def combine_words(wordlist1, wordlist2, joint=""):

    name_list = [joint.join(pair) for pair in itertools.product(wordlist1, wordlist2)]

    temp_set = set()

    for combined_word in name_list:
        if len(combined_word) >= 8 and len(combined_word) <= 12:
            temp_set.add(combined_word)

    # wipe name_list and save a list representation of temp_set
    name_list = list(temp_set)
    name_list.sort(key=str.lower)
    sorted_by_len_name_list = sorted(name_list, key=len)

    return sorted_by_len_name_list