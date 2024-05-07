#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from models.domain import Domain
from classes.permanent_repository.mutations.checked_domains import (
    CheckedDomainsMutations,
)
from modules.get_whois import get_whois, DomainStates
import sys
import time
import random
import orjson as json
import pandas as pd
from classes.keyword import Keyword
from classes.user_repository.mutations.user_preferences import UserPreferenceMutations
from classes.user_repository.repository import UserRepository
from datetime import datetime

# Checks domain availability using whois
def check_domains(namelist_filepath):

    domains = CheckedDomainsMutations.get_domains()

    domain_log = {
        domain.name: domain
        for domain in filter(
            lambda domain: domain.domain_expiration < datetime.now().timestamp(),
            domains,
        )
    }

    keyword_tmp = {}

    # Open file with generated names
    with open(namelist_filepath, "rb") as namelist_file:
        names = json.loads(namelist_file.read())

    # Get blacklisted keywords
    UserRepository.init_user()
    keyword_blacklist = UserPreferenceMutations.get_blacklisted()

    # Shuffle pre-generated names from the name generator and sort by name score.
    # This is so that the names don't get picked in alphabetical order but names with higher scores are prioritized.
    random.shuffle(names)
    names = sorted(names, key=lambda k: (k["name_score"] * -1))

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
                break
            elif available == limit:
                break

        else:
            domain = name["domain"]
            print(f"Checking {domain}...")
            keyword = list(name["keyword1"])
            keyword1 = Keyword(keyword=keyword[0].lower(), wordsAPI_pos=keyword[1])
            keyword = list(name["keyword2"])
            keyword2 = Keyword(keyword=keyword[0].lower(), wordsAPI_pos=keyword[1])

            # Skip name if name is in domain_check_log
            if domain in domain_log:
                print(f"'{domain}' already checked", "\n")

            # Skip name if word is used more than two time
            elif keyword1.keyword in keyword_tmp.keys() and keyword_tmp[keyword1.keyword] > 2:
                print(f"'{keyword1.keyword}' already used too often. Skipping name...", "\n")

            elif keyword2.keyword in keyword_tmp.keys() and keyword_tmp[keyword2.keyword] > 2:
                print(f"'{keyword2.keyword}' already used too often. Skipping name...", "\n")

            # Skip name if name contains blacklisted keywords
            elif (keyword1_bad := keyword1 in keyword_blacklist) or (
                keyword2_bad := keyword2 in keyword_blacklist
            ):
                try:
                    if keyword1_bad:
                        print(f"Blacklisted word '{keyword1.keyword}' used in name", "\n")
                except UnboundLocalError:
                    print("")

                try:
                    if keyword2_bad:
                        print(f"Blacklisted word '{keyword2.keyword}' used in name", "\n")
                except UnboundLocalError:
                    print("")

            else:
                # Access whois API
                domain_result: Domain = get_whois(domain)
                # If domain is available
                if domain_result.availability == DomainStates.AVAIL:
                    available_domains.append(name)
                    print(f"{domain} available")
                    print(
                        f"Date checked: {time.strftime('%d-%b-%Y (%H:%M:%S)').format(domain_result.date_checked)}"
                    )
                    # print(domain_result.to_json())
                    CheckedDomainsMutations.upsert_domain(
                        Domain.from_json(domain_result.to_json())
                    )
                    if keyword1.keyword in keyword_tmp.keys():
                        print(keyword1.keyword + " (keyword1) previously used")
                        key_count = keyword_tmp[keyword1.keyword] + 1
                        keyword_tmp.update({keyword1.keyword: key_count})
                    else:
                        print(keyword1.keyword + " (keyword1) new")
                        keyword_tmp[keyword1.keyword] = 1

                    if keyword2.keyword in keyword_tmp.keys():
                        print(keyword2.keyword + " (keyword1) previously used")
                        key_count = keyword_tmp[keyword2.keyword] + 1
                        keyword_tmp.update({keyword2.keyword: key_count})
                    else:
                        print(keyword2.keyword + " (keyword2) new")
                        keyword_tmp[keyword2.keyword] = 1

                    available += 1
                # If domain is not available
                elif domain_result.availability == DomainStates.NOT_AVAIL:
                    print(f"{domain} not available.")
                    print(
                        f"Expiration date: {time.strftime('%d-%b-%Y (%H:%M:%S)').format(domain_result.domain_expiration)}"
                    )
                    print(
                        f"Date checked: {time.strftime('%d-%b-%Y (%H:%M:%S)').format(domain_result.date_checked)}"
                    )

                    # Stop the script for 1 second to make sure API is not overcalled.
                    time.sleep(1)
                # If connection error
                elif domain_result.availability == DomainStates.UNKNOWN:
                    error_count += 1

                counter += 1
                print(f"Names processed: {counter}")
                print(f"Names available: {available}", "\n")

    if available == 0:
        print(
            "No available domains collected. Check your internet connection or add more source data."
        )
        sys.exit()

    # Export to excel file
    df1 = pd.DataFrame.from_dict(available_domains, orient="columns")

    df1.insert(4, column="Name and Domain check", value="")
    df1.insert(7, column="Keyword 1 check", value="")
    df1.insert(9, column="Keyword 2 check", value="")

    df1.to_excel(sys.argv[2])

    with open("ref/keywordstmp_list.json", "wb+") as out_file:
        out_file.write(json.dumps(keyword_tmp, option=json.OPT_INDENT_2))

if __name__ == "__main__":
    check_domains(sys.argv[1])
