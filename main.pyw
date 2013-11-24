import mail, filewriter, widget
import threading, time


class mainSMC:
	money = 0
	t = None
	period = 10 * 60

	def main(self):
		self.money = filewriter.getSum()
		widget.update(self.money)
		self.cycle()
		#widget.registerOnClick(self.doItBaby())
		widget.registerOnClick(self.cycle)

		#tr = threading.Thread(target=self.sleepCycle())
		#tr.start()

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
		#try:
		file.write("Into mailbox...\n")
		self.money += self.checkItAgain()

		file.write("Writing the file...\n")
		self.rewriteIt(self.money)

		file.write("Updating UI...\n")
		widget.update(self.money)

		file.close()

	def cycle(self, anything=None):
		import traceback
		time.sleep(10) #Reducing the chance that the internet is not yet on after wake-up
		file = open('error.txt', 'a')
		try:
			if self.t is not None:
				self.t.cancel()
			self.doItBaby(anything)
			self.t = threading.Timer(self.period, self.cycle)
			self.t.start()
		except Exception as tr:
			traceback.print_exc(file)
		file.close()

	def sleepCycle(self):
		import traceback
		file = open('error.txt', 'a')
		while (True):
			try:
				self.doItBaby
			except Exception as tr:
				traceback.print_exc(file)
			time.sleep(self.period)
		file.close()


mainSMC().main()