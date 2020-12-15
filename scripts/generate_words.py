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
        word_pos: str?; fill out
        word_tag: str; fill out
        word_dep: str; fill out
        word_lemma: str; fill out
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
    }


def find_unique_lines(text):

    # Replace only-white space lines with nothing
    text = re.sub(r"^\W+$", "", text)

    lines = text.split("\n")
    lines.remove("")
    lines.remove(" ")

    # Filter unique lines
    # Set is faster than checking if line is already in
    unique_lines = set(lines)
    unique_lines_with_occurences_n_len = []

    # Add info for each unique line in dict format
    for unique_line in unique_lines:
        unique_lines_with_occurences_n_len.append(
            {
                "line": unique_line,
                "occurence": lines.count(
                    unique_line
                ),  # count returns occurences of list items
                "len": len(unique_line),  # no need to assign unnecessary vars
            }
        )

    # Sort lines by length, occurence and alphabetical oder
    sorted_unique_lines = sorted(
        unique_lines_with_occurences_n_len,
        key=lambda k: (-k["len"], -k["occurence"], k["line"].lower()),
    )

    words = []
    for line in map(lambda line: line["line"], sorted_unique_lines):

        # Process "line" with spacy.
        doc = nlp(line)

        # Spacy divides "line" into sentences ("sent").
        for sent in doc.sents:

            sent_len = len(sent)
            count = 1
            prev_len_plus_idx = 0
            ttext = ""
            word = ""
            word_pos = ""
            word_tag = ""
            word_lemma = ""

            # Spacy divides sentences ("sent") into words ("tokens"). (Tokens can also be symbols and other things that are not full words. )
            for token in sent:

                # Next, we need to determine if there is a space between the "tokens". This ensure that tokens not separated by spaces such as "Masayuki" "'" and "s" combine together to make "Masayuki's"
                # "token.idx" returns the nth position of the first character of word within the sentence.
                # Add the length of the word to get the position of the last character of word.
                word_len_plus_idx = len(token.text) + token.idx

                # Substract the previous word's last character position by the current word's first character position.
                # If it equals 1, then there is a space. If it equals 0, there is no space.
                space_num = token.idx - prev_len_plus_idx

                # Save current word's last character position so that the next token can use it.
                prev_len_plus_idx = word_len_plus_idx

                # If word count if 1, then add '▶' symbol at beginning to indicate word at start of sentence.
                # If word count equals length of sentence, then add '◀' to end to indicate word at end of sentence.
                # Words at beginning of sentences could have more value so I'd like to collect them for analysis.
                if count == 1:
                    ttext = "▶" + token.text
                elif count == sent_len:
                    ttext = token.text + "◀"
                else:
                    ttext = token.text

                # Combine tokens together if they are not divided by space.
                if space_num == 0:
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

                count += 1

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

    with open("tmp/words.json", "w+") as out_file:
        json.dump(sorted_unique_words, out_file, ensure_ascii=False)


if __name__ == "__main__":
    find_unique_lines(sys.stdin.read())
