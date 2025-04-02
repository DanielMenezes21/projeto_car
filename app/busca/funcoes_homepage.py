import os
import pandas as pd
from kivymd.uix.button import MDIconButton
import shapefile

def buscar_celula(tela_principal, instance):
    """
    Busca o conteúdo associado à célula inserida.
    """
    celula = tela_principal.car_input.text.strip()  # Obtém o texto inserido no campo de entrada
    conteudo = obter_conteudo_celula(tela_principal, celula)  # Busca o conteúdo da célula

    if conteudo:
        tela_principal.resultado.text = f"Célula: {celula}\nConteúdo:\n{conteudo}"
        coordenadas = extrair_coordenadas(tela_principal, conteudo)
        download_button = MDIconButton(
            icon='download',
            on_release=lambda x: criar_arquivos(tela_principal, coordenadas)
        )
        tela_principal.box.add_widget(download_button)
    else:
        tela_principal.resultado.text = "Célula não encontrada. Verifique o identificador."


def obter_conteudo_celula(tela_principal, celula):
    """
    Retorna o conteúdo de uma célula específica (ex: A1, A2) a partir de um arquivo Excel.
    """
    try:
        df = pd.read_excel("cordenadas_reais.xlsx")  # Substitua pelo caminho do seu arquivo Excel
        linha = int(celula[1:]) - 1
        coluna = ord(celula[0].upper()) - 65
        if linha < len(df) and coluna < len(df.columns):
            return df.iloc[linha, coluna]
        else:
            return None
    except Exception as e:
        return f"Erro ao acessar o arquivo Excel: {e}"


def extrair_coordenadas(tela_principal, conteudo):
    """
    Extrai todas as coordenadas do conteúdo da célula.
    """
    try:
        conteudo = conteudo.strip("[]")
        coordenadas = conteudo.split("), (")
        lista_coordenadas = []
        for coord in coordenadas:
            coord = coord.strip("()")
            lat, lon, alt = map(float, coord.split(","))
            lista_coordenadas.append((lat, lon, alt))
        return lista_coordenadas
    except Exception as e:
        tela_principal.resultado.text += f"\nErro ao extrair coordenadas: {e}"
        return []


def criar_arquivos(tela_principal, coordenadas):
    """
    Cria os arquivos .shp, .kml, .fix e .prj com as coordenadas fornecidas.
    """
    criar_shapefile(tela_principal, coordenadas)
    criar_kml(tela_principal, coordenadas)
    criar_fix(tela_principal, coordenadas)
    criar_prj(tela_principal)

def criar_shapefile(tela_principal, coordenadas):
    """
    Cria um shapefile com um polígono baseado nas coordenadas fornecidas.
    """
    arquivo_shp = "car_poligono.shp"
    with shapefile.Writer(arquivo_shp, shapeType=shapefile.POLYGON) as shp:
        shp.field("ID", "C")
        shp.poly([[(lon, lat) for lat, lon, _ in coordenadas]])
        shp.record("1")
    tela_principal.resultado.text += f"\nArquivo {arquivo_shp} criado com sucesso!"


def criar_kml(tela_principal, coordenadas):
    """
    Cria um arquivo .kml com um polígono baseado nas coordenadas fornecidas.
    """
    arquivo_kml = "car_poligono.kml"
    with open(arquivo_kml, "w") as kml:
        kml.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        kml.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
        kml.write("  <Document>\n")
        kml.write("    <Placemark>\n")
        kml.write("      <name>CAR Polígono</name>\n")
        kml.write("      <Polygon>\n")
        kml.write("        <outerBoundaryIs>\n")
        kml.write("          <LinearRing>\n")
        kml.write("            <coordinates>\n")
        for lat, lon, alt in coordenadas:
            kml.write(f"              {lon},{lat},{alt}\n")
        kml.write("            </coordinates>\n")
        kml.write("          </LinearRing>\n")
        kml.write("        </outerBoundaryIs>\n")
        kml.write("      </Polygon>\n")
        kml.write("    </Placemark>\n")
        kml.write("  </Document>\n")
        kml.write("</kml>\n")
    tela_principal.resultado.text += f"\nArquivo {arquivo_kml} criado com sucesso!"

    try:
        os.startfile(arquivo_kml)  # No Windows, isso abrirá o arquivo com o programa padrão
        tela_principal.resultado.text += f"\nArquivo {arquivo_kml} aberto no Google Earth Pro!"
    except Exception as e:
        tela_principal.resultado.text += f"\nErro ao abrir o arquivo {arquivo_kml}: {e}"

def criar_fix(tela_principal, coordenadas):
    """
    Cria um arquivo .FIX com as coordenadas fornecidas.
    """
    arquivo_fix = "car_poligono.fix"
    with open(arquivo_fix, "w") as fix:
        fix.write("Coordenadas do Polígono:\n")
        for lat, lon, alt in coordenadas:
            fix.write(f"{lat}, {lon}, {alt}\n")
    tela_principal.resultado.text += f"\nArquivo {arquivo_fix} criado com sucesso!"


def criar_prj(tela_principal):
    """
    Cria um arquivo .PRJ com o sistema de coordenadas WGS84.
    """
    arquivo_prj = "car_poligono.prj"
    wgs84_prj = """
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]
    """
    with open(arquivo_prj, "w") as prj:
        prj.write(wgs84_prj.strip())
    tela_principal.resultado.text += f"\nArquivo {arquivo_prj} criado com sucesso!"

def on_voltar(self, *args):
        self.manager.current = 'login'