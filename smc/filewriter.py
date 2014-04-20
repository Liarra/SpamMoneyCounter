def writeNewSum(sum):
	file=open("sum",'w+')
	file.write(str(sum))
	file.close()
	
def getSum():
	import os
	
	if os.path.exists('sum'):
		file=open("sum",'r+')
		str=file.readline()
		file.close()
		
		if len(str)==0:
			return 0
		return int(str)
	else:
		return 0
