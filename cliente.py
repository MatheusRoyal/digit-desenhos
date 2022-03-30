from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import lib.cliente_gui as clt
from functools import partial
import subprocess
Window.size = (400, 300)

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    GridLayout:
        cols: 2
        row_force_default: True
        row_default_height: 40
        Label:
            text: 'Usuário'
        TextInput:
            id: usuario
            multiline: False
            write_tab: False
        Label:
            text: 'Senha'
        TextInput:
            id: senha
            multiline: False
            write_tab: False
            password: True
        Label:
            text: ''
        Button:
            id: entrar
            text: 'Entrar'


<SettingsScreen>:
    GridLayout:
        cols: 2
        row_force_default: True
        row_default_height: 40
        Label:
            text: 'N° desenho'
        TextInput:
            id: codigo
            hint_text: '000000.000'
            multiline: False
        Label:
            text: ''
        Button:
            text: 'Requisitar desenho'
            on_press: root.pegar_pdf()

""")

            #on_press: root.entrado
def erro_popup(msg: str):
    popup = Popup(title='Erro',
        content=Label(text=msg),
        size_hint=(None, None), size=(250, 150))
    popup.bind(on_key_down=popup.dismiss)
    return popup

# Declare both screens
class MenuScreen(Screen):

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.ids.entrar.bind(on_press=self.get_info)


    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40 or keycode == 88: # 40 - Enter key pressed, 88 - Tab key pressed
            if self.ids.senha.focus:
                self.get_info()
            elif self.ids.usuario.focus:
                self.ids.senha.focus = True

    def get_info(self, *args):
        global user, pword
        user = self.ids.usuario.text
        pword = self.ids.senha.text
        self.entrado()

    def entrado(self, *args):
        print('pressionado')
        global connection, cipher
        try:
            connection, cipher = clt.connect_serv()
        except:
            popup = erro_popup('Não foi possível conectar ao servidor')
            popup.open()
            return
        result = clt.cred(cipher, user, pword, connection)
        if not result:
            popup = erro_popup('Usuário não encontrado')
            popup.open()
            connection.close()
            print('voltando')
        else:
            self.manager.current = 'settings'

    def on_parent(self, widget, parent):
        self.ids.usuario.focus = True

    pass

class SettingsScreen(Screen):

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

    def pegar_pdf(self):
        cod = self.ids.codigo.text
        if connection.fileno() == -1:
            MenuScreen.entrado(self)
        busca = clt.get_pdf(cipher, cod, connection)
        if busca != b'nada':
            cod = busca.decode()
            temp = "\\\\192.168.254.246\\Dados\\Publico\\Manutenção\\Temp\\" + cod
            subprocess.Popen([temp], shell=True)
            connection.close()
            #App.get_running_app().stop()
        else:
            popup = erro_popup("PDF não encontrado")
            popup.open()

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.ids.codigo.focus and (keycode == 40 or keycode == 88):  # 40 - Enter key pressed
            self.pegar_pdf()

    def on_enter(self):
        self.ids.codigo.focus = True

    pass

#class ErroPopup(Popup):

#    def __init__(self, **kwargs):
#        super(ErroPopup, self).__init__(**kwargs)
#        Window.bind(on_key_down=self._on_keyboard_down)

#    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
#        self.close()

class TestApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm

if __name__ == '__main__':
    TestApp().run()
#
# class UserApp(App):
#     def entrado(self, cipher, connection, entrar):
#         user = self.usuario.text
#         pword = self.senha.text
#         clt.cred(cipher, user, pword, connection)
#
#     def build(self):
#         layout = GridLayout(cols=2, row_force_default=True, row_default_height=40)
#         lab_usuario = Label(text = "Usuário")
#         self.usuario = TextInput(multiline = False, \
#             width = 20, \
#             write_tab = False)
#         lab_senha = Label(text = "Senha")
#         self.senha = TextInput(multiline = False, \
#             width = 20, \
#             password = True, \
#             write_tab = False)
#         lab_empty = Label(text = "")
#         self.entrar = Button(text = "Entrar")
#         layout.add_widget(lab_usuario)
#         layout.add_widget(self.usuario)
#         layout.add_widget(lab_senha)
#         layout.add_widget(self.senha)
#         layout.add_widget(lab_empty)
#         layout.add_widget(self.entrar)
#         connection, cipher = clt.connect_serv()
#         self.entrar.bind(on_press=partial(self.entrado, cipher, connection))
#         return layout
#
#
# if __name__ == '__main__':
#     UserApp().run()

#===============================================================================

# from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.uix.textinput import TextInput
# from kivy.uix.label import Label
# from kivy.uix.gridlayout import GridLayout
# from kivy.core.window import Window
# from kivy.uix.button import Button
# import cliente_gui as clt
# from functools import partial
# Window.size = (300, 120)
#
# class UserApp(App):
#     def entrado(self, cipher, connection, entrar):
#         user = self.usuario.text
#         pword = self.senha.text
#         clt.cred(cipher, user, pword, connection)
#
#     def build(self):
#         layout = GridLayout(cols=2, row_force_default=True, row_default_height=40)
#         lab_usuario = Label(text = "Usuário")
#         self.usuario = TextInput(multiline = False, \
#             width = 20, \
#             write_tab = False)
#         lab_senha = Label(text = "Senha")
#         self.senha = TextInput(multiline = False, \
#             width = 20, \
#             password = True, \
#             write_tab = False)
#         lab_empty = Label(text = "")
#         self.entrar = Button(text = "Entrar")
#         layout.add_widget(lab_usuario)
#         layout.add_widget(self.usuario)
#         layout.add_widget(lab_senha)
#         layout.add_widget(self.senha)
#         layout.add_widget(lab_empty)
#         layout.add_widget(self.entrar)
#         connection, cipher = clt.connect_serv()
#         self.entrar.bind(on_press=partial(self.entrado, cipher, connection))
#         return layout
#
#
# if __name__ == '__main__':
#     UserApp().run()
