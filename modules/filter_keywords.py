#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from typing import List
from classes.keyword import Keyword
from os import path
import regex as re
import json
from classes.user_repository.mutations.user_preferences import UserPreferenceMutations
from classes.user_repository.repository import UserRepository


def filter_keywords(keywords: List[Keyword]) -> List[Keyword]:
    """
    Filter approved keywords (approved keywords may be the following):
    - Either a noun, verb, or an adjective
    - Not contain any characters except alphabets
    - Word is at least 3 letters
    - Word is not a blacklisted word
    """
    approved_pos = ["noun", "verb", "adjective"]
    illegal_char = re.compile(r"[^a-zA-Z]")

    UserRepository.init_user()
    keyword_blacklist = UserPreferenceMutations.get_blacklisted()

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
