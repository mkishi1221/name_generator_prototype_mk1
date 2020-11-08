#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re
import sys


def generate_names(text):
    text = text.replace("’", "'")
    text = re.sub("we're","we are", text)
    text = re.sub("we've","we have", text)
    text = re.sub("doesn't","does not", text)
    text = re.sub("aren't","are not", text)
    text = re.sub("don't","do not", text)
    text = re.sub("'s","", text)
    text = re.sub(r'[\']',"", text)
    text = re.sub(r'[^A-Za-zä\-]'," ", text)  # TODO: What's that?
    text = re.sub('  +'," ", text)
    text = text.lower()

    word_list = set(text.split(" "))  # set is a data structure where each entry can only occur once
    
    sorted_word_list = sorted(word_list, key=len)

    return '\n'.join(sorted_word_list)

if __name__ == '__main__':
    print(generate_names(sys.stdin.read()))