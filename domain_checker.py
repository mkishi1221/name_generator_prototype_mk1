#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from modules.get_whois import get_whois, DomainStates, DomainInfo
import sys
import time
import random
import json
import pandas as pd


# Checks domain availability using whois
def check_domains(namelist_filepath):

    with open(namelist_filepath) as namelist_file:
        names = json.load(namelist_file)

    # Shuffle pre-generated names from the name generator.
    random.shuffle(names)

    counter = 0
    available = 0
    limit = int(sys.argv[3])
    available_domains = []

    # Check names from top of the shuffled name list until it reaches the desired number of available names
    # Desired number of available names specified by the "limit" available in bash file "create_names.sh"
    for name in names:
        if available == limit:
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

            counter = counter + 1
            print(f"Names processed: {counter}")
            print(f"Names available: {available}")
            print("")

        # Stop the script for 1 second to make sure API is not overcalled.
        time.sleep(1)

    # Export to excel file
    df1 = pd.DataFrame.from_dict(available_domains, orient="columns")

    df1.insert(3, column='Name and Domain check', value='')
    df1.insert(6, column='Algorithm and joint check', value='')
    df1.insert(9, column='Keyword 1 check', value='')
    df1.insert(11, column='Keyword 2 check', value='')

    df1.to_excel(sys.argv[2])


if __name__ == "__main__":
    check_domains(sys.argv[1])
