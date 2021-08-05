#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import whois
from models.domain import Domain
from datetime import datetime, timedelta

# Search domain database by calling the whois database in python


class DomainStates:
    AVAIL = "domain available"
    NOT_AVAIL = "domain not available"
    UNKNOWN = "connection error"


def get_whois(name) -> Domain:

    # Call whois API to get domain information
    try:
        flags = 0
        flags = flags | whois.NICClient.WHOIS_QUICK
        w = whois.whois(name, flags=flags)
        domain_expiration = int(w.expiration_date.timestamp())
        status = DomainStates.NOT_AVAIL
    except (whois.parser.PywhoisError):
        domain_expiration = int((datetime.now() + timedelta(days=1)).timestamp())
        status = DomainStates.AVAIL
    except (AttributeError):
        domain_expiration = None
        status = DomainStates.UNKNOWN

    data = Domain(name, status, domain_expiration)

    return data


# For testing purposes:
# print(get_whois("google.com"))
