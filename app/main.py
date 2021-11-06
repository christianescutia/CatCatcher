
# To run code make sure to have kivy add kivymd installed via pip or follow the links below to download and or documentation
# https://kivymd.readthedocs.io/en/latest/getting-started/
# https://kivy.org/doc/stable/gettingstarted/installation.html

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3

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
    
    def register_user(self):
        print('user registered...')
    
    def clear(self):
        print('clear data')
        self.ids.user.text = ''
        self.ids.email.text = ''
        self.ids.phone_num.text = ''
        self.ids.password.text = ''
        self.ids.password_confirm.text = ''

class InfoScreen(Screen):
    pass


# Screen Manager
sm = ScreenManager()
sm.add_widget( HomeScreen ( name = 'home_screen' ) )
sm.add_widget( LoginScreen ( name = 'login_screen' ) )
sm.add_widget( RegisterScreen ( name = 'register_screen' ) )
sm.add_widget( InfoScreen ( name = 'info_screen' ) )


class CatCatcherApp(MDApp):
    
    def build(self):
        screen = Builder.load_file('screen_manager.kv')
        return screen

CatCatcherApp().run()