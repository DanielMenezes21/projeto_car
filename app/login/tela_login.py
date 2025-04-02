import sqlite3
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDExtendedFabButtonIcon, MDButtonIcon, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialogIcon
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class TelaLogin(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        box.add_widget(MDLabel(text='Login', halign='center'))

        self.username_field = TextInput(
            hint_text='Usuário',
            size_hint=(0.8, 0.12),
            write_tab=False,
            pos_hint={"center_x": 0.5}
        )
        box.add_widget(self.username_field)

        self.password_field = TextInput(
            hint_text='Senha',
            password=True,
            write_tab=False,
            size_hint=(0.8, 0.12),
            pos_hint={"center_x": 0.5}
        )
        box.add_widget(self.password_field)

        fab_button = MDButton(
            MDButtonIcon(
                icon="login",
                theme_icon_color="Custom",
                icon_color=(1, 1, 1, 1),
            ),
            MDButtonText(
                text="Entrar",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
            ),
            theme_bg_color="Custom",
            md_bg_color=(0,0,0, 1),
            pos_hint={"center_x": 0.1, "center_y": 0.1},
            size_hint=(0.8, 0.12),
            on_release=self.on_login
        )
        box.add_widget(fab_button)

        self.add_widget(box)

    def on_login(self, *args):
        username = self.username_field.text
        password = self.password_field.text

        conn = sqlite3.connect('database/database_login.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM login WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            self.manager.current = 'principal'
        else:
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            content.add_widget(Label(text="Usuário ou senha incorretos."))

            close_button = Button(text="Fechar", size_hint=(1, 0.3))
            content.add_widget(close_button)

            popup = Popup(
                title="Erro de Login",
                content=content,
                size_hint=(0.8, 0.4),
                auto_dismiss=False
            )
            close_button.bind(on_release=popup.dismiss)
            popup.open()

        conn.close()