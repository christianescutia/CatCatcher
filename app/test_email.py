import smtplib

gmail_user = 'catcatcher.noreply@gmail.com'
gmail_password = 'cat_catcher_2021'

sent_from = gmail_user
to = ['christianescutia8520@gmail.com']
subject = 'Cat Catcher Test Email'
body = 'Hello Test Messages'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print ('Email sent!')
except:
    print ('Something went wrong...')