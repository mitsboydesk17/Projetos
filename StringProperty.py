from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class MyWidget(BoxLayout):
    saudacao = StringProperty("Olá, Kivy!")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 20

        # Criar um Label para mostrar a saudação
        self.label = Label(
            text=self.saudacao,
            font_size='40sp',
            color=get_color_from_hex('#3498db'),  # Azul bonito
            halign='center',
            valign='middle'
        )
        # Configura para o label se ajustar no box
        self.label.bind(size=self.label.setter('text_size'))
        self.add_widget(self.label)

        # Opcional: fundo branco
        Window.clearcolor = get_color_from_hex('#ffffff')

class StringPropApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    StringPropApp().run()
