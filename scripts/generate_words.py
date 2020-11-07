#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re
import sys

word_list = []

def generate_names(text):
    text = text.replace("’", "'")
    text = re.sub("we're","we are", text)
    text = re.sub("we've","we have", text)
    text = re.sub("doesn't","does not", text)
    text = re.sub("aren't","are not", text)
    text = re.sub("don't","do not", text)
    text = re.sub("'s","", text)
    text = re.sub('[\']',"", text)
    text = re.sub('[^A-Za-zä\-]'," ", text)
    text = re.sub('  +'," ", text)
    text = text.lower()

    allwords = (text.split(" "))

    for word in allwords:
        if word not in word_list:
            word_list.append(word)
    
    sorted_word_list = sorted(word_list, key=len)

    words = '\n'.join(map(str, sorted_word_list))

    return words

if __name__ == '__main__':
    print(generate_names(sys.stdin.read()))