#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re
import spacy
import json

nlp = spacy.load("en_core_web_lg")


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

                words.append(create_base_word(word, word_pos, word_lemma))

    # Create set of unique words - @Korbi cause word is a dict and dicts are unhashable a comprehension won't work here!
    unique_words = []
    for word in words:
        if word.get("word") != "" and word not in unique_words:
            unique_words.append(word)

    # Count occurence of unique word
    for unique_word in unique_words:
        unique_word["occurence"] = words.count(unique_word)

    # Sort keyword list according to it's "base" word in alphabetical order, its occurence and the original word in alphabetical order.
    sorted_unique_words = sorted(
        unique_words, key=lambda k: (k["base"], -k["occurence"], k["word"].lower())
    )

    # filter single letter words beforehand
    sorted_unique_words = [
        word for word in sorted_unique_words if word.get("base_len") > 1
    ]

    with open("ref/tmp_words_spacy.json", "w+") as out_file:
        json.dump(sorted_unique_words, out_file, ensure_ascii=False, indent=1)

    """
    Filter approved keywords (approved keywords may be the following):
    - Either a noun, verb, or an adjective
    - Contain more than 1 letter
    - Not contain any numbers
    - Must not be a duplicate even with a different pos (Right now POS are not used to create names - this will change in the future!)
    """

    # Filter words that are only nouns, verbs or adjectives
    # Remove words that only contain alphabet letters
    # Make sure keyword list only contains unqiue values
    approved_pos = ["NOUN", "VERB", "ADJ"]
    illegal_char = re.compile(r"[^a-zA-Z]")
    keywords = []
    base_list = []
    for word in sorted_unique_words:
        if (
            word.get("pos") in approved_pos
            and not bool(illegal_char.search(word.get("base")))
            and word.get("base") not in base_list
        ):
            keywords.append(word)
            base_list.append(word.get("base"))

    return keywords
