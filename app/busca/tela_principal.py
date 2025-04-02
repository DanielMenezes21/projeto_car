from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
import shapefile
import os
import pandas as pd
from app.busca.funcoes_homepage import buscar_celula, on_voltar, criar_arquivos

class TelaPrincipal(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.box = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        self.add_widget(self.box)

        # Campo de entrada para a célula
        self.box.add_widget(MDLabel(text='Busca', halign='center'))
        self.car_input = TextInput(
            hint_text='Digite a célula desejada (ex: A1, A2)',
            size_hint=(0.8, 0.12),
            pos_hint={"center_x": 0.5},
            multiline=False
        )
        self.car_input.bind(on_text_validate=lambda x: buscar_celula(self, x))
        self.box.add_widget(self.car_input)

        # Campo de saída para exibir as coordenadas
        self.resultado = TextInput(
            hint_text='Coordenadas',
            size_hint=(0.8, 0.12),
            pos_hint={"center_x": 0.5},
            multiline=True,
            readonly=True
        )
        self.box.add_widget(self.resultado)

        self.box.add_widget(MDIconButton(text='Voltar', icon='arrow-left', on_release=lambda x: on_voltar(self, x)))
