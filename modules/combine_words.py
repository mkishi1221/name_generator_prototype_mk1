#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from typing import List
from classes.algorithm import Algorithm
import itertools
from classes.name import Name


def combine_words(wordlist1: List[str], wordlist_1_type: str, wordlist2: List[str], wordlist2_type: str, algorithm: Algorithm) -> List[Name]:

    # Combine keywords from 2 keyword lists

    joint = algorithm.joint

    name_list = [joint.join(pair) for pair in itertools.product(wordlist1, wordlist2)]

    name_list: list[Name] = []
    for keyword_1 in wordlist1:
        for keyword_2 in wordlist2:
            name = joint.join((keyword_1, keyword_2))
            domain = name.lower() + ".com"
            all_keywords = "| " + keyword_1 + " | " + keyword_2 + " |"
            name_list.append(
                Name(repr(algorithm), len(name), name, domain, all_keywords, (keyword_1, wordlist_1_type), (keyword_2, wordlist2_type))
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
