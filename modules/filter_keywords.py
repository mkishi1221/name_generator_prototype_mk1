#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from typing import List
from classes.keyword import Keyword
from os import path
import regex as re
import json


def filter_keywords(keywords: List[Keyword]) -> List[Keyword]:
    """
    Filter approved keywords (approved keywords may be the following):
    - Either a noun, verb, or an adjective
    - Not contain any characters except alphabets
    - Word is at least 3 letters
    - To Do: filter out blacklisted words as well
    """
    approved_pos = ["noun", "verb", "adjective"]
    illegal_char = re.compile(r"[^a-zA-Z]")

    keyword_blacklist = []
    if path.exists('ref/keyword_blacklist.json'):
        with open('ref/keyword_blacklist.json', "rb") as keyword_blacklist_file:
            keyword_blacklist_json = json.loads(keyword_blacklist_file.read())
        for keyword in keyword_blacklist_json:
            keyword_blacklist.append(Keyword("", keyword['keyword_len'], keyword['keyword'], "", "", keyword['wordsAPI_pos'], "", 0))

    # Create set of approved keywords, filtering by pos, "illegal_chars" and length
    approved_keywords = {
        keyword
        for keyword in keywords
        if keyword.wordsAPI_pos in approved_pos
        and not bool(illegal_char.search(keyword.keyword))
        and keyword.keyword_len > 2
        and keyword not in keyword_blacklist
    }

    return list(approved_keywords)
