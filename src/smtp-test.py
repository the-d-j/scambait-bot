from decouple import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
from time import sleep

NUMBER_OF_EMAILS = 20 

SENDER = config('SENDER')
SENDER_PWD = config('SENDER_PWD')
recipient = 'thedonnieutley@gmail.com'

min_ws = 1
max_ws = 20


try:
  #  server = smtplib.SMTP('localhost')
  server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
  # server.starttls()
  server.login(SENDER, SENDER_PWD)
  for email in range(NUMBER_OF_EMAILS):
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = recipient

    ws1 = ''.join(random.choice(string.whitespace) for x in range(random.randint(min_ws, max_ws)))
    ws2 = ''.join(random.choice(string.whitespace) for x in range(random.randint(min_ws, max_ws)))
    # ws1 = ''.join(chr(0x20) for x in range(random.randint(1, 20)))
    # ws2 = ''.join(chr(0x20) for x in range(random.randint(1, 20)))
    subject = "I <3 SPAM!!"+ws2

    msg['Subject'] = subject
    print(msg['Subject'])

    body = "This is some message for the body."
    msg.attach(MIMEText(body, 'plain'))

    final_msg = msg.as_string()
    server.sendmail(SENDER, recipient, final_msg) 

    # secs = random.randint(10, 60) # pause between 10 and 60 seconds
    # sleep(secs)       
  print("Successfully sent email")
except:
  print("Error: unable to send email")

server.quit()
server.close()
