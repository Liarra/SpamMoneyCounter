#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re


def find_big_numeric_numbers(letter):
    ret = {}
    regex = re.compile(r"(\$ ?\d{1,3}[., ]? ?(\d{3})?([., ]? ?000)+)")
    match = regex.finditer(letter)
    for m in match:
        ret[m.group()] = m.start()
    return ret


def find_short_numbers(letter):
    ret = {}
    regex = re.compile(r"(\$ ?\d+[.,]?\d* ?(million|m))", re.I)
    match = regex.finditer(letter)
    for m in match:
        ret[m.group()] = m.start()
    return ret


def get_amount_in_dollars(letter):
    strings = find_big_numeric_numbers(letter)
    sum_in_usd = 0
    for s in strings.keys():
        num = (re.findall(ur"\$ ?(.*)", s))[0]

        num = num.replace(".", "")
        num = num.replace(",", "")
        num = num.replace(" ", "")

        sum_in_usd += int(num)

    strings = find_short_numbers(letter)
    for s in strings.keys():
        num = (re.findall(ur"\$ ?(.*) ?(m|million)", s, re.I))[0][0]
        print num
        num = num.replace(",", ".")

        sum_in_usd += int(float(num) * 1000000)

    return sum_in_usd


debug_letter = """
Hello dear!

I'm a poor princess from Agrabah, my father left me $56m and I'm so stupid that I decided to buy a
 email database for those, and ask a random stranger to help me spend the rest.
Please reply ASAP.
"""
# print findBigNumericNumbers(letter)
# print getAmountInDollars(letter)
# print findShortNumbers(letter)
# print getAmountInDollars(letter)
