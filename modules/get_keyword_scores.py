#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import orjson as json
from classes.keyword import Keyword
from typing import List

with open("dict/wikipedia_word_count/wikipedia-en-words-cumulative.json", "rb") as keyword_score_data_file:
    keyword_score_data = json.loads(keyword_score_data_file.read())

def get_keyword_scores(keywords_db: List[Keyword]) -> List[Keyword]:

    updated_keywords_db = []
    for keyword_data in keywords_db:
        if keyword_data.keyword in keyword_score_data.keys():
            keyword_data.keyword_score = keyword_score_data[keyword_data.keyword]['keyword_score']
        else:
            keyword_data.keyword_score = 0
        updated_keywords_db.append(keyword_data)
    
    return updated_keywords_db
