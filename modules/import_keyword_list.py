#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from classes.keyword import Keyword
import regex as re


def create_keyword(word: str) -> Keyword:
    """
    summary:
        Creates a "base-word" so that similar words are grouped together regardless of their case-styles/symbols used.
        Removes non-alphabet characters from beginning and end of word and saves it as lowercase "base_word".
        (eg. "+High-tech!" → "high-tech" )
    """
    base_word = re.sub(r"^\W+", "", word)
    base_word = re.sub(r"\W+$", "", base_word)
    return Keyword(word, len(base_word), base_word.lower(), "keyword_list")


def import_keyword_list(words) -> "list[Keyword]":

    # Create set of unique words
    unique_words = {create_keyword(word) for word in words}

    # Sort keyword list according to:
    # - "base" word in alphabetical order
    # - "original" word in alphabetical order.
    sorted_unique_words = sorted(unique_words, key=lambda k: (k.base, k.word.lower()))

    # filter single letter words beforehand
    sorted_unique_words = [word for word in sorted_unique_words if word.base_len >= 1]

    return sorted_unique_words
