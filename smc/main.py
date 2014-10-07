import mail, filewriter, widget
import threading, time
import ConfigParser
from datetime import datetime


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
				#That's it, this line runs the wxPython application loop, so no lines after this are executed before app exit
		print "Bye"
		exit (0)

	def prepareMail(self):
		cfg=ConfigParser.SafeConfigParser()
		cfg.readfp(open('mailbox.config'))
		mail.name=cfg.get('Gmail','login')
		mail.password=cfg.get('Gmail','password')


	def prepareWidget(self):
		widget.update(self.money)
		widget.main()
			

	def cycle(self, anything=None):
		
		time.sleep(20) #Reducing the chance that the internet is not yet on after wake-up
		
		try:
			if self.cycleThread is not None:
				self.cycleThread.cancel()
			self.doItBaby()
		except Exception as tr:
			self.writeToLog(tr)
			
		finally:
			self.cycleThread = threading.Timer(self.period, self.cycle)
			self.cycleThread.setDaemon(True)
			self.cycleThread.start()
	
	
	def writeToLog(self, exception):
		import traceback
		
		error_log = open('error.txt', 'a')
		
		error_log.write('['+str(datetime.now())+'] '+str(tr)+"\n")
		traceback.print_exc(file=error_log)
		error_log.write("\n")
		
		error_log.close()
		

	def doItBaby(self):
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
