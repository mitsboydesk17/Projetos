from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class LayoutResponsivo(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = [30, 50, 30, 50]

        # Cor de fundo da janela
        Window.clearcolor = get_color_from_hex("#f7f9fb")

        # Título
        self.titulo = Label(
            text="Bem-vindo ao App Responsivo!",
            font_size='28sp',
            size_hint=(1, 0.2),
            color=get_color_from_hex("#2c3e50")
        )
        self.add_widget(self.titulo)

        # Entrada de texto
        self.caixa_input = TextInput(
            hint_text="Digite seu nome...",
            multiline=False,
            font_size='20sp',
            size_hint=(1, 0.15),
            background_color=get_color_from_hex("#ffffff"),
            foreground_color=get_color_from_hex("#2c3e50"),
            cursor_color=get_color_from_hex("#2c3e50"),
            padding_y=(10, 10)
        )
        self.add_widget(self.caixa_input)

        # Botão de enviar
        self.botao = Button(
            text="Enviar",
            size_hint=(1, 0.15),
            font_size='22sp',
            background_color=get_color_from_hex("#3498db"),
            color=(1, 1, 1, 1)
        )
        self.botao.bind(on_release=self.exibir_mensagem)
        self.add_widget(self.botao)

        # Resultado
        self.resposta = Label(
            text="",
            font_size='24sp',
            size_hint=(1, 0.2),
            color=get_color_from_hex("#16a085")
        )
        self.add_widget(self.resposta)

    def exibir_mensagem(self, instance):
        nome = self.caixa_input.text.strip()
        if nome:
            self.resposta.text = f"Olá, {nome}! Seja bem-vindo 😄"
        else:
            self.resposta.text = "Por favor, digite seu nome!"

class ResponsivoApp(App):
    def build(self):
        return LayoutResponsivo()

if __name__ == '__main__':
    ResponsivoApp().run()
