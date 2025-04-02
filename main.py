from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, WipeTransition
from app.login.tela_login import TelaLogin
from app.busca.tela_principal import TelaPrincipal

class MainApp(MDApp):
    def build(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = 'Light'
        sm = ScreenManager(transition=WipeTransition(duration=0.5))
        sm.add_widget(TelaLogin(name='login'))
        sm.add_widget(TelaPrincipal(name='principal'))
        return sm

if __name__ == '__main__':
    MainApp().run()