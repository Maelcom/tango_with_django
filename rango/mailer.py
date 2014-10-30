import smtplib
from email.mime.text import MIMEText

DEFAULT_TEXT = "Ololo abgeschlossen!"
DEFAULT_SUBJECT = '[dev Rango] You sent it'
DEFAULT_FROM = 'dev Rango admin <maelcom@mail.ru>'
DEFAULT_TO = 'Recipient <maelcom@mail.ru>'

MAIL_PROVS = {'mail.ru': ('smtp.mail.ru', 465),
              'inbox.ru': ('smtp.mail.ru', 465),
              'list.ru': ('smtp.mail.ru', 465),
              'gmail.com': ('smtp.gmail.com', 465),
              }


def get_provs():
    return ', '.join(MAIL_PROVS.keys())


def sendphish(fromaddr="", toaddr="", pwd=""):
    text = DEFAULT_TEXT
    subj = DEFAULT_SUBJECT

    print "fromaddr {0}, toaddr {1} pwd {2}".format(fromaddr, toaddr, pwd)

    prov = fromaddr.split('@')[1]

    msg = MIMEText(text)
    msg['Subject'] = subj
    # mail.ru demands that 'From' is equal to user
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Content-Type'] = "text/html; charset=UTF-8"

    try:
        s = smtplib.SMTP_SSL(*MAIL_PROVS[prov])
        s.login(fromaddr, pwd)
        s.sendmail(fromaddr, toaddr, msg.as_string())
        s.quit()
    except KeyError:
        return "Unknown mail provider {0}".format(prov)
    except Exception as e:
        print e
        return "Could not connect to provider {0}\nCheck logs.".format(prov)
