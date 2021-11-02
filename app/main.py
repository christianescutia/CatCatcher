
# To run code make sure to have kivy add kivymd installed via pip or follow the links below to download and or documentation
# https://kivymd.readthedocs.io/en/latest/getting-started/
# https://kivy.org/doc/stable/gettingstarted/installation.html

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

"""
class LoginScreen(Screen):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_pallete = "BlueGray"
        return Builder.load_file('login.kv')

    def logger(self):
        print("Logged in Info: ")
        print("username: " + self.root.ids.user.text)
        print("password: " + self.root.ids.password.text)
        print("password-confirm: " + self.root.ids.password_confirm.text)

        # check if both passwords are the same
        #if( self.root.ids.password.text == self.root.ids.password_confirm.text):
            #print("password check passed...")
        #else:
            #print("password check failed...")
        
        # end of logger
        pass

    def clear(self):
        #self.LoginApp.ids.user.text = ""
        #self.LoginApp.ids.password.text = ""
        pass

class HomeScreen(Screen):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_pallete = "BlueGray"
        return Builder.load_file('home.kv')

    def login(self):
        print("Login Button Pressed...")
        pass
    
    def register(self):
        print("Register Button Pressed...")
        pass
    
    def info(self):
        print("Info Button Pressed...")
        pass
"""


screen_helper = """

ScreenManager:
    HomeScreen:
    LoginScreen:
    RegisterScreen:
    InfoScreen:

<HomeScreen>:
    name: "home_screen"
    MDCard:
        size_hint: None, None
        size: 600, 800
        pos_hint: { "center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 50
        spacing: 50
        orientation: "vertical"

        MDIcon:
            id: app_icon
            icon: "cat"
            font_size: 140
            padding_x: 175
    
        MDLabel:
            id: welcome_label
            text: "Welcome to Cat Catcher"
            font_size: 80
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 20

        MDRoundFlatButton:
            text: 'Login'
            font_size: 24
            pos_hint: { "center_x": 0.5 }
            on_press: root.manager.current = 'login_screen'

        MDRoundFlatButton:
            text: 'Register'
            font_size: 24
            pos_hint: { "center_x": 0.5 }
            on_press: root.manager.current = 'register_screen'
        
        MDRoundFlatButton:
            text: 'Info'
            font_size: 24
            pos_hint: { "center_x": 0.5 }
            on_press: root.manager.current = 'info_screen'

<LoginScreen>:
    name: "login_screen"
    MDCard:
        size_hint: None, None
        size: 600, 800
        pos_hint: { "center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 50
        spacing: 50
        orientation: "vertical"

        MDIcon:
            id: app_icon
            icon: "cat"
            font_size: 140
            padding_x: 175
    
        MDLabel:
            id: welcome_label
            text: "Login"
            font_size: 80
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 20
    
        MDTextFieldRound:
            id: user
            hint_text: "username"
            icon_right: "account"
            size_hint_x: None
            width: 400
            font_size: 32
            pos_hint: { "center_x": 0.5 }

        MDTextFieldRound:
            id: password
            hint_text: "password"
            icon_right: "eye-off"
            size_hint_x: None
            width: 400
            font_size: 32
            pos_hint: { "center_x": 0.5 }
            password: True

        MDRoundFlatButton:
            text: 'Login'
            font_size: 24
            pos_hint: { "center_x": 0.5 }
        
        MDRoundFlatButton:
            text: 'Clear'
            font_size: 24
            pos_hint: { "center_x": 0.5 }
        
        MDRoundFlatButton:
            text: 'Back'
            font_size: 24
            pos_hint: { "center_x": 0.5 }
            on_press: root.manager.current = 'home_screen'

<RegisterScreen>:
    name: "register_screen"
    MDCard:
        size_hint: None, None
        size: 600, 800
        pos_hint: { "center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 50
        spacing: 50
        orientation: "vertical"

        MDIcon:
            id: app_icon
            icon: "cat"
            font_size: 140
            padding_x: 175
    
        MDLabel:
            id: welcome_label
            text: "Register"
            font_size: 80
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 20
    
        MDTextFieldRound:
            id: user
            hint_text: "username"
            icon_right: "account"
            size_hint_x: None
            width: 400
            font_size: 32
            pos_hint: { "center_x": 0.5 }

        MDTextFieldRound:
            id: password
            hint_text: "password"
            icon_right: "eye-off"
            size_hint_x: None
            width: 400
            font_size: 32
            pos_hint: { "center_x": 0.5 }
            password: True
        
        MDTextFieldRound:
            id: password_confirm
            hint_text: "password"
            icon_right: "eye-off"
            size_hint_x: None
            width: 400
            font_size: 32
            pos_hint: { "center_x": 0.5 }
            password: True

        MDRoundFlatButton:
            text: 'Register'
            font_size: 24
            pos_hint: { "center_x": 0.5 }
        
        MDRoundFlatButton:
            text: 'Clear'
            font_size: 24
            pos_hint: { "center_x": 0.5 }
        
        MDRoundFlatButton:
            text: 'Back'
            font_size: 24
            pos_hint: { "center_x": 0.5 }
            on_press: root.manager.current = 'home_screen'

<InfoScreen>:
    name: "info_screen"
    MDCard:
        size_hint: None, None
        size: 600, 800
        pos_hint: { "center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 50
        spacing: 50
        orientation: "vertical"

        MDIcon:
            id: app_icon
            icon: "cat"
            font_size: 140
            padding_x: 175
        
        MDRoundFlatButton:
            text: 'Home'
            font_size: 24
            pos_hint: { "center_x": 0.5 }
            on_press: root.manager.current = 'home_screen'
"""

class HomeScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

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
        screen = Builder.load_string(screen_helper)
        return screen

CatCatcherApp().run()