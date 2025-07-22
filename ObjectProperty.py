from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class ControleWidget(BoxLayout):
    # ObjectProperty para referenciar o Label alvo
    target_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        # Cria o label alvo e atribui à propriedade
        self.target_label = Label(
            text="Texto Inicial",
            font_size='36sp',
            halign='center',
            valign='middle',
            color=get_color_from_hex('#2c3e50')
        )
        self.target_label.bind(size=self.target_label.setter('text_size'))
        self.add_widget(self.target_label)

        # Botão que muda o texto do label alvo
        self.btn_mudar = Button(
            text="Mudar Texto",
            size_hint=(1, 0.3),
            font_size='28sp',
            background_color=get_color_from_hex('#2980b9'),
            color=(1,1,1,1)
        )
        self.btn_mudar.bind(on_release=self.mudar_texto_alvo)
        self.add_widget(self.btn_mudar)

        # Fundo claro
        Window.clearcolor = get_color_from_hex('#ecf0f1')

    def mudar_texto_alvo(self, instance):
        if self.target_label:
            self.target_label.text = "Texto Mudado!"

class ObjectPropApp(App):
    def build(self):
        return ControleWidget()

if __name__ == '__main__':
    ObjectPropApp().run()
