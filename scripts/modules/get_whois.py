#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import whois
from datetime import datetime

def domain_info(domain_name, status, expiration_date) -> dict:

    timestamp = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")

    return {
        "domain": domain_name,
        "status": status,
        "expiration_date": expiration_date,
        "date_searched": timestamp
    }

def get_whois(name):

    try:
        flags = 0
        flags = flags | whois.NICClient.WHOIS_QUICK
        w=whois.whois(name, flags=flags)
        domain_expiration = w.expiration_date.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        status = "domain not available"

    except(whois.parser.PywhoisError):
        domain_expiration = ""
        status = "domain available"

    data = domain_info(name, status, domain_expiration)

    return data

# For testing purposes:
# print(get_whois("google.com"))