
# To run code make sure to have kivy add kivymd installed via pip or follow the links below to download and or documentation
# https://kivymd.readthedocs.io/en/latest/getting-started/
# https://kivy.org/doc/stable/gettingstarted/installation.html

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import ScreenManager, Screen

# import needed to connect to SQL server
import mysql.connector

# import for email messages
import smtplib

# import for sms messageing
from twilio.rest import Client

# Global Values
# Items needed to send SMS and Email to users as needed
# needed for email responses
gmail_user = ''
gmail_password = ''
# needed for postgres access
account_sid = ''
auth_token = ''
database = ''
error_msg = ''
# needed for Twilio SMS access
client = Client('','')

current_user = ''
registered_cages = 0
current_cage = ''

class HomeScreen(Screen):
    # Screen for home screen - this is meant to stay empty unless need to add additonal functionality at runtime
    pass

class LoginScreen(Screen):
    # Screen used to allow user to login to gain access to backend functions

    def login(self):
        print('Attempting to Login...')
        global current_user

        # check if input is empty
        if len(self.ids.user.text) == 0:
            print('empty username')
            self.ids.error_label.text = 'username is empty'
            return False
        
        if len(self.ids.password.text) == 0:
            print('empty username')
            self.ids.error_label.text = 'password is empty'
            return False

        # define database connection data
        mydb = mysql.connector.connect(
            host='us-cdbr-east-04.cleardb.com',
            user=account_sid,
            password=auth_token,
            database= database
        )

        # create cursor
        mycursor = mydb.cursor()

        sql_command = "SELECT username, pwd FROM users WHERE username = \'" + self.ids.user.text + "\' AND pwd = \'" + self.ids.password.text + "\'"

        # check if user and password match is taken
        mycursor.execute( sql_command )

        isEmpty = 0

        for x in mycursor:
            isEmpty +=1
        
        # close database connection
        mydb.close()

        if isEmpty == 0:
            print('user not found')
            self.ids.error_label.text = 'User Doesn\'t Exist or Password is Incorrect'
            return False
        else:
            print('user found')
            current_user = self.ids.user.text
            print('Logging in as user: ' + current_user)
            return True

        print('Got to End of User Login - Bad Error')
        return False

    def clear(self):
        print('clear data')
        self.ids.error_label.text = '  '
        self.ids.user.text = ''
        self.ids.password.text = ''

class RegisterScreen(Screen):
    # Screen used to register user, function below check user input and register the user to the database


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

    def UserCheck(self):
        # define database connection data
        mydb = mysql.connector.connect(
            host='us-cdbr-east-04.cleardb.com',
            user=account_sid,
            password=auth_token,
            database= database
        )

        # create cursor
        mycursor = mydb.cursor()

        username = self.ids.user.text
        phone_number = self.ids.phone_num.text
        email = self.ids.email.text

        # grab data from the database
        sql_command_username = "SELECT username FROM users"
        sql_command_email = "SELECT email FROM users"
        sql_command_phone = "SELECT phone_num FROM users"

        # check if username is taken
        mycursor.execute(sql_command_username)

        for x in mycursor:
            #print(x)
            # check if user matches
            str_u = str(x)
            length = len(str_u)
            sliced = str_u[2:length-3]
            #print(sliced)

            if sliced == username:
                print('user already exits')
                error_msg = 'username taken'
                mydb.close() # close database connection
                return False
        
        # check if email is taken
        mycursor.execute( sql_command_email)

        for x in mycursor:
            #print(x)
            # check if email matches
            str_u = str(x)
            length = len(str_u)
            sliced = str_u[2:length-3]
            #print(sliced)

            if sliced == email:
                print('email already taken')
                error_msg = 'email taken'
                mydb.close() # close database connection
                return False
        
        # check if phone is taken
        mycursor.execute( sql_command_phone)

        for x in mycursor:
            #print(x)
            # check if phone_num matches
            str_u = str(x)
            length = len(str_u)
            sliced = str_u[2:length-3]
            #print(sliced)

            if sliced == phone_number:
                print('phone number already taken')
                error_msg = 'phone number taken'
                mydb.close() # close database connection
                return False

        # close database connection
        mydb.close()
        # Assumes if got here username, email and phonenum are avaiable
        return True

    def CheckInput(self):
        #check if all string do not have special characters
        spec_chars = '[@_!#$%^&*()<>?/.\|}{~:]'
        user_len = len(self.ids.user.text)
        email_len = len(self.ids.email.text)
        ph_num_len = len(self.ids.phone_num.text)
        pw_len = len(self.ids.password.text)
        pwc_len = len(self.ids.password_confirm.text)
        global error_msg

        # print out lens of all input
        print('User Input Lengths:')
        print(user_len)
        print(email_len)
        print(ph_num_len)
        print(pw_len)
        print(pwc_len)

        # check if fields are empty
        if user_len == 0:
            print("Error: Username cannot be empty")
            error_msg = 'user empty'
            return False
        if email_len == 0:
            print("Error: email cannot be empty")
            error_msg = 'email empty'
            return False
        if ph_num_len == 0:
            print("Error: phone mum cannot be empty")
            error_msg = 'phone empty'
            return False
        if pw_len == 0:
            error_msg = 'password empty'
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

        # check if passwords match and minimal length
        if pw_len < 8:
            error_msg = 'password to short, 8 or more'
            print("Error: password cannot be less then 8 characters")
            return False
        
        if self.ids.password.text != self.ids.password_confirm.text:
            error_msg = 'passwords don\'t match'
            print("Error: passwords must match")
            return False

        
        # Check if user already exits
        if self.UserCheck() == False:
            return False

        
        # default response if everything passes
        return True

    def CreateUser(self):

        # define database connection data
        mydb = mysql.connector.connect(
            host='us-cdbr-east-04.cleardb.com',
            user=account_sid,
            password=auth_token,
            database= database
        )

        # create cursor
        mycursor = mydb.cursor()

        # add user to database
        sql_command = "INSERT INTO users ( username, email, phone_num, pwd) VALUES ( %s, %s, %s, %s)"
        values = (self.ids.user.text, self.ids.email.text, self.ids.phone_num.text, self.ids.password.text)

        # executeb SQL Command
        mycursor.execute(sql_command, values)

        # commit changes
        mydb.commit()

        # close database connection
        mydb.close()

        print('user registered...')

    def register_user(self):

        # check if user input is acceptable
        if self.CheckInput():
            print('user input accepted...')
            self.CreateUser()
            self.ids.error_label.text = 'User Created'

            # send welcome email and text message
            self.SendWelcomeEmail()
            self.SendWelcomeSMS()

            # clear data at end
            self.clear()

        else:
            global error_msg
            print('user input error...')
            self.ids.error_label.text = 'Error: ' + str(error_msg)
            error_msg = ''
    
    def clear(self):
        print('clear data')
        self.ids.user.text = ''
        self.ids.email.text = ''
        self.ids.phone_num.text = ''
        self.ids.password.text = ''
        self.ids.password_confirm.text = ''
    
    def reset(self):
        self.ids.error_label.text = '   '

class UserMainScreen(Screen):
    # Screen used to allow user to query active boxes, delete user account or logout

    def test(self):
        print('Testing')
        pass

    def logout(self):
        current_user = ''
        global registered_cages
        registered_cages = 0
        print('user logged out and reset main')
    
    def refresh(self):
        global registered_cages
        global current_user
        cageList = []
        mydb = mysql.connector.connect(
            host='us-cdbr-east-04.cleardb.com',
            user=account_sid,
            password=auth_token,
            database= database
        )

        # create cursor
        mycursor = mydb.cursor()

        # grab all cages user is registered for
        sql_command = "SELECT box_id FROM notify_list WHERE username =\'" +current_user+ "\'"
        mycursor.execute( sql_command)

        for x in mycursor:
            str_u = str(x)
            length = len(str_u)
            sliced = str_u[2:length-3]
            cageList.append(sliced)
        
        print("List Made")
        for x in cageList:
            print(x)

        # grab all cage ID's
        sql_command = "SELECT cage_id from cages"
        mycursor.execute( sql_command)

        # clear previous refresh
        self.ids.cage_container.clear_widgets()

        for x in mycursor:
            registered_cages +=1
            str_u = str(x)
            length = len(str_u)
            sliced = str_u[2:length-3]
            cage_found = False
            for y in cageList:
                if y == sliced:
                    cage_found = True
                    print('Cage Matched!')
                    break
            
            if cage_found:
                self.ids.cage_container.add_widget(
                    OneLineListItem(text=sliced + " - Notifications On")
                )
            else:
                self.ids.cage_container.add_widget(
                    OneLineListItem(text=sliced)
                )

        if registered_cages == 0:
            print('cages not found - refresh')
        else:
            print('cage found - refresh')

        # close database connection
        mydb.close()

class UserInfoScreen(Screen):
    
    def delete_user(self):
        print('delete user')
        global current_user
        # define database connection data
        mydb = mysql.connector.connect(
            host='us-cdbr-east-04.cleardb.com',
            user=account_sid,
            password=auth_token,
            database= database
        )

        # create cursor
        mycursor = mydb.cursor()

        # add user to database
        sql_command = "DELETE FROM users WHERE username = \'"+current_user+"\'"

        # executeb SQL Command
        mycursor.execute(sql_command)

        # commit changes
        mydb.commit()

        # close database connection
        mydb.close()

        print('user deleted...')
    pass

class UserDeleteConfirmation(Screen):
    pass

class NotificationsScreen(Screen):

    def NotifyToggle(self):
        print('User Toggle for Cage: ' + self.ids.box_id_1.text)

        # define database connection data
        mydb = mysql.connector.connect(
            host='us-cdbr-east-04.cleardb.com',
            user=account_sid,
            password=auth_token,
            database= database
        )

        try:
            global current_user
            matchFound = False
            # Attempt to find if Notify exists, if True then Delete, else Create

            # create cursor
            mycursor = mydb.cursor()

            # add user to database
            sql_command = "SELECT * FROM notify_list WHERE username = \'"+current_user+"\' AND box_id = \'"+self.ids.box_id_1.text+"\'"

            # executeb SQL Command
            mycursor.execute(sql_command)

            for x in mycursor:
                matchFound = True
            
            print('Checking After Match Found')
            
            if matchFound:
                # delete from database notify list
                sql_command = "DELETE FROM notify_list WHERE username = \'"+current_user+"\' AND box_id = \'"+self.ids.box_id_1.text+"\'"

                # executeb SQL Command
                mycursor.execute(sql_command)

                # commit changes
                mydb.commit()
            else:
                # Add to Notify List
                sql_command = "INSERT INTO notify_list ( box_id, username) VALUES ( %s, %s)"
                values = (self.ids.box_id_1.text, current_user)

                # executeb SQL Command
                mycursor.execute(sql_command, values)

                # commit changes
                mydb.commit()

        except:
            print("An exception occurred")
            self.ids.msg_label.text = 'Cage Not Found'

        self.ids.box_id_1.text = ''
        # close database connection
        mydb.close()
    
    def InstaReport(self):
        print('Insta Report')

        try:
            matchFound = False

             # define database connection data
            mydb = mysql.connector.connect(
                host='us-cdbr-east-04.cleardb.com',
                user=account_sid,
                password=auth_token,
                database= database
            )

            # create cursor
            mycursor = mydb.cursor()

            # add user to database
            sql_command = "SELECT * FROM cages WHERE cage_id = \'"+self.ids.box_id_2.text+"\'"

            # executeb SQL Command
            mycursor.execute(sql_command)

            for x in mycursor:
                matchFound = True
            
            if matchFound:
                # if true cage exits and send request else deny
                sql_command = "INSERT INTO msg_board ( box_id, username) VALUES ( %s, %s)"
                values = (self.ids.box_id_2.text, current_user)
                # executeb SQL Command
                mycursor.execute(sql_command,values)
                # commit changes
                mydb.commit()
            else:
                print('Cage Doesn\'t exists so notify user')
        except:
            print("An exception occurred")

        self.ids.box_id_2.text = ''

class InfoScreen(Screen):
    # Screen used to Add info to contact Admin or anything Public Related
    # Left for the Client to make any additions
    pass


# Screen Manager - used to register screens to allow for transition between them all
sm = ScreenManager()
sm.add_widget( HomeScreen ( name = 'home_screen' ) )
sm.add_widget( LoginScreen ( name = 'login_screen' ) )
sm.add_widget( RegisterScreen ( name = 'register_screen' ) )
sm.add_widget( UserMainScreen ( name = 'user_main_screen' ) )
sm.add_widget( UserInfoScreen ( name = 'user_info_screen' ) )
sm.add_widget( UserDeleteConfirmation ( name = 'user_delete_confirmation_screen' ) )
sm.add_widget( NotificationsScreen ( name = 'notifications_screen') )
sm.add_widget( InfoScreen ( name = 'info_screen' ) )


# Main run script for the app loads from screen_manager file to determine how app looks.
class CatCatcherApp(MDApp):
    
    def build(self):
        screen = Builder.load_file('screen_manager.kv')
        return screen

CatCatcherApp().run()
