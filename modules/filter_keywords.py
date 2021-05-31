#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from classes.keyword import Keyword
import regex as re


def filter_keywords(keywords: "list[Keyword]") -> "set[Keyword]":
    """
    Filter approved keywords (approved keywords may be the following):
    - Either a noun, verb, or an adjective
    - Not contain any characters except alphabets
    - Word is at least 3 letters
    """
    approved_pos = ["noun", "verb", "adjective"]
    illegal_char = re.compile(r"[^a-zA-Z]")

    # Create set of approved keywords, filtering by pos and "illegal_chars"
    approved_keywords = {
        keyword
        for keyword in keywords
        if keyword.wordsAPI_pos in approved_pos
        and not bool(illegal_char.search(keyword.base))
    }

    return approved_keywords
