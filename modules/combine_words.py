#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import itertools
from classes.names import Names


def combine_words(wordlist1, wordlist2, algorithm, joint=""):

    # Combine keywords from 2 keyword lists

    name_list = [joint.join(pair) for pair in itertools.product(wordlist1, wordlist2)]

    name_list: list[Names] = []
    for keyword_1 in wordlist1:
        for keyword_2 in wordlist2:
            name = joint.join((keyword_1, keyword_2))
            domain = name.lower() + ".com"
            all_keywords = "| " + keyword_1 + " | " + keyword_2 + " |"
            name_list.append(
                Names(algorithm, len(name), name, domain, all_keywords, keyword_1, keyword_2)
            )

    # Filter out names that are more than 12 characters
    temp_set = {
        combined_word for combined_word in name_list if combined_word.length <= 12
    }

    # Sort name list by alphabetical order and length.
    name_list = list(temp_set)
    name_list.sort(
        key=lambda combined_name: getattr(combined_name, "name").lower(), reverse=False
    )
    sorted_by_len_name_list = sorted(
        name_list,
        key=lambda combined_name: getattr(combined_name, "length"),
        reverse=False,
    )

    return sorted_by_len_name_list
