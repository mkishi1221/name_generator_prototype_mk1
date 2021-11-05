#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import os
from classes.algorithm import Algorithm
from classes.name import Name
from modules.combine_words import combine_words

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
            "origin": "sentences",
            "spacy_pos": "VERB",
            "wordsAPI_pos": "verb",
            "lemma": "design",
            "algorithm": "",
            "occurrence": 42,
            "keyword_user_score": 0,
            "keyword_wiki_score": 1,
            "keyword_total_score": 1
        },
        {
            "word": "design",
            "keyword_len": 6,
            "keyword": "design",
            "origin": "sentences",
            "spacy_pos": "VERB",
            "wordsAPI_pos": "verb",
            "lemma": "design",
            "algorithm": "",
            "occurrence": 42,
            "keyword_user_score": 0,
            "keyword_wiki_score": 1,
            "keyword_total_score": 1
        }
    ]

    wordlist_2_type = "verb"

    algorithm = Algorithm(
        "noun",
        "verb",
        ""
    )

    result = [Name(
        'noun + verb',
        14,
        'IdentityDesign',
        'identitydesign.com',
        '| Identity | Design |',
        (
            'Identity',
            'noun',
            'user: 3',
            'wiki: 1',
            'keyword_list'
        ),
        (
            'Design',
            'verb',
            'user: 0',
            'wiki: 1',
            'sentences'
        ),
        4,
        1,
        0,
        5
    )]

    assert str(combine_words(wordlist1, wordlist_1_type, wordlist2, wordlist_2_type, algorithm)) == str(result), "Results differ from expectations"

if __name__ == "__main__":
    test_combine_words()
    print("Combine words operating as expected")
