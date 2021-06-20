#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from classes.keyword import Keyword
import regex as re


def create_keyword(word: str) -> Keyword:
    """
    summary:
        Creates a "keyword" so that similar words are grouped together regardless of their case-styles/symbols used.
        Removes non-alphabet characters from beginning and end of word and saves it as lowercase "keyword".
        (eg. "+High-tech!" → "high-tech" )
    """
    keyword = re.sub(r"^\W+", "", word)
    keyword = re.sub(r"\W+$", "", keyword)
    return Keyword(word, len(keyword), keyword.lower(), "keyword_list")


def import_keyword_list(words) -> "list[Keyword]":

    # Create set of unique words
    unique_words = {create_keyword(word) for word in words}

    # Sort keyword list according to:
    # - "keyword" in alphabetical order
    # - "original" word in alphabetical order.
    sorted_unique_words = sorted(unique_words, key=lambda k: (k.keyword, k.word.lower()))

    # filter single letter words beforehand
    sorted_unique_words = [word for word in sorted_unique_words if word.keyword_len >= 1]

    return sorted_unique_words
