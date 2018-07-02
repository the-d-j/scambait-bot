from decouple import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER = config('SENDER')
SENDER_PWD = config('SENDER_PWD')

recipient = 'thedonnieutley@gmail.com'

# message = 
"""From: From Person <test@geekrho.com>
To: To Person <17donnie@gmail.com>
MIME-Version: 1.0
Content-type: text/html
Subject: SMTP HTML e-mail test

This is an e-mail message to be sent in HTML format

<b>This is HTML message.</b>
<h1>This is headline.</h1>
"""

msg = MIMEMultipart()
msg['From'] = SENDER
msg['To'] = recipient
msg['Subject'] = "I <3 SPAM!"

body = "This is some message for the body."
msg.attach(MIMEText(body, 'plain'))


try:
  #  server = smtplib.SMTP('localhost')
  server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
  # server.starttls()
  # server.login('17donnie@gmail.com', 'password')
  server.login(SENDER, SENDER_PWD)
  for i in range(1):
    final_msg = msg.as_string()
    msg['From'] = str(i)+"@gmail.com"
    server.sendmail(SENDER, recipient, final_msg)         
  print("Successfully sent email")
except:
  print("Error: unable to send email")

server.quit()