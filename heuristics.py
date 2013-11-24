import re
def findBigNumericNumbers(letter):
	ret={}
	regex=re.compile(ur"(\$ ?\d{1,3}([., ]?000)+)")
	match=regex.finditer(letter)
	for m in match:
		ret[m.group()]=m.start()
	return ret

def findCurrency(letter, numbers):
	pass
	
def getAmountInDollars(letter):
	strings=findBigNumericNumbers(letter)
	sum=0
	#print strings.keys()
	for s in strings.keys():
		num=(re.findall(ur"\$ ?(.*)",s))[0]
		
		num=num.replace(".","")
		num=num.replace(",","")
		num=num.replace(" ","")
		
		sum+=int(num)
	return sum

#letter="$1000 sdfd $ 5 000 000 34233 123 dfdfdfd $5,000,000 8.000 000,000"
#print findBigNumericNumbers(letter)
#print getAmountInDollars(letter)