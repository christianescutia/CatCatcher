# Basic imports
import os

# Import to connect to postgress server
import mysql.connector

# Import for SMS messaging
from twilio.rest import Client

# Import to send emails
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# Global variables
gmail_user = ''
gmail_password = ''
ImgFileName1 = "/home/pi/rightImage.jpg"
ImgFileName2 = "/home/pi/middleImage.jpg"
ImgFileName3 = "/home/pi/leftImage.jpg"
client = Client('ACebaf22614c3bf1885d8bb9acf1638ab7','f54342d07240369873eddb11dfab5f25')

# Open connection to sql server
mydb = mysql.connector.connect(
    host='us-cdbr-east-04.cleardb.com',
    user='',
    password='',
    database= ''
)

# create cursor
c = mydb.cursor()

print("Checking for requests")

# Checks the message board to see if there are any image requests
sql_command = "SELECT username FROM msg_board WHERE box_id = \'Cage00\'"

c.execute(sql_command)

notify_list = []

onlyOnce = True

for x in c:
    str_u = str(x)
    length = len(str_u)
    sliced = str_u[2:length-3]
    notify_list.append(sliced)
    print(sliced)

    # If there is at least one request, take picutes
    if onlyOnce:
        os.system("python3 takePics.py")
        with open(ImgFileName3, 'rb') as f:
            img_data3 = f.read()

        with open(ImgFileName2, 'rb') as f:
            img_data2 = f.read()

        with open(ImgFileName1, 'rb') as f:
            img_data1 = f.read()
        onlyOnce = False

# Email the users that requested images
for x in notify_list:
    sql_command = "SELECT email FROM users WHERE username = \'" + x + "\'"
    c.execute(sql_command)
    for x in c:
        str_u = str(x)
        length = len(str_u)
        sliced = str_u[2:length-3]
        msg = MIMEMultipart()
        msg['Subject'] = 'Requested Image from Cat Catcher Cage00'
        msg['From'] = 'CatCatcher@gmail.com'
        msg['To'] = sliced
        To = [sliced]

        text = MIMEText("Cat Catcher Images")
        msg.attach(text)
        image = MIMEImage(img_data1, name=os.path.basename(ImgFileName1))
        msg.attach(image)

        image = MIMEImage(img_data2, name=os.path.basename(ImgFileName2))
        msg.attach(image)

        image = MIMEImage(img_data3, name=os.path.basename(ImgFileName3))
        msg.attach(image)

        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.ehlo()
        s.login(gmail_user, gmail_password)
        s.sendmail(gmail_user, To, msg.as_string())
        s.quit()

# Clear the requests from the message board
sql_command = "DELETE FROM msg_board WHERE box_id = \'Cage00\'"
c.execute(sql_command)
mydb.commit()
mydb.close()

