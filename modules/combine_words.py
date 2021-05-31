#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import itertools

def combine_words(wordlist1, wordlist2, joint=""):

    # Combine keywords from 2 keyword lists
    name_list = [joint.join(pair) for pair in itertools.product(wordlist1, wordlist2)]

    # Create a name list with unique values
    # Filter out names that are more than 12 characters
    temp_set = {combined_word for combined_word in name_list if len(combined_word) <= 12}

    # Sort name list by alphabetical order and length.
    name_list = list(temp_set)
    name_list.sort(key=str.lower)
    sorted_by_len_name_list = sorted(name_list, key=len)

    return sorted_by_len_name_list