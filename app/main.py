
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