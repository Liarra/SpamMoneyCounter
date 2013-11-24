def writeNewSum(sum):
	file=open("sum",'w')
	file.write(str(sum))
	file.close()
	
def getSum():
	file=open("sum")
	str=file.readline()
	file.close()
	return int(str)
	

##writeNewSum(10)
#writeNewSum(20)
#writeNewSum(30)
#writeNewSum(10030)
