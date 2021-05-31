#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re
import sys
import spacy
import json

# Load spacy model
nlp = spacy.load("en_core_web_lg")

def create_base_word(word, word_pos, word_tag, word_dep, word_lemma) -> dict:
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
        "tag": word_tag,
        "dep": word_dep,
        "lemma": word_lemma,
        "preference": ""
    }


def extract_words_with_spacy(lines):

    words = []
    for line in map(lambda line: line["line"], lines):

        # Process "line" with spacy.
        doc = nlp(line)

        # Spacy divides "line" into sentences ("sent").
        for sent in doc.sents:

            sent_len = len(sent)
            line_len = 0
            ttext = ""
            word = ""
            word_pos = ""
            word_tag = ""
            word_lemma = ""

            # Spacy divides sentences ("sent") into words ("tokens"). (Tokens can also be symbols and other things that are not full words. )
            for token in sent:

                # If word count if 1, then add '▶' symbol at beginning to indicate word at start of sentence.
                # If word count equals length of sentence, then add '◀' to end to indicate word at end of sentence.
                # Words at beginning of sentences could have more value so I'd like to collect them for analysis.
                if token.idx == 0:
                    ttext = "▶" + token.text
                elif line_len + len(token.text) == sent_len:
                    ttext = token.text + "◀"
                else:
                    ttext = token.text

                # Combine tokens together if they are not divided by space.
                if line_len + 1 == token.idx or token.idx == 0:
                    word = word + ttext
                    word_lemma = word_lemma + token.lemma_
                    if word_pos == "":
                        # If this is the first token, save the POS data for the next token.
                        word_pos = token.pos_
                        word_tag = token.tag_
                        word_dep = token.dep_
                    else:
                        # If there are previous POS data, append new POS data divided by '∘' symbol. (eg. food! = noun∘sym)
                        word_pos = word_pos + "∘" + token.pos_
                        word_tag = word_tag + "∘" + token.tag_
                        word_dep = word_dep + "∘" + token.dep_
                else:
                    words.append(
                        create_base_word(word, word_pos, word_tag, word_dep, word_lemma)
                    )

                    # Last word gets added to the dictionary outside of this loop.
                    word = ttext
                    word_pos = token.pos_
                    word_tag = token.tag_
                    word_dep = token.dep_
                    word_lemma = token.lemma_

                line_len += len(token.text)

            words.append(
                create_base_word(word, word_pos, word_tag, word_dep, word_lemma)
            )

    # Create set of unique words
    unique_words = []
    for word in words:  # unfortunatley sets of dictionaries don't exist :(
        if word.get("word") != "" and word not in unique_words:
            unique_words.append(word)

    for unique_word in unique_words:
        unique_word["occurence"] = words.count(unique_word)

    sorted_unique_words = sorted(
        unique_words, key=lambda k: (k["base"], -k["occurence"], k["word"].lower())
    )

    with open("ref/tmp_words_spacy.json", "w+") as out_file:
        json.dump(sorted_unique_words, out_file, ensure_ascii=False, indent=1)


    return sorted_unique_words
