#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import regex as re
import sys
import spacy
import json

nlp = spacy.load('en_core_web_lg')

def find_uniq_lines(text):
    text = text.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
    text = re.sub(r'^\W+$',"", text)
    
    lines_list = text.split('\n')
    
    lines =[]
    for line in lines_list:
        if line != "":
            line.strip()
            line_dict = {"line" : line}
            lines.append(line_dict)
        
    uniq_lines = []
    for line in lines:
        if line != uniq_lines:
            uniq_lines.append(line)
    
    for uniq_line in uniq_lines:
        count = 0
        line_len = len(uniq_line.get("line"))
        for line in lines:
            if uniq_line == line:
                count += 1
        uniq_line['occurence'] = count
        uniq_line['len'] = line_len
    
    sorted_uniq_lines = sorted(uniq_lines, key=lambda k: (-k['len'], -k['occurence'], k['line'].lower()))

    line_list = []
    for item in sorted_uniq_lines:
        if item != "":
            line_list.append(item.get("line"))
    
    words = []
    for line in line_list:
        
        all_sentences = []
        all_tokens = []
        
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
            
                word_len = len(token.text)
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
                    base_word = re.sub(r'^\W+',"", word)
                    base_word = re.sub(r'\W+$',"", base_word)
                    base_word = base_word.lower()
                    base_word_len = len(base_word)
                    token_dict = {"base_len" : base_word_len, "base" : base_word, "word" : word, "pos" : word_pos, "tag" : word_tag, "dep" : word_dep, "lemma" : word_lemma}
                    words.append(token_dict)
                    word = ttext
                    word_pos = token.pos_
                    word_tag = token.tag_
                    word_dep = token.dep_
                    word_lemma = token.lemma_
                
                count += 1
            
            base_word = re.sub(r'^\W+',"", word)
            base_word = re.sub(r'\W+$',"", base_word)
            base_word = base_word.lower()
            base_word_len = len(base_word)
            token_dict = {"base_len" : base_word_len, "base" : base_word, "word" : word, "pos" : word_pos, "tag" : word_tag, "dep" : word_dep, "lemma" : word_lemma}
            words.append(token_dict)
    
    uniq_words = []
    for word in words:
        if word not in uniq_words:
            uniq_words.append(word)
    
    for uniq_word in uniq_words:
        count = 0
        for word in words:
            if uniq_word == word:
                count += 1
        uniq_word['occurence'] = count
        
    sorted_uniq_words = sorted(uniq_words, key=lambda k: (k['base'], -k['occurence'], k['word'].lower()))
            
    return '\n'.join(json.dumps(word, ensure_ascii=False) for word in sorted_uniq_words)

if __name__ == '__main__':
    print(find_uniq_lines(sys.stdin.read()))