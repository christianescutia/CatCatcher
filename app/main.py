
# To run code make sure to have kivy add kivymd installed via pip or follow the links below to download and or documentation
# https://kivymd.readthedocs.io/en/latest/getting-started/
# https://kivy.org/doc/stable/gettingstarted/installation.html

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# import needed to connect to postgress server
import psycopg2

class HomeScreen(Screen):
    pass

class LoginScreen(Screen):
    
    def login(self):
        print('logging in user...')

    def clear(self):
        print('clear data')
        self.ids.user.text = ''
        self.ids.password.text = ''

class RegisterScreen(Screen):

    def CheckInput(self):
        #check if all string do not have special characters
        spec_chars = '[@_!#$%^&*()<>?/.\|}{~:]'
        ph_num_len = len(self.ids.phone_num.text)
        user_len = len(self.ids.user.text)
        email_len = len(self.ids.email.text)
        pw_len = len(self.ids.password.text)

        if user_len == 0: #check username text not empty
            print("Error: Username cannot be empty")
            return False
        
        if user_len > 255: #check username text max 255
            print("Error: Username exceeds max length")
            return False
        
        #check email check proper format, contains email handle, one @, one . one extension max 255
        if '@' not in self.ids.email.text or '.' not in self.ids.email.text:
            print("Error: Invalid email format")
            return False
        else:
            if email_len  < 5: #min valid: a@b.c - len 5
                print("Error: Email too short")
                return False
            elif email_len > 255:
                print("Error: Email too long")
                return False

            if self.ids.email.text.count('@') != 1 or self.ids.email.text.count('.') != 1:
                print('Error: Invalid number of \'@\' or \'.\' in email')
                return False
            
            at_i = self.ids.email.text.find('@')
            period_i = self.ids.email.text.find('.')
            if at_i == 0:
                print('Error: No email username')
                return False
            elif period_i == at_i +1:
                print('Error: No email domain name')
                return False
            elif period_i == len(self.ids.email.text) -1:
                print('Error: No email domain')
                return False
                

        if ph_num_len < 9: #check phone number 9 digits, possibly 10 for international code (max 20)
            print("Error: Phone number too short")
            return False

        if ph_num_len <= 20:
            if ph_num_len == 10 and self.ids.phone_num.text[0] != '1':
                print("Error: Invalid country code")
                return False
            elif ph_num_len != 9: #invalid phone number
                print("Error: Invalid phone number length")
                return False
        else:
            print("Error: Phone number exceeds max length")
            return False
        
        for number in self.ids.phone_num.text:
            if number.isalpha():
                print("Error: Phone number cannot contain alphabetical characters")

        if pw_len < 8:
            print("Error: Password must be at least 8 characters long")
            return False
        elif pw_len > 255:
            print("Error: Password must be less than 256 characters long")
            return False

        if self.ids.password.text != self.ids.password_confirm.text:
            print("Error: Password does not match confirmation password")

        for spec in spec_chars:
            if spec in self.ids.user.text:
                print("Error: Username cannot contain special characters")
                return False
            if spec in self.ids.phone_num.text:
                print("Error: Phone number cannot contain special characters")
                return False
            if spec in self.ids.email.text:
                if spec != '@' and spec != '.':
                    print('Error: Email cannot contain special characters')
                    return False
            if spec in self.ids.password.text:
                print("Error: Password cannot contain special characters")
                return False

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
        sql_command = "INSERT INTO users (id, username, email, phone_num, password) VALUES (%s, %s, %s, %s, %s)"
        values = ( '1', self.ids.user.text, self.ids.email.text, self.ids.phone_num.text, self.ids.password.text)

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

        else:
            print('user input error...')
    
    def clear(self):
        print('clear data')
        self.ids.user.text = ''
        self.ids.email.text = ''
        self.ids.phone_num.text = ''
        self.ids.password.text = ''
        self.ids.password_confirm.text = ''

class RegisterScreenVerification(Screen):
    pass

class InfoScreen(Screen):
    pass


# Screen Manager
sm = ScreenManager()
sm.add_widget( HomeScreen ( name = 'home_screen' ) )
sm.add_widget( LoginScreen ( name = 'login_screen' ) )
sm.add_widget( RegisterScreen ( name = 'register_screen' ) )
sm.add_widget( RegisterScreenVerification ( name = 'register_screen_verification' ) )
sm.add_widget( InfoScreen ( name = 'info_screen' ) )


class CatCatcherApp(MDApp):
    
    def build(self):
        screen = Builder.load_file('screen_manager.kv')
        return screen

CatCatcherApp().run()