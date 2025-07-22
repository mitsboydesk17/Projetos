from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class Contador(BoxLayout):
    # Propriedade numérica para armazenar o valor do contador
    conta = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 40
        self.spacing = 30

        # Label que mostra o valor do contador
        self.label = Label(
            text=str(self.conta),
            font_size='60sp',
            color=get_color_from_hex('#e74c3c'),  # Vermelho forte
            halign='center',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.add_widget(self.label)

        # Botão para aumentar o contador
        self.btn_aumentar = Button(
            text="Aumentar",
            size_hint=(1, 0.3),
            font_size='30sp',
            background_color=get_color_from_hex('#3498db')  # Azul
        )
        self.btn_aumentar.bind(on_release=self.aumentar)
        self.add_widget(self.btn_aumentar)

        # Atualiza o label quando a propriedade 'conta' mudar
        self.bind(conta=self.atualizar_label)

        # Fundo claro
        Window.clearcolor = get_color_from_hex('#f9f9f9')

    def aumentar(self, instance):
        self.conta += 1  # Incrementa o contador

    def atualizar_label(self, instance, value):
        self.label.text = str(value)  # Atualiza o texto do label

class NumericPropApp(App):
    def build(self):
        return Contador()

if __name__ == '__main__':
    NumericPropApp().run()
