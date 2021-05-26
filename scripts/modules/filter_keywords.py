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
        if (
            keyword.get("wordsAPI_pos") in approved_pos
            and keyword.get("base_len") > 2
            and not bool(illegal_char.search(keyword.get("base")))
        ):
            approved_keywords.append(keyword)

    return approved_keywords
