#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import whois
from datetime import datetime

# Search domain database by calling the whois database in python

class DomainStates:
    AVAIL = "domain available"
    NOT_AVAIL = "domain not available"

class DomainInfo:
    def __init__(self, domain, status, expiration_date):
        self.domain = domain
        self.status = status
        self.expiration_date = expiration_date
        self.date_searched = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")

    def __repr__(self) -> str:
        return f"Domain: {self.domain}\nStatus: {self.status}\nExpiration date: {self.expiration_date}\nDate searched: {self.date_searched}"


def get_whois(name) -> DomainInfo:

    # Call whois API to get domain information
    try:
        flags = 0
        flags = flags | whois.NICClient.WHOIS_QUICK
        w = whois.whois(name, flags=flags)
        domain_expiration = w.expiration_date.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        status = "domain not available"
    except (whois.parser.PywhoisError):
        domain_expiration = ""
        status = "domain available"

    data = DomainInfo(name, status, domain_expiration)

    return data


# For testing purposes:
# print(get_whois("google.com"))