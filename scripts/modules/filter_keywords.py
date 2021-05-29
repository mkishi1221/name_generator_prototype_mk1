#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re


def filter_keywords(keywords):
    """
    Filter approved keywords (approved keywords may be the following):
    - Either a noun, verb, or an adjective
    - Not contain any characters except alphabets
    - Word is at least 3 letters
    """
    approved_pos = ["noun", "verb", "adjective"]
    illegal_char = re.compile(r"[^a-zA-Z]")
    approved_keywords = []

    for keyword in keywords:

        # Remove unused keyword dict keys
        tmp_keyword = keyword.copy()
        tmp_keyword.pop("word")
        tmp_keyword.pop("lemma", None)
        tmp_keyword.pop("spacy_pos", None)
        tmp_keyword.pop("occurence", None)

        # Filter approved keywords
        if (
            tmp_keyword.get("wordsAPI_pos") in approved_pos
            and tmp_keyword.get("base_len") > 2
            and not bool(illegal_char.search(tmp_keyword.get("base")))
            and not any(
                tmp_keyword["base"] == d["base"]
                and tmp_keyword["wordsAPI_pos"] == d["wordsAPI_pos"]
                for d in approved_keywords
            )
        ):
            approved_keywords.append(tmp_keyword)

    return approved_keywords
