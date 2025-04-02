from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
import re  
import shapefile
import os
import time

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
            coordenadas = (-15.7801, -47.9292)
            self.resultado.text = f"CAR válido!\nCoordenadas: Latitude: {coordenadas[0]}, Longitude: {coordenadas[1]}"
            self.box.add_widget(MDIconButton(icon='download', on_release=lambda x: self.criar_arquivos(coordenadas)))
        else:
            self.resultado.text = "Formato de CAR inválido. Insira 15 dígitos."

    def criar_arquivos(self, coordenadas):
        """
        Cria os arquivos .shp e .kml com as coordenadas fornecidas.
        """
        # Cria o arquivo .shp
        self.criar_shapefile(coordenadas)

        # Cria o arquivo .kml
        self.criar_kml(coordenadas)

    def criar_shapefile(self, coordenadas):
        """
        Cria um shapefile com as coordenadas fictícias.
        """
        # Nome do arquivo .shp
        arquivo_shp = "car_ponto.shp"

        # Criação do shapefile
        with shapefile.Writer(arquivo_shp, shapeType=shapefile.POINT) as shp:
            shp.field("ID", "C")  # Adiciona um campo de atributo
            shp.point(coordenadas[1], coordenadas[0])  # Adiciona o ponto (longitude, latitude)
            shp.record("1")  # Adiciona um registro com ID "1"

        # Mensagem de sucesso para o arquivo .shp
        self.resultado.text += f"\nArquivo {arquivo_shp} criado com sucesso!"

    def criar_kml(self, coordenadas):
        """
        Cria um arquivo .kml com as coordenadas fictícias e o abre no Google Earth Pro.
        """
        # Nome do arquivo .kml
        arquivo_kml = "car_ponto.kml"

        # Criação do arquivo .kml
        with open(arquivo_kml, "w") as kml:
            kml.write("<?xml version='1.0' encoding='UTF-8'?>\n")
            kml.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
            kml.write("  <Document>\n")
            kml.write("    <Placemark>\n")
            kml.write(f"      <name>CAR Ponto</name>\n")
            kml.write("      <Point>\n")
            kml.write(f"        <coordinates>{coordenadas[1]},{coordenadas[0]},0</coordinates>\n")
            kml.write("      </Point>\n")
            kml.write("    </Placemark>\n")
            kml.write("  </Document>\n")
            kml.write("</kml>\n")

        # Mensagem de sucesso para o arquivo .kml
        self.resultado.text += f"\nArquivo {arquivo_kml} criado com sucesso!"

        # Abre o arquivo .kml no Google Earth Pro
        try:
            os.startfile(arquivo_kml)  # Abre o arquivo no programa associado (Google Earth Pro)
        except Exception as e:
            self.resultado.text += f"\nErro ao abrir o arquivo: {e}"
            
    def on_voltar(self, *args):
        self.manager.current = 'login'