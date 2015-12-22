import heuristics

name = "m.e.tigra"
password = "Meliss@123"


def get_into_mailbox(server="imap.googlemail.com"):
    import imaplib

    conn = imaplib.IMAP4_SSL(server)
    conn.login(name, password)

    typ, folders = conn.list()

    folder_id=None
    for folder in folders:
        flags, delimiter, mailbox_name = parse_list_response(folder)
        if "\Junk" in flags:
            folder_id = mailbox_name

    print folder_id

    code, dummy = conn.select(folder_id)
    if code != 'OK':
        print dummy
        raise RuntimeError, "Failed to select inbox"

    code, data = conn.search(None, 'ALL')
    if code == 'OK':
        msgid_list = data[0].split()
    else:
        raise RuntimeError, "Failed to get message IDs"
    s = 0
    for msgid in msgid_list:
        code, data = conn.fetch(msgid, '(BODY[1])')
        # you can also use '(RFC822.HEADER)' only for headers
        if code == 'OK':
            d = heuristics.get_amount_in_dollars(str(data))
            s += d
            if d > 0:
                print "removing..."
                conn.store(msgid, '+FLAGS', '\\Deleted')
        else:
            raise RuntimeError, "could not retrieve msgid %r" % msgid

    conn.close()
    conn.logout()
    print "$" + str(s)
    return s


def parse_list_response(line):
    import re
    list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return flags, delimiter, mailbox_name

# getIntoMailbox(0)
