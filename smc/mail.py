import heuristics
name="m.e.tigra"
password="Meliss@123"
folderid=""

def getIntoMailbox(server):
	import imaplib
	
	conn= imaplib.IMAP4_SSL('imap.googlemail.com')
	conn.login(name, password)
	
	typ,folders=conn.list()
	
	for folder in folders:
		flags, delimiter, mailbox_name = parse_list_response(folder)
		if "\Junk" in flags: folderid=mailbox_name
		
	print folderid

	code, dummy= conn.select(folderid)
	if code != 'OK':
		print dummy
		raise RuntimeError, "Failed to select inbox"

	code, data= conn.search(None, 'ALL')
	if code == 'OK':
		msgid_list= data[0].split()
	else:
		raise RuntimeError, "Failed to get message IDs"
	s=0
	for msgid in msgid_list:
		code, data= conn.fetch(msgid, '(BODY[1])')
		# you can also use '(RFC822.HEADER)' only for headers
		if code == 'OK':
			d=heuristics.getAmountInDollars(str(data))
			s+=d
			if d>0:
				print "removing..."
				conn.store(msgid, '+FLAGS', '\\Deleted')
		else:
			raise RuntimeError, "could not retrieve msgid %r" % msgid

	conn.close()
	conn.logout()
	print "$"+str(s);
	return s

def parse_list_response(line):
	import re
	list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
	flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
	mailbox_name = mailbox_name.strip('"')
	return (flags, delimiter, mailbox_name)
     	
#getIntoMailbox(0)
