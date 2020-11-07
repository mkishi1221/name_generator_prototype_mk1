#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re
import sys

word_list = []
name_list = []

def generate_names(text):

    word_list = (text.split("\n"))

    for word in word_list:
            if word:
                first=word

                for word in word_list:
                    if word: 
                        second=word
                        name=first + second

                        if len(name) > 10:
                            name_list.append(name)

    name_list.sort(key=str.lower)
    sorted_name_list = sorted(name_list, key=len)

    names = '\n'.join(map(str, sorted_name_list))

    return names

if __name__ == '__main__':
    print(generate_names(sys.stdin.read()))


    # if len(name) > 4 and name not in name_list: