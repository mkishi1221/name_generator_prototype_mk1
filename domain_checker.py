#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from modules.get_whois import get_whois, DomainStates, DomainInfo
import sys
import time
import random
import orjson as json
import pandas as pd
from os import path
from classes.keyword import Keyword

# Checks domain availability using whois
def check_domains(namelist_filepath):

    with open(namelist_filepath, "rb") as namelist_file:
        names = json.loads(namelist_file.read())

    keyword_blacklist = []
    if path.exists('ref/keyword_blacklist.json'):
        with open('ref/keyword_blacklist.json', "rb") as keyword_blacklist_file:
            keyword_blacklist_json = json.loads(keyword_blacklist_file.read())
        for keyword in keyword_blacklist_json:
            keyword_blacklist.append(Keyword("", keyword['keyword_len'], keyword['keyword'], "", "", keyword['wordsAPI_pos'], "", 0))

    # Shuffle pre-generated names from the name generator.
    random.shuffle(names)

    counter = 0
    available = 0
    error_count = 0
    limit = int(sys.argv[3])
    available_domains = []

    # Check names from top of the shuffled name list until it reaches the desired number of available names
    # Desired number of available names specified by the "limit" available in bash file "create_names.sh"
    for name in names:
        if available == limit or error_count == 5:
            if error_count == 5:
                print("Connection unstable: check your internet connection.")
            break
        else:
            domain = name["domain"]
            print(f"Checking {domain}...")

            # Access whois API
            domain_result: DomainInfo = get_whois(domain)

            # If domain is available
            if domain_result.status == DomainStates.AVAIL:
                available_domains.append(name)
                print(f"{domain} available")
                available = available + 1

            # If domain is not available
            elif domain_result.status == DomainStates.NOT_AVAIL:
                print(f"{domain} not available")

            # If connection error
            elif domain_result.status == DomainStates.UNKNOWN:
                error_count += 1

            counter = counter + 1
            print(f"Names processed: {counter}")
            print(f"Names available: {available}")
            print("")

        # Stop the script for 1 second to make sure API is not overcalled.
        time.sleep(1)

    if available == 0:
        print("No available domains collected. Check your internet connection or add more source data.")
        sys.exit()

    # Export to excel file
    df1 = pd.DataFrame.from_dict(available_domains, orient="columns")

    df1.insert(4, column='Name and Domain check', value='')
    df1.insert(7, column='Keyword 1 check', value='')
    df1.insert(9, column='Keyword 2 check', value='')

    df1.to_excel(sys.argv[2])


if __name__ == "__main__":
    check_domains(sys.argv[1])
