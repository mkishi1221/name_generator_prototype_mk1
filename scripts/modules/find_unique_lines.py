#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import regex as re
import json


def find_unique_lines(text):

    # Replace only-white space lines with nothing, replace multiple spaces with single spaces and split into list
    text = re.sub(r"^\W+$", "", text)
    text = re.sub(r"  +", " ", text)
    lines = text.split("\n")

    lines = [line for line in lines if line != ""]
    lines = [line for line in lines if line != " "]

    # filter unique lines
    unique_lines = set(lines)
    unique_lines_with_data = []

    # add info for each unique line in dict format
    for unique_line in unique_lines:
        unique_lines_with_data.append(
            {
                "line": unique_line,
                "occurence": lines.count(unique_line),
                "len": len(unique_line),
            }
        )

    # sort lines by length, occurence and alphabetical oder
    sorted_unique_lines = sorted(
        unique_lines_with_data,
        key=lambda k: (-k["len"], -k["occurence"], k["line"].lower()),
    )

    # number lines
    for index, sorted_unique_line in enumerate(sorted_unique_lines):
        sorted_unique_line["line_count"] = index

    # save tmp file to double-check data
    with open("ref/tmp_unique_lines.json", "w+") as out_file:
        json.dump(sorted_unique_lines, out_file, ensure_ascii=False, indent=1)

    return sorted_unique_lines
