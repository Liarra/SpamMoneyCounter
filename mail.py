import heuristics
def getIntoMailbox(server,name,password):
	import imaplib
	conn= imaplib.IMAP4_SSL('imap.googlemail.com')
	conn.login(name, password)

	code, dummy= conn.select(ur'[Gmail]/&BCEEPwQwBDw-')
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

#getIntoMailbox("","m.e.tigra","Licantr0pia")