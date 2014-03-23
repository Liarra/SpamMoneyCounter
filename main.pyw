import mail, filewriter, widget
import threading, time
import ConfigParser


class mainSMC:
	money = 0
	cycleThread = None
	period = 10 * 60

	def main(self):
		t1 = threading.Thread(target=self.cycle)
		t1.start()
		
		self.money = filewriter.getSum()
		
		self.prepareMail()
		self.prepareWidget()		
		#That's it, this line runs the wxPython application loop, so no lines after this are executed

	def prepareMail(self):
		cfg=ConfigParser.SafeConfigParser()
		cfg.readfp(open('mailbox.config'))
		mail.name=cfg.get('Gmail','login')
		mail.password=cfg.get('Gmail','password')


	def prepareWidget(self):
		widget.registerOnClick(self.cycle)
		widget.update(self.money)
		widget.main()
			

	def cycle(self, anything=None):
		import traceback
		time.sleep(20) #Reducing the chance that the internet is not yet on after wake-up
		file = open('error.txt', 'a')
		try:
			if self.cycleThread is not None:
				self.cycleThread.cancel()
			self.doItBaby(anything)
		except Exception as tr:
			traceback.print_exc(file)
		finally:
			self.cycleThread = threading.Timer(self.period, self.cycle)
			self.cycleThread.start()
			file.close()
			

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
		
	def checkItAgain(self):
		newmoney = mail.getIntoMailbox("")
		return newmoney

	def rewriteIt(self, num):
		filewriter.writeNewSum(num)		
			

mainSMC().main()
