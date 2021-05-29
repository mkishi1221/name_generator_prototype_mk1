#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import regex as re

def create_base_word(word) -> dict:
    """
    summary:
        Creates a "base-word" so that similar words are grouped together regardless of their case-styles/symbols used.
        Removes non-alphabet characters from beginning and end of word and saves it as lowercase "base_word".
        (eg. "+High-tech!" → "high-tech" )
    """
    base_word = re.sub(r"^\W+", "", word)
    base_word = re.sub(r"\W+$", "", base_word)
    return {
        "base_len": len(base_word),
        "base": base_word.lower(),
        "word": word,
        "origin": "keyword_list"
    }


def import_keyword_list(words):

    # Create set of unique words
    tmp_words = []
    unique_words = []
    
    for word in words:
        if word not in tmp_words:
            unique_words.append(create_base_word(word))
            tmp_words.append(word)

    # Sort keyword list according to:
    # - "base" word in alphabetical order
    # - "original" word in alphabetical order.
    sorted_unique_words = sorted(
        unique_words, key=lambda k: (k["base"], k["word"].lower())
    )

    # filter single letter words beforehand
    sorted_unique_words = [
        word for word in sorted_unique_words if word.get("base_len") > 1
    ]

    return sorted_unique_words
