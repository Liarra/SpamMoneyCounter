def writeNewSum(sum):
	file=open("sum",'w+')
	file.write(str(sum))
	file.close()
	
def getSum():
	file=open("sum",'r+')
	str=file.readline()
	file.close()
	return int(str)
