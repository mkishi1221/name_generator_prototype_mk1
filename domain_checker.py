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
from classes.user_repository.mutations.user_preferences import UserPreferenceMutations
from classes.user_repository.repository import UserRepository
from operator import itemgetter
from datetime import datetime

# Checks domain availability using whois
def check_domains(namelist_filepath):

    # Open domain check log file
    domain_check_log_path = "ref/logs/domain_check_log.json"
    try:
        with open(domain_check_log_path, "rb") as domain_check_log_file:
            domain_check_log = {}
            domain_check_log_original = json.loads(domain_check_log_file.read())
            for domain in domain_check_log_original:
                # Remove domains past its expiration date
                expiration_date = domain_check_log_original[domain]["domain_expiration"]
                if expiration_date is not None and datetime.strptime(expiration_date, '%d-%b-%Y (%H:%M:%S)') > datetime.now():
                    domain_check_log[domain] = domain_check_log_original[domain]

    except FileNotFoundError:
        print("file not found")
        domain_check_log = {}

    # Open file with generated names
    with open(namelist_filepath, "rb") as namelist_file:
        names = json.loads(namelist_file.read())

    # Get blacklisted keywords
    UserRepository.init_user()
    keyword_blacklist = UserPreferenceMutations.get_blacklisted()

    # Shuffle pre-generated names from the name generator and sort by name score.
    # This is so that the names don't get picked in alphabetical order but names with higher scores are prioritized.
    random.shuffle(names)
    names = sorted(names, key=lambda k: (k['name_score'] * -1))

    counter = 0
    available = 0
    error_count = 0
    limit = int(sys.argv[3])
    available_domains = []

    # Check names from top of the shuffled name list until it reaches the desired number of available names
    # Skip names that are already in the domain_check_log.
    # Desired number of available names is specified by the "limit" variable in bash file "create_names.sh"
    for name in names:

        if available == limit or error_count == 5:
            if error_count == 5:
                print("Connection unstable: check your internet connection.")
            if available == limit:
                break

        else:
            domain = name["domain"]
            print(f"Checking {domain}...")
            # Skip name if name contains blacklisted keywords
            keyword = list(name["keyword1"])
            keyword1 = Keyword(keyword=keyword[0].lower(), wordsAPI_pos=keyword[1])
            keyword = list(name["keyword2"])
            keyword2 = Keyword(keyword=keyword[0].lower(), wordsAPI_pos=keyword[1])
            if (keyword1_bad := keyword1 in keyword_blacklist) or (keyword2_bad := keyword2 in keyword_blacklist):
                if keyword1_bad:
                    print(f"Blacklisted word '{keyword1}' used in name")
                if keyword2_bad:
                    print(f"Blacklisted word '{keyword2}' used in name")

            # Skip name if name is in domain_check_log
            elif domain in domain_check_log.keys():
                print(f"'{domain}' already checked")
                print("")

            else:
                # Access whois API
                domain_result: DomainInfo = get_whois(domain)
                # If domain is available
                if domain_result.status == DomainStates.AVAIL:
                    available_domains.append(name)
                    print(f"{domain} available")
                    print(f"Date checked: {domain_result.date_searched}")
                    available += 1
                # If domain is not available
                elif domain_result.status == DomainStates.NOT_AVAIL:
                    print(f"{domain} not available.")
                    print(f"Expiration date: {domain_result.expiration_date}")
                    print(f"Date checked: {domain_result.date_searched}")
                # If connection error
                elif domain_result.status == DomainStates.UNKNOWN:
                    error_count += 1

                if domain_result.status != DomainStates.UNKNOWN:
                    domain_check_log[domain] = {
                        'name': name,
                        'availability': domain_result.status,
                        'domain_expiration': domain_result.expiration_date,
                        'date_checked': domain_result.date_searched
                    }

                # Stop the script for 1 second to make sure API is not overcalled.
                time.sleep(1)

                counter += 1
                print(f"Names processed: {counter}")
                print(f"Names available: {available}")
                print("")

    with open(domain_check_log_path, "wb+") as out_file:
        out_file.write(json.dumps(domain_check_log, option=json.OPT_INDENT_2))

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
