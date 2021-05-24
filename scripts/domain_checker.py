#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from modules.get_whois import DomainInfo, DomainStates
import sys
import time
import random
from modules.get_whois import get_whois

# Checks domain availability using whois
def check_domains(namelist_filepath):

    names_data = open(namelist_filepath, "r").read()
    names = names_data.split("\n")

    # Shuffle pre-generated names from the name generator.
    random.shuffle(names)

    counter = 0
    available = 0
    limit = int(sys.argv[3])
    available_domains = []

    # Check names from top of the shuffled name list until the it reaches the desired number of available names (specified by the "limit" available in bash)
    for name in names:
        if available == limit:
            break
        else:
            domain = f"{name}.com"
            print(f"Checking {domain}...")

            # Access whois API
            domain_result: DomainInfo = get_whois(domain)

            # If domain is available
            if domain_result.status == DomainStates.AVAIL:
                domain_name = f"{name}\t{domain}"
                available_domains.append(domain_name)
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

    available_domains = "\n".join(available_domains)

    # Output available names
    with open(sys.argv[2], "w+") as out_file:
        out_file.write(available_domains)


if __name__ == "__main__":
    check_domains(sys.argv[1])