from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
import re  

class TelaPrincipal(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.box = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        self.add_widget(self.box)

        self.box.add_widget(MDLabel(text='Busca', halign='center'))
        self.car_input = TextInput(
            hint_text='Digite o CAR desejado',
            size_hint=(0.8, 0.12),
            pos_hint={"center_x": 0.5},
            multiline=False
        )
        self.car_input.bind(on_text_validate=self.validar_car)
        self.box.add_widget(self.car_input)

        self.resultado = TextInput(
            hint_text='Coordenadas',
            size_hint=(0.8, 0.12),
            pos_hint={"center_x": 0.5},
            multiline=True,
            readonly=True
        )
        self.box.add_widget(self.resultado)

        self.box.add_widget(MDIconButton(text='Voltar', icon='arrow-left', on_release=self.on_voltar))

    def validar_car(self, instance):
        """
        Valida o formato do CAR federal e exibe coordenadas fictícias.
        """
        texto = self.car_input.text
        if texto:
            coordenadas = "Latitude: -15.7801, Longitude: -47.9292"
            self.resultado.text = f"CAR válido!\nCoordenadas: {coordenadas}"
            self.box.add_widget(MDIconButton(icon='download', on_release=self.on_enter))
        else:
            self.resultado.text = "Formato de CAR inválido. Insira 15 dígitos."

    def on_voltar(self, *args):
        self.manager.current = 'login'