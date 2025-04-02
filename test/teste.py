from kivy.lang import Builder
from kivymd.app import MDApp

KV = '''
MDScreen:
    canvas.before:
        Color:
            rgba: 0, 0.5, 0, 1  # Cor verde (RGBA)
        Rectangle:
            size: self.size
            pos: self.pos

    MDExtendedFabButton:
        id: btn
        pos_hint: {"center_x": .5, "center_y": .5}
        fab_state: "collapse"
        on_touch_down:
            if not self.collide_point(*args[1].pos): \
            self.fab_state = "expand" \
            if self.fab_state == "collapse" else "collapse"

        MDExtendedFabButtonIcon:
            icon: "pencil-outline"

        MDExtendedFabButtonText:
            text: "Compose"
'''


class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"  # Define a paleta de cores primária
        self.theme_cls.theme_style = "Light"  # Define o estilo do tema (Light ou Dark)
        return Builder.load_string(KV)


Example().run()
