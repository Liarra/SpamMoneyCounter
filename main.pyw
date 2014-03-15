import mail, filewriter, widget
import threading, time


class mainSMC:
	money = 0
	t = None
	period = 10 * 60

	def main(self):
		import os
		
		widget.registerOnClick(self.cycle)
		
		t1 = threading.Thread(target=self.cycle)
		t1.start()
		
		self.money = filewriter.getSum()
		widget.update(self.money)
		
		widget.main()	


	def checkItAgain(self):
		newmoney = mail.getIntoMailbox("", "m.e.tigra", "Licantr0pia")
		return newmoney

	def rewriteIt(self, num):
		filewriter.writeNewSum(num)

	def doItBaby(self, anything=None):
		import datetime

		file = open('log.txt', 'a')
		
		file.write(str(datetime.datetime.now()) + "\n")
		
		file.write("Into mailbox...\n")
		self.money += self.checkItAgain()

		file.write("Writing the file...\n")
		self.rewriteIt(self.money)

		file.write("Updating UI...\n")
		widget.update(self.money)

		file.close()

	def cycle(self, anything=None):
		import traceback
		time.sleep(20) #Reducing the chance that the internet is not yet on after wake-up
		file = open('error.txt', 'a')
		try:
			if self.t is not None:
				self.t.cancel()
			self.doItBaby(anything)
		except Exception as tr:
			traceback.print_exc(file)
		finally:
			self.t = threading.Timer(self.period, self.cycle)
			self.t.start()
			file.close()

mainSMC().main()
