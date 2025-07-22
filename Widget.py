from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock

class MyContainer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        # TextInput para o usuário digitar
        self.meu_input = TextInput(
            multiline=False,
            font_size=24,
            size_hint_y=None,
            height=40
        )
        self.meu_input.bind(text=self.on_text_change)
        self.add_widget(self.meu_input)

        # Label que sempre mostra o texto atual do TextInput
        self.label_texto = Label(
            text="",
            font_size=28,
            size_hint_y=None,
            height=40,
            halign='center',
            valign='middle'
        )
        self.label_texto.bind(size=self.label_texto.setter('text_size'))
        self.add_widget(self.label_texto)

        # Label que mostra "Você está digitando..." quando o texto muda
        self.label_digitando = Label(
            text="",
            font_size=24,
            size_hint_y=None,
            height=30,
            color=(0, 0, 1, 1),  # Azul
            halign='center',
            valign='middle'
        )
        self.label_digitando.bind(size=self.label_digitando.setter('text_size'))
        self.add_widget(self.label_digitando)

        self._event = None  # Guarda o evento do Clock para cancelar

    def on_text_change(self, instance, value):
        # Atualiza o label com o texto digitado
        self.label_texto.text = value

        # Mostra mensagem "Você está digitando..."
        self.label_digitando.text = "Você está digitando..."

        # Cancela evento anterior (se existir)
        if self._event:
            self._event.cancel()

        # Agenda para limpar a mensagem após 1.5 segundos de pausa
        self._event = Clock.schedule_once(self.limpar_mensagem, 1.5)

    def limpar_mensagem(self, dt):
        self.label_digitando.text = ""
        self._event = None

class KVBindApp(App):
    def build(self):
        return MyContainer()

if __name__ == '__main__':
    KVBindApp().run()
