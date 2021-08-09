#!/bin/bash

# Check if data with sentences exists
if [ -n "$(ls -A data/*.txt 2>/dev/null)" ]; then
    # Pour source texts modification dates into one file
    sentences="exists"
    FILES=data/*.*
    for f in $FILES
    do
    ls -lh ${f} \
    >> ref/logs/source_data_log.tsv
    done
else
    sentences="none"
    echo "No sentences found! Checking if keywords are supplied..."
fi

echo ${sentences}