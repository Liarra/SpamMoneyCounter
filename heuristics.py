#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
def findBigNumericNumbers(letter):
	ret={}
	regex=re.compile(r"(\$ ?\d{1,3}[., ]? ?(\d{3})?([., ]? ?000)+)")
	match=regex.finditer(letter)
	for m in match:
		ret[m.group()]=m.start()
	return ret
	
def findShortNumbers(letter):
	ret={}
	regex=re.compile(r"(\$ ?\d+[.,]{0,1}\d* {0,1}(million|m))",re.I)
	match=regex.finditer(letter)
	for m in match:
		ret[m.group()]=m.start()
	return ret	

def findCurrency(letter, numbers):
	pass
	
def getAmountInDollars(letter):
	strings=findBigNumericNumbers(letter)
	sum=0
	for s in strings.keys():
		num=(re.findall(ur"\$ ?(.*)",s))[0]
		
		num=num.replace(".","")
		num=num.replace(",","")
		num=num.replace(" ","")
		
		sum+=int(num)
		
	
	strings=findShortNumbers(letter)
	for s in strings.keys():
		num=(re.findall(ur"\$ ?(.*) ?(m|million)",s,re.I))[0][0]
		print num
		num=num.replace(",",".")
		
		sum+=int(float(num)*1000000)
	
	return sum

letter="Microsoft Office появились Ваш E-Mail $ 900,000.00 USD. Отправить Подробности, имя, номер телефона & страну"
#print findBigNumericNumbers(letter)
#print getAmountInDollars(letter)
#print findShortNumbers(letter)
#print getAmountInDollars(letter)
