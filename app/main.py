
# To run code make sure to have kivy add kivymd installed via pip or follow the links below to download and or documentation
# https://kivymd.readthedocs.io/en/latest/getting-started/
# https://kivy.org/doc/stable/gettingstarted/installation.html

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# import needed to connect to postgress server
import psycopg2
import time

# import for email messages
import smtplib

# import for sockets
import socket

# import for sms messageing
from twilio.rest import Client

# Global Values
gmail_user = 'catcatcher.noreply@gmail.com'
gmail_password = 'cat_catcher_2021'
account_sid = 'ACebaf22614c3bf1885d8bb9acf1638ab7'
auth_token = 'f54342d07240369873eddb11dfab5f25'
client = Client(account_sid, auth_token)

class HomeScreen(Screen):
    pass

class LoginScreen(Screen):
    
    def login(self):
        print('Attempting to Login...')

        # define database connection data
        conn = psycopg2.connect(
            host = "ec2-54-90-13-87.compute-1.amazonaws.com",
            database = "ddg16dt0q9df1t",
            user = "ofxriywaexambz",
            password = "15180294c0a4537da6c6cb7f5ecd6931aa138f1e2968d802268b942554828624",
            port = "5432"
        )

        # create cursor
        c = conn.cursor()

        # add user to database
        # SELECT username, pwd from Users WHERE username = 'cheraten';
        sql_command = "SELECT username, pwd FROM users WHERE username = \'" + (self.ids.user.text) +"\'"

        given_username = str(self.ids.user.text)
        given_pwd = str(self.ids.password.text)

        username_d = ''
        password_d = ''

        # executeb SQL Command
        c.execute( sql_command)

        for x in c:
            username_d = str(x[0])
            password_d = str(x[1])

        # commit changes
        conn.commit()

        # close database connection
        conn.close()

        self.ids.welcome_label.text = 'User Found'

    def clear(self):
        print('clear data')
        self.ids.user.text = ''
        self.ids.password.text = ''

class RegisterScreen(Screen):

    def SendWelcomeEmail(self):
        gmail_user = 'catcatcher.noreply@gmail.com'
        gmail_password = 'cat_catcher_2021'

        sent_from = gmail_user
        to = [self.ids.email.text]
        subject = 'Welcome to Cat Catcher'
        body = 'Welcome to Cat Catcher. This email has been registered to your account. If you feel this is a mistake contact your Admin.'

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
            print ('Something went wrong with welcome email...')
    
    def SendWelcomeSMS(self):
        # take user phone and send welcome sms message
        user_number = "+1" + self.ids.phone_num.text
        message = client.messages.create(
            body='Welcome '+ self.ids.user.text + ' to the Cat Catcher App',
            from_='+18646600650',
            to=user_number
        )

    def CheckInput(self):
        #check if all string do not have special characters
        spec_chars = '[@_!#$%^&*()<>?/.\|}{~:]'
        user_len = len(self.ids.user.text)
        email_len = len(self.ids.email.text)
        ph_num_len = len(self.ids.phone_num.text)
        pw_len = len(self.ids.password.text)

        # print out lens of all input
        print('User Input Lengths:')
        print(user_len)
        print(email_len)
        print(ph_num_len)
        print(pw_len)

        # check if fields are empty
        if user_len == 0:
            print("Error: Username cannot be empty")
            return False
        if email_len == 0:
            print("Error: email cannot be empty")
            return False
        if ph_num_len == 0:
            print("Error: phone mum cannot be empty")
            return False
        if pw_len == 0:
            print("Error: password cannot be empty")
            return False
        
        # check if all not greater than max length
        if user_len > 255:
            print("Error: Username cannot be more than 255 characters")
            return False
        if email_len > 255:
            print("Error: email cannot be more than 255 characters")
            return False
        if ph_num_len > 20:
            print("Error: phone num cannot be more than 20 numbers")
            return False
        if pw_len  > 255:
            print("Error: password cannot be more than 255 characters")
            return False
        

        
        # default response if everything passes
        return True

    def CreateUser(self):

        # define database connection data
        conn = psycopg2.connect(
            host = "ec2-54-90-13-87.compute-1.amazonaws.com",
            database = "ddg16dt0q9df1t",
            user = "ofxriywaexambz",
            password = "15180294c0a4537da6c6cb7f5ecd6931aa138f1e2968d802268b942554828624",
            port = "5432"
        )

        # create cursor
        c = conn.cursor()

        # add user to database
        sql_command = "INSERT INTO users ( username, email, phone_num, pwd) VALUES ( %s, %s, %s, %s)"
        values = (self.ids.user.text, self.ids.email.text, self.ids.phone_num.text, self.ids.password.text)

        # executeb SQL Command
        c.execute( sql_command, values)

        # commit changes
        conn.commit()

        # close database connection
        conn.close()

        print('user registered...')
    
    def register_user(self):

        # check if user input is acceptable
        if self.CheckInput():
            print('user input accepted...')
            self.CreateUser()
            self.ids.welcome_label.text = 'User Created'

            # send welcome email and text message
            self.SendWelcomeEmail()
            self.SendWelcomeSMS()

            # clear data at end
            self.clear()


        else:
            print('user input error...')
            self.ids.welcome_label.text = 'Error: '
    
    def clear(self):
        print('clear data')
        self.ids.user.text = ''
        self.ids.email.text = ''
        self.ids.phone_num.text = ''
        self.ids.password.text = ''
        self.ids.password_confirm.text = ''
    
    def reset(self):
        self.ids.welcome_label.text = 'Register'

class UserMainScreen(Screen):
    pass

class InfoScreen(Screen):
    # Screen used to Add info to contact Admin or anything Public Related
    # Left for the Client to make any additions

    def socket_test(self):
        # Create a socket object
        s = socket.socket()        
        
        # Define the port on which you want to connect
        port = 55635               
        
        conn_attempts = 0
        while True:
            try:
                # connect to the server on local computer
                s.connect(('127.0.0.1', port))
                # receive data from the server and decoding to get the string.
                print (s.recv(1024).decode())
                # close the connection
                s.close()
                break
            except:
                print("Connection Error")
                time.sleep(5)
                conn_attempts += 1
                if conn_attempts == 3:
                    break
        # end of while loop
        print('3 attempts failed... try again later')


# Screen Manager
sm = ScreenManager()
sm.add_widget( HomeScreen ( name = 'home_screen' ) )
sm.add_widget( LoginScreen ( name = 'login_screen' ) )
sm.add_widget( RegisterScreen ( name = 'register_screen' ) )
sm.add_widget( UserMainScreen ( name = 'user_main_screen' ) )
sm.add_widget( InfoScreen ( name = 'info_screen' ) )


class CatCatcherApp(MDApp):
    
    def build(self):
        screen = Builder.load_file('screen_manager.kv')
        return screen

CatCatcherApp().run()