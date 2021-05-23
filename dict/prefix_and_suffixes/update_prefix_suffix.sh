#!/bin/bash

FILES=original_data/*.*
for file in $FILES
do
    
    filename=$(basename ${file})
    word_type=$(basename ${file%.*})
    
    echo "Converting ${filename}..."
    python3 generate_prefix_suffix_dict.py \
        ${file} \
        ${word_type} \
        "../${word_type}.json"
    
done