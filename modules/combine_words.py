#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from typing import List
from classes.algorithm import Algorithm
from classes.name import Name


def combine_words(wordlist1: List[dict], wordlist_1_type: str, wordlist2: List[dict], wordlist_2_type: str, algorithm: Algorithm) -> List[Name]:

    # Combine keywords from 2 keyword lists
    joint = algorithm.joint
    name_list: list[Name] = []
    for keyword_1_dict in wordlist1:
        if wordlist_1_type == 'prefix':
            keyword_1 = keyword_1_dict['prefix']
            keyword_1_score = 3
        else:
            keyword_1 = keyword_1_dict['keyword'].title()
            keyword_1_score = keyword_1_dict['keyword_score']
        for keyword_2_dict in wordlist2:
            if wordlist_2_type == 'suffix':
                keyword_2 = keyword_2_dict['suffix']
                keyword_2_score = 3
            else:
                keyword_2 = keyword_2_dict['keyword'].title()
                keyword_2_score = keyword_2_dict['keyword_score']
            name = joint.join((keyword_1, keyword_2))
            domain = name.lower() + ".com"
            all_keywords = "| " + keyword_1 + " | " + keyword_2 + " |"
            name_score = int(keyword_1_score) + int(keyword_2_score)
            name_list.append(
                Name(
                    repr(algorithm),
                    len(name),
                    name,
                    domain,
                    all_keywords,
                    (keyword_1, wordlist_1_type, keyword_1_score),
                    (keyword_2, wordlist_2_type, keyword_2_score),
                    name_score
                )
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
