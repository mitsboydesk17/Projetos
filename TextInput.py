from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class InputPropWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        # TextInput para o usuário digitar o texto
        self.meu_input_texto = TextInput(
            multiline=False,
            font_size=24,
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.meu_input_texto)

        # Label para mostrar o texto confirmado
        self.label_confirmado = Label(
            text="",
            font_size=28,
            size_hint_y=None,
            height=50,
            halign='center',
            valign='middle',
            color=get_color_from_hex('#2c3e50')
        )
        self.label_confirmado.bind(size=self.label_confirmado.setter('text_size'))
        self.add_widget(self.label_confirmado)

        # Botão para confirmar a atualização do texto
        self.botao_confirmar = Button(
            text="Confirmar",
            size_hint=(1, 0.3),
            font_size=26,
            background_color=get_color_from_hex('#2980b9'),
            color=(1, 1, 1, 1)
        )
        self.botao_confirmar.bind(on_release=self.confirmar_texto)
        self.add_widget(self.botao_confirmar)

        # Fundo claro
        Window.clearcolor = get_color_from_hex('#ecf0f1')

    def confirmar_texto(self, instance):
        # Atualiza o texto do label com o texto do TextInput
        self.label_confirmado.text = self.meu_input_texto.text

class InputPropApp(App):
    def build(self):
        return InputPropWidget()

if __name__ == '__main__':
    InputPropApp().run()
