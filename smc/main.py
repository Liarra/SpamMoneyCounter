import mail, filewriter, widget
import threading, time
import ConfigParser


class mainSMC:
	money = 0
	cycleThread = None
	period = 10*60

	def main(self):
		t1 = threading.Thread(target=self.cycle)
		t1.setDaemon(True)
		t1.start()
		
		self.money = filewriter.getSum()
		
		self.prepareMail()
		self.prepareWidget()
		print "Bye"
		# t1.
		#exit(0)
		#That's it, this line runs the wxPython application loop, so no lines after this are executed

	def prepareMail(self):
		cfg=ConfigParser.SafeConfigParser()
		cfg.readfp(open('mailbox.config'))
		mail.name=cfg.get('Gmail','login')
		mail.password=cfg.get('Gmail','password')


	def prepareWidget(self):
		#widget.registerOnClick(self.cycle)
		widget.update(self.money)
		widget.main()
			

	def cycle(self, anything=None):
		import traceback
		from datetime import datetime
		time.sleep(20) #Reducing the chance that the internet is not yet on after wake-up
		error_log = open('error.txt', 'a')
		try:
			if self.cycleThread is not None:
				self.cycleThread.cancel()
			self.doItBaby(anything)
		except Exception as tr:
			error_log.write('['+str(datetime.now())+'] '+str(tr)+"\n")
			traceback.print_exc(file=error_log)
			error_log.write("\n")
			
		finally:
			self.cycleThread = threading.Timer(self.period, self.cycle)
			self.cycleThread.setDaemon(True)
			self.cycleThread.start()
			error_log.close()
			

	def doItBaby(self, anything=None):
		self.money += self.checkItAgain()

		self.rewriteIt(self.money)
		widget.update(self.money)
		
	def checkItAgain(self):
		newmoney = mail.getIntoMailbox("")
		return newmoney

	def rewriteIt(self, num):
		filewriter.writeNewSum(num)		
			
if __name__ == "__main__":
	mainSMC().main()
