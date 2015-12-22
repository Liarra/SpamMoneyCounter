import ConfigParser
import threading
import time
from datetime import datetime

import filewriter
import mail
import widget


def load_mail_credentials():
    cfg = ConfigParser.SafeConfigParser()
    cfg.readfp(open('mailbox.config'))
    mail.name = cfg.get('Gmail', 'login')
    mail.password = cfg.get('Gmail', 'password')


def check_new_money():
    new_money = mail.get_into_mailbox()
    return new_money


def write_new_amount(num):
    filewriter.write_new_sum(num)


class MainSMC:
    money = 0
    cycleThread = None
    period = 10 * 60

    def main(self):
        t1 = threading.Thread(target=self.cycle)
        t1.setDaemon(True)
        t1.start()

        self.money = filewriter.get_sum()

        load_mail_credentials()
        self.init_widget()
        # That's it, this line runs the wxPython application loop, so no lines after this are executed before app exit
        print "Bye"
        exit(0)

    def init_widget(self):
        widget.update(self.money)
        widget.main()

    def cycle(self, anything=None):

        time.sleep(20)  # Reducing the chance that the internet is not yet on after wake-up

        try:
            if self.cycleThread is not None:
                self.cycleThread.cancel()
            self.check_and_update()
        except Exception as tr:
            self.writeToLog(tr)

        finally:
            self.cycleThread = threading.Timer(self.period, self.cycle)
            self.cycleThread.setDaemon(True)
            self.cycleThread.start()

    def writeToLog(self, exception):
        import traceback

        error_log = open('error.txt', 'a')

        error_log.write('[' + str(datetime.now()) + '] ' + str(exception) + "\n")
        traceback.print_exc(file=error_log)
        error_log.write("\n")

        error_log.close()

    def check_and_update(self):
        self.money += check_new_money()

        write_new_amount(self.money)
        widget.update(self.money)


if __name__ == "__main__":
    MainSMC().main()
