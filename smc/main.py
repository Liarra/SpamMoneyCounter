import ConfigParser
import threading
import time
from datetime import datetime

import filewriter
import mail
from widget import SMCWidget


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


def write_to_log(exception):
    import traceback

    error_log = open('error.txt', 'a')

    error_log.write('[' + str(datetime.now()) + '] ' + str(exception) + "\n")
    traceback.print_exc(file=error_log)
    error_log.write("\n")

    error_log.close()


class MainSMC:
    money = 0
    period = 5

    # period = 10 * 60

    def __init__(self):
        self.widget = SMCWidget()

    def main(self):
        t1 = threading.Thread(target=self.cycle)
        t1.setDaemon(True)
        t1.start()

        self.money = filewriter.get_sum()

        load_mail_credentials()
        self.start_widget()
        # That's it, this line runs the wxPython application loop, so no lines after this are executed before app exit
        exit(0)

    def start_widget(self):
        self.widget.update(self.money)
        self.widget.run()

    def cycle(self, anything=None):

        while True:
            time.sleep(self.period)

            try:
                self.check_and_update()
                print "Alive"
            except Exception as tr:
                write_to_log(tr)

    def check_and_update(self):
        old_money = self.money
        self.money += check_new_money()

        if old_money != self.money:
            write_new_amount(self.money)
            self.widget.update(self.money)


if __name__ == "__main__":
    MainSMC().main()
