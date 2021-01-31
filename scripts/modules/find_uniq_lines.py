#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import regex as re
import sys
import json

def find_uniq_lines(text):

    # Replace only-white space lines with nothing, replace multiple spaces with single spaces and split into list
    text = re.sub(r"^\W+$", "", text)
    text = re.sub(r"  +", " ", text)
    lines = text.split("\n")

    #Remove blank lines
    lines = [line for line in lines if line != '']
    lines = [line for line in lines if line != ' ']

    # Filter unique lines
    uniq_lines = list(set(lines))
    uniq_lines_with_data = []

    # Add info for each uniq line in dict format
    for uniq_line in uniq_lines:
        uniq_lines_with_data.append(
            {
                "line": uniq_line,
                "occurence": lines.count(uniq_line),  # count returns occurences of list items
                "len": len(uniq_line),  # no need to assign unnecessary vars
            }
        )

    # Sort lines by length, occurence and alphabetical oder
    sorted_uniq_lines = sorted(
        uniq_lines_with_data,
        key=lambda k: (-k["len"], -k["occurence"], k["line"].lower()),
    )

    #Number lines
    count = 1
    for sorted_uniq_line in sorted_uniq_lines:
        sorted_uniq_line['line_count'] = count
        count += 1

    #Save tmp file to double-check data
    with open("ref/tmp_unique_lines.json", "w+") as out_file:
        json.dump(sorted_uniq_lines, out_file, ensure_ascii=False, indent=1)

    return sorted_uniq_lines