#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re
import sys


def generate_names(text):

    name_list = []
    word_list = text.split("\n")

    for first_word in word_list:
        for second_word in word_list:
            name = first_word + second_word
            if len(name) > 10:
                name_list.append(name)

    name_list.sort(key=str.lower)
    sorted_by_len_name_list = sorted(name_list, key=len)

    return '\n'.join(sorted_by_len_name_list)


if __name__ == '__main__':
    print(generate_names(sys.stdin.read()))

    # if len(name) > 4 and name not in name_list:
