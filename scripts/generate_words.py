#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re
import sys
import spacy
import json

nlp = spacy.load('en_core_web_lg')


def find_unique_lines(text):
    text = text.translate(str.maketrans(
        {chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
    text = re.sub(r'^\W+$', "", text)

    lines = text.split('\n')
    lines.remove("")
    lines.remove(" ")

    # set is faster than checking if line is already in
    unique_lines = set(lines)
    unique_lines_with_occurences_n_len = []

    for unique_line in unique_lines:
        unique_lines_with_occurences_n_len.append({
            "line": unique_line,
            "occurence": lines.count(unique_line), # count returns occurences of list items
            "len": len(unique_line)  # no need to assign unnecessary vars
        })

    sorted_unique_lines = sorted(unique_lines_with_occurences_n_len,
                                 key=lambda k: (-k['len'], -k['occurence'], k['line'].lower()))

    words = []
    for line in map(lambda line: line["line"], sorted_unique_lines):

        doc = nlp(line)

        for sent in doc.sents:

            sent_len = len(sent)
            count = 1
            prev_len_plus_idx = 0
            ttext = ""
            word = ""
            word_pos = ""
            word_tag = ""
            word_lemma = ""

            for token in sent:

                word_len_plus_idx = len(token.text) + token.idx
                space_num = token.idx - prev_len_plus_idx
                prev_len_plus_idx = word_len_plus_idx

                if count == 1:
                    ttext = '▶' + token.text
                elif count == sent_len:
                    ttext = token.text + '◀'
                else:
                    ttext = token.text

                if space_num == 0:
                    word = word + ttext
                    word_lemma = word_lemma + token.lemma_
                    if word_pos == "":
                        word_pos = token.pos_
                        word_tag = token.tag_
                        word_dep = token.dep_
                    else:
                        word_pos = word_pos + '∘' + token.pos_
                        word_tag = word_tag + '∘' + token.tag_
                        word_dep = word_dep + '∘' + token.dep_
                else:
                    base_word = re.sub(r'^\W+', "", word)
                    base_word = re.sub(r'\W+$', "", base_word)
                    base_word = base_word.lower()
                    base_word_len = len(base_word)
                    token_dict = {"base_len": base_word_len, "base": base_word, "word": word,
                                  "pos": word_pos, "tag": word_tag, "dep": word_dep, "lemma": word_lemma}
                    words.append(token_dict)
                    word = ttext
                    word_pos = token.pos_
                    word_tag = token.tag_
                    word_dep = token.dep_
                    word_lemma = token.lemma_

                count += 1

            base_word = re.sub(r'^\W+', "", word)
            base_word = re.sub(r'\W+$', "", base_word)
            base_word = base_word.lower()
            base_word_len = len(base_word)
            token_dict = {"base_len": base_word_len, "base": base_word, "word": word,
                          "pos": word_pos, "tag": word_tag, "dep": word_dep, "lemma": word_lemma}
            words.append(token_dict)

    unique_words = []
    for word in words:  # unfortunatley sets of dictionaries don't exist :(
        if word not in unique_words:
            unique_words.append(word)

    for unique_word in unique_words:
        unique_word['occurence'] = words.count(unique_word)

    sorted_unique_words = sorted(unique_words, key=lambda k: (
        k['base'], -k['occurence'], k['word'].lower()))

    with open("tmp/words.json", "w") as out_file:
        json.dump(sorted_unique_words, out_file, ensure_ascii=False)


if __name__ == '__main__':
    # print(find_unique_lines(sys.stdin.read()))
    find_unique_lines(sys.stdin.read())
