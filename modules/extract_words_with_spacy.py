#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from classes.keyword import Keyword
import regex as re
import spacy


nlp = spacy.load("en_core_web_lg")


def create_keyword(word, word_pos, word_lemma) -> Keyword:
    """
    summary:
        Creates a "base-word" so that similar words are grouped together regardless of their case-styles/symbols used.
        Removes non-alphabet characters from beginning and end of word and saves it as lowercase "base_word".
        (eg. "+High-tech!" → "high-tech" )
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
    return Keyword(
        word,
        len(base_word),
        base_word.lower(),
        "sentences",
        spacy_pos=word_pos,
        lemma=word_lemma,
    )


def extract_words_with_spacy(lines) -> "list[Keyword]":
    keywords: list[Keyword] = []
    for line in map(lambda line: line["line"], lines):
        doc = nlp(line)

        # Spacy divides sentences ("sent") into words ("tokens").
        # Tokens can also be symbols and other things that are not full words.
        for sent in doc.sents:
            for token in sent:
                word = token.text
                word_pos = token.pos_
                word_lemma = token.lemma_

                keywords.append(create_keyword(word, word_pos, word_lemma))

    unique_words = {word for word in keywords if word.word != "" and word.base_len >= 1}

    # Count occurence of unique word
    for unique_word in unique_words:
        unique_word.occurence = keywords.count(unique_word)

    # Sort keyword list according to:
    # - "base" word in alphabetical order
    # - Occurence
    # - "original" word in alphabetical order.
    sorted_unique_words = sorted(
        unique_words, key=lambda k: (k.base, -k.occurence, k.word.lower())
    )

    return sorted_unique_words
