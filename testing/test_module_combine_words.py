#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import os
from classes.algorithm import Algorithm
from classes.name import Name
from modules.combine_words import combine_words

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

def test_combine_words():

    wordlist1 = [
        {
            "word": "identity",
            "keyword_len": 8,
            "keyword": "identity",
            "origin": "keyword_list",
            "spacy_pos": "",
            "wordsAPI_pos": "noun",
            "lemma": "",
            "algorithm": "",
            "occurrence": 0,
            "keyword_user_score": 3,
            "keyword_wiki_score": 1,
            "keyword_total_score": 4
        },
        {
            "word": "identity",
            "keyword_len": 8,
            "keyword": "identity",
            "origin": "keyword_list",
            "spacy_pos": "",
            "wordsAPI_pos": "noun",
            "lemma": "",
            "algorithm": "",
            "occurrence": 0,
            "keyword_user_score": 3,
            "keyword_wiki_score": 1,
            "keyword_total_score": 4
        }
    ]

    wordlist_1_type = "noun"

    wordlist2 = [
        {
            "word": "design",
            "keyword_len": 6,
            "keyword": "design",
            "origin": "keyword_list",
            "spacy_pos": "",
            "wordsAPI_pos": "verb",
            "lemma": "",
            "algorithm": "",
            "occurrence": 0,
            "keyword_user_score": 3,
            "keyword_wiki_score": 1,
            "keyword_total_score": 4
        },
        {
            "word": "design",
            "keyword_len": 6,
            "keyword": "design",
            "origin": "keyword_list",
            "spacy_pos": "",
            "wordsAPI_pos": "verb",
            "lemma": "",
            "algorithm": "",
            "occurrence": 0,
            "keyword_user_score": 3,
            "keyword_wiki_score": 1,
            "keyword_total_score": 4
        }
    ]

    wordlist_2_type = "verb"

    algorithm = Algorithm(
        "noun",
        "verb",
        ""
    )

    result = Name(
        "noun + verb",
        14,
        "IdentityDesign",
        "identitydesign.com",
        "| Identity | Design |",
        [
            "Identity",
            "noun",
            "user: 3",
            "wiki: 1",
            "keyword_list"
        ],
        [
            "Design",
            "verb",
            "user: 0",
            "wiki: 1",
            "sentences"
        ],
        4,
        1,
        0,
        5
    )

    assert combine_words(wordlist1, wordlist_1_type, wordlist2, wordlist_2_type, algorithm) == [result]
