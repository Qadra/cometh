#!/usr/bin/env python3

import yaml
from colorama import Fore, Back, Style
from time import sleep, time
from email.parser import BytesParser
import imaplib, smtplib, uuid, traceback


# TODO
# - Crash in TestMailDeletions if dovecot cannot access mail folders
# - Test that invalid SMTP password fails
# - Find better solution for sharing of data

class Test: # {{{
    # Override and call
    def __init__(self, name, description):
        self.description = description
        self.RequirePassed = []

    # Override
    def run(self, P):
        pass

    def __str__(self):
        return self.description

    def prereq(self, P):
        if hasattr(self, 'force'):
            if self.force == True:
                return True
            else:
                return False

        for C in self.RequirePassed:
            if not C.__name__ in P or P[C.__name__][0] == False:
                return False

        return True

    def data(self):
        if hasattr(self, 'd'):
            return self.d
        else:
            return None

    def error(self):
        if hasattr(self, 'errmsg'):
            return self.errmsg
        else:
            return None
# }}}

class GenericIMAPMailReaderTest(Test): # {{{
    def __init__(self, name, description, host, port, username, password, search):
        super(GenericIMAPMailReaderTest, self).__init__(
                name, description
                )
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.search = search
        self.RequirePassed.extend([TestSMTPSendUnauthMail, TestIMAPAuth])

    def searchfunc(self, x, d):
        return False

    def run(self, P):
        waittime = 5
        try:
            mail_content = bytearray(P, 'utf-8')

            with imaplib.IMAP4(self.host, self.port) as C:
                success = False
                C.login(self.username, self.password)
                C.select()

                t0 = time()
                while time() - t0 < waittime:
                    typ, data = C.search(None, 'ALL') 
                    for num in data[0].split():
                        typ, d = C.fetch(num, self.search)

                        if self.searchfunc(d, mail_content):
                            success = True
                            break

                    if success == True:
                        break

                    sleep(0.25)

                # Empty the mailbox
                #typ, data = C.search(None, 'ALL') 
                #for num in data[0].split():
                #    C.store(num, '+FLAGS', '\\DELETED')

                #C.expunge()
                C.close()

                if success == False:
                    raise Exception("Message to {0} with string '{1}' not found in {2} seconds".format(self.username, mail_content, waittime))


        except Exception as e:
            self.errmsg = str(e)
#}}}

class TestSMTPConnect(Test): # {{{
    def __init__(self, host, port):
        super(TestSMTPConnect, self).__init__(self.__class__.__name__, "SMTP Connect")
        self.host = host
        self.port = port

    def run(self, P):
        try:
            with smtplib.SMTP(host = self.host, port = self.port) as C:
                msg = C.ehlo("test.example.com")
                msg = C.noop()

        except Exception as e:
            self.errmsg = str(e)
# }}}

class TestSMTPAuth(Test): # {{{
    def __init__(self, host, port, username, password):
        super(TestSMTPAuth, self).__init__(self.__class__.__name__, "SMTP Authentication")
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.RequirePassed.append(TestSMTPConnect)

    def run(self, P):
        try:
            with smtplib.SMTP(host = self.host, port = self.port) as C:
                msg = C.ehlo("test.example.com")
                msg = C.login(self.username, self.password)

        except Exception as e:
            self.errmsg = str(e)
# }}}

class TestSMTPSendUnauthMail(Test): # {{{
    def __init__(self, host, port, recipient, shouldSucceed=True):
        super(TestSMTPSendUnauthMail, self).__init__(
                self.__class__.__name__,
                "SMTP Unauth Sendmail ({0})".format(recipient)
            )

        self.host = host
        self.port = port
        self.recipient = recipient
        self.shouldSucceed = shouldSucceed
        self.RequirePassed.append(TestSMTPConnect)

    def run(self, P):
        try:
            with smtplib.SMTP(host = self.host, port = self.port) as C:
                sender = 'testfrom@example.com'
                comethid = str(uuid.uuid1())

                C.ehlo("test.example.com")
                msg = '''From: {0}\r\nTo: {1}\r\nSubject: Test\r\nCometh-ID: {2}\r\n\r\n{3}'''.format(sender, self.recipient, comethid, comethid)
                self.d = comethid
                C.sendmail(sender, self.recipient, msg)

        except Exception as e:
            if self.shouldSucceed:
                self.errmsg = str(e)
        else:
            if not self.shouldSucceed:
                self.errmsg = "Delivery succeeded"
# }}}

class TestIMAPConnect(Test): # {{{
    def __init__(self, host, port):
        super(TestIMAPConnect, self).__init__(
                self.__class__.__name__, "IMAP Connect ({0}:{1})".format(host, port))
        self.host = host
        self.port = port

    def run(self, P):
        try:
            with imaplib.IMAP4(self.host, self.port) as C:
                C.noop()

        except Exception as e:
            self.errmsg = str(e)
#}}}

class TestIMAPAuth(Test): # {{{
    def __init__(self, host, port, username, password):
        super(TestIMAPAuth, self).__init__(self.__class__.__name__, "IMAP Authentication")
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.RequirePassed.append(TestIMAPConnect)

    def run(self, P):
        try:
            with imaplib.IMAP4(self.host, self.port) as C:
                C.login(self.username, self.password)

        except Exception as e:
            self.errmsg = str(e)
#}}}

class TestIMAPMailReceived(GenericIMAPMailReaderTest): # {{{
    def __init__(self, host, port, username, password):
        super(TestIMAPMailReceived, self).__init__(
                self.__class__.__name__,
                "IMAP Mail Received ({0})".format(username),
                host, port, username, password,
                'BODY[TEXT]'
                )
        #self.force = True #TODO: Run while testing

    def searchfunc(self, x, data):
        body = x[0][1]
        return data in body 
#}}}

class TestMailPassedSpamfilter(GenericIMAPMailReaderTest): # {{{
    def __init__(self, host, port, username, password):
        super(TestMailPassedSpamfilter, self).__init__(
                self.__class__.__name__,
                "IMAP Mail Passed Spamfilter ({0})".format(username),
                host, port, username, password,
                'RFC822.HEADER'
                )
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.RequirePassed.extend([TestSMTPSendUnauthMail, TestIMAPAuth, TestIMAPMailReceived])

        #self.force = True #TODO: Run while testing

    def searchfunc(self, x, data):
        h = BytesParser().parsebytes(x[0][1], headersonly=True)
        data = data.decode('utf-8')
        print(data)
        print(h['Cometh-ID'])
        if 'Cometh-ID' in h and h['Cometh-ID'] == data and 'X-Spam-Status' in h:
            return True

        return False

#}}}

class TestMailDeletions(Test): # {{{
    def __init__(self, host, port, username, password):
        super(TestMailDeletions, self).__init__(
                self.__class__.__name__,
                "Delete emails"
                )
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.RequirePassed.extend([TestSMTPSendUnauthMail, TestIMAPAuth, TestIMAPMailReceived])

        #self.force = True

    def run(self, P):
        try:
            mail_content = bytearray(P, 'utf-8')

            with imaplib.IMAP4(self.host, self.port) as C:
                success = False
                C.login(self.username, self.password)
                C.select()


                # Empty the mailbox
                typ, data = C.search(None, 'ALL') 
                for num in data[0].split():
                    C.store(num, '+FLAGS', '\\DELETED')

                C.expunge()

                resp = C.select()
                if int(resp[1][0]) != 0:
                    raise Exception("Non-zero message count after delete")

                C.close()

        except Exception as e:
            traceback.print_exc()
            self.errmsg = str(e)
#}}}


def run_test(c, P, data): # {{{
    if type(c) == tuple:
        (c, k) = c
    else:
        k = ''

    print(Style.BRIGHT + c.description + Style.RESET_ALL + ": ", end='')

    if not c.prereq(P):
        P[c.__class__.__name__ + k] = (False, None)
        print(Back.YELLOW + "Skipped" + Style.RESET_ALL)
        return

    if k != '' and k in data:
        session = data[k]
    else:
        session = None

    c.run(session)

    if c.error() == None:
        P[c.__class__.__name__ + k] = (True, c.data())
        if k != '' and c.data() != None:
            data[k] = c.data()
        print(Back.GREEN + "Pass" + Style.RESET_ALL)
    else:
        P[c.__class__.__name__ + k] = (False, None)
        print(Back.RED + "Fail" + Style.RESET_ALL + " ", end = '')
        print(Fore.RED + Style.DIM + c.error() + Style.RESET_ALL)
# }}}

def main():
    Tests = []

    Tests.append(TestSMTPConnect('localhost', '25'))
    Tests.append(TestSMTPSendUnauthMail('localhost', '25', 'test@example.com'))
    Tests.append(TestSMTPSendUnauthMail('localhost', '25', 'nonexistant@example.com', False))

    Tests.append(TestSMTPAuth('localhost', '25', 'test@example.com', 'test'))

    Tests.append(TestIMAPConnect('localhost', '143'))
    Tests.append(TestIMAPAuth('localhost', '143', 'test@example.com', 'test'))

    Tests.append(TestIMAPMailReceived('localhost', '143', 'test@example.com', 'test'))
    Tests.append(TestMailPassedSpamfilter('localhost', '143', 'test@example.com', 'test'))

    # WARNING!! DELETES ALL MESSAGES IN INBOX
    Tests.append(TestMailDeletions('localhost', '143', 'test@example.com', 'test'))


    TestStatus = {}
    data = {}
    for T in Tests:
        run_test(T, TestStatus, data)

if __name__ == '__main__':
    main()
    print(Style.RESET_ALL, end='')
