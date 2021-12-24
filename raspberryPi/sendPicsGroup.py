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

# Global Variables
gmail_user = 'catcatcher.noreply@gmail.com'
gmail_password = 'cat_catcher_2021'
ImgFileName1 = "/home/pi/rightImage.jpg"
ImgFileName2 = "/home/pi/middleImage.jpg"
ImgFileName3 = "/home/pi/leftImage.jpg"
client = Client('','')

with open(ImgFileName3, 'rb') as f:
    img_data3 = f.read()

with open(ImgFileName2, 'rb') as f:
    img_data2 = f.read()

with open(ImgFileName1, 'rb') as f:
    img_data1 = f.read()

# Connect to sql server
mydb = mysql.connector.connect(
    host='us-cdbr-east-04.cleardb.com',
    user='',
    password='',
    database= ''
)

# Create cursor
c = mydb.cursor()

sql_command = "SELECT username FROM notify_list WHERE box_id = \'Cage00\'"

c.execute(sql_command)

notify_list = []

# Find all users that are registered to reviece notifications
for x in c:
    str_u = str(x)
    length = len(str_u)
    sliced = str_u[2:length-3]
    notify_list.append(sliced)
    print("User " + sliced + " is registered to revceive emails")

# Email all the registered users the images
for x in notify_list:
    sql_command = "SELECT email FROM users WHERE username = \'" + x + "\'"
    c.execute(sql_command)
    for x in c:
        str_u = str(x)
        length = len(str_u)
        sliced = str_u[2:length-3]
        print("Emailing " + sliced)
        msg = MIMEMultipart()
        msg['Subject'] = 'Cat Catcher Cage00 was Tripped'
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

# Text all registered users notifying them that the cage was triggered
for x in notify_list:
    sql_command = "SELECT phone_num FROM users WHERE username = \'" + x + "\'"
    c.execute(sql_command)
    for x in c:
        str_u = str(x)
        length = len(str_u)
        sliced = str_u[2:length-3]
        print(sliced)
        user_number = "+1" + sliced
        message = client.messages.create(
            body = "Cat Catcher Cage00 was tripped. Check your email for photos.",
            from_ = "",
            to = user_number
        )


mydb.close()

