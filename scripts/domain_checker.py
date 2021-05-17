#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from modules.get_whois import DomainInfo, DomainStates
import sys
import time
from modules.get_whois import get_whois


def check_domains(namelist_filepath):

    names_data = open(namelist_filepath, "r").read()
    names = names_data.split("\n")

    counter = 0
    available = 0
    limit = int(sys.argv[3])
    available_domains = []

    for name in names:
        if available == limit:
            break
        else:
            domain = f"{name}.com"
            print(f"Checking {domain}...")

            domain_result: DomainInfo = get_whois(domain)

            if domain_result.status == DomainStates.AVAIL:
                domain_name = f"{name}\t{domain}"
                available_domains.append(domain_name)
                print(f"{domain} available")
                available = available + 1

            elif domain_result.status == DomainStates.NOT_AVAIL:
                print(f"{domain} not available")

            counter = counter + 1
            print(f"Names processed: {counter}")
            print(f"Names available: {available}")
            print("")

        time.sleep(1)

    available_domains = "\n".join(available_domains)

    with open(sys.argv[2], "w+") as out_file:
        out_file.write(available_domains)


if __name__ == "__main__":
    check_domains(sys.argv[1])