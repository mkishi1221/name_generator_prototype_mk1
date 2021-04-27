#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re
import sys
import spacy
import json

nlp = spacy.load('en_core_web_lg')

def create_base_word(word, word_pos, word_lemma) -> dict:
    """
    summary:
        Creates a "base-word" so that slightly different words can be grouped together regardless of their case-styles and symbols used.
        Removes non-alphabet characters from beginning and end of word and saves it as lowercase "base_word". (eg. "+High-tech!" → "high-tech" )
    parameters:
        word: str; word to create base_word from
        word_pos: str; Coarse-grained part-of-speech from the Universal POS tag set. (eg. noun, verb etc.)
        word_tag: str; Fine-grained part-of-speech. (eg. NN = singular noun, NNS = plural noun etc.)
        word_dep: str; Syntactic dependency relation. (What relations the word has to other words in the sentence.)
        word_lemma: str; Base form of the token, with no inflectional suffixes. (eg. word = changing, lemma = change)
    returns:
        token_dict: dict; a dictionary containing all important parameters of base_word
    """
    base_word = re.sub(r"^\W+", "", word)
    base_word = re.sub(r"\W+$", "", base_word)
    return {
        "base_len": len(base_word),
        "base": base_word.lower(),
        "word": word,
        "pos": word_pos,
        "lemma": word_lemma,
    }

def extract_words_with_spacy(lines):
    words = []
    for line in map(lambda line: line["line"], lines):
        doc = nlp(line)

        # Spacy divides sentences ("sent") into words ("tokens"). (Tokens can also be symbols and other things that are not full words. )
        for sent in doc.sents:
            for token in sent:
                word = token.text
                word_pos = token.pos_
                word_lemma = token.lemma_

                words.append(
                    create_base_word(word, word_pos, word_lemma)
                )

    # Create set of unique words
    unique_words = []
    for word in words:
        if word.get("word") != "" and word not in unique_words:
            unique_words.append(word)

    for unique_word in unique_words:
        unique_word["occurence"] = words.count(unique_word)

    sorted_unique_words = sorted(
        unique_words, key=lambda k: (k["base"], -k["occurence"], k["word"].lower())
    )

    with open("ref/tmp_words_spacy.json", "w+") as out_file:
        json.dump(sorted_unique_words, out_file, ensure_ascii=False, indent=1)

    #Filter undesirable keywords

    approved_pos = ["NOUN", "VERB", "ADJ"]

    keywords = []
    base_list = []
    for word in sorted_unique_words:
        if word.get("base_len") > 1 and any(str.isdigit(c) for c in word.get("base")) == False and word.get("pos") in approved_pos and word.get("base") not in base_list:
            keywords.append(word)
            base_list.append(word.get("base"))

    return keywords