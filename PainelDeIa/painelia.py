from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

# Tamanho da janela
Window.size = (600, 500)
Window.clearcolor = (0.08, 0.1, 0.12, 1)  # Cor de fundo escura

class Painel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=25, spacing=20, **kwargs)

        with self.canvas.before:
            Color(0.15, 0.18, 0.22, 0.95)  # Fundo da interface
            self.bg = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # Título
        self.titulo = Label(
            text='[b]Painel de Controle da I.A[/b]',
            markup=True,
            font_size=28,
            color=(0.6, 0.9, 1, 1),
            size_hint=(1, 0.2)
        )
        self.add_widget(self.titulo)

        # Status da IA
        self.status = Label(
            text='[IA DESATIVADA]',
            font_size=18,
            color=(1, 0.4, 0.4, 1),
            size_hint=(1, 0.1)
        )
        self.add_widget(self.status)

        # Barra de ameaça
        self.progress = ProgressBar(max=100, value=0, height=25)
        self.add_widget(self.progress)

        # Botão de ligar/desligar IA
        self.toggle_btn = ToggleButton(
            text='Ligar I.A',
            size_hint=(1, 0.15),
            background_color=(0.2, 0.7, 1, 1),
            font_size=16
        )
        self.toggle_btn.bind(on_press=self.toggle_ia)
        self.add_widget(self.toggle_btn)

        # Campo de entrada de comando
        self.comando_input = TextInput(
            hint_text='Digite um comando...',
            size_hint=(1, 0.15),
            font_size=16,
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.6, 0.9, 1, 1)
        )
        self.add_widget(self.comando_input)

        # Botão de envio
        self.send_btn = Button(
            text='Enviar Comando',
            size_hint=(1, 0.12),
            background_color=(0.1, 0.6, 0.3, 1),
            font_size=16
        )
        self.send_btn.bind(on_press=self.executar_comando)
        self.add_widget(self.send_btn)

        # Inicialização da IA
        self.ia_ativa = False
        self.threat_event = None

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def toggle_ia(self, instance):
        self.ia_ativa = not self.ia_ativa
        if self.ia_ativa:
            self.status.text = '[IA ATIVADA]'
            self.status.color = (0.5, 1, 0.5, 1)
            self.toggle_btn.text = 'Desligar I.A'
            self.iniciar_ameaca()
        else:
            self.status.text = '[IA DESATIVADA]'
            self.status.color = (1, 0.4, 0.4, 1)
            self.toggle_btn.text = 'Ligar I.A'
            self.encerrar_ameaca()

    def iniciar_ameaca(self):
        self.progress.value = 0
        if self.threat_event:
            self.threat_event.cancel()
        self.threat_event = Clock.schedule_interval(self.aumentar_ameaca, 1.5)

    def encerrar_ameaca(self):
        if self.threat_event:
            self.threat_event.cancel()
            self.threat_event = None
        self.progress.value = 0

    def aumentar_ameaca(self, dt):
        if self.progress.value < 100:
            self.progress.value += 7
        else:
            self.status.text = '[ALERTA MÁXIMO - AMEAÇA TOTAL]'
            self.status.color = (1, 0.7, 0.2, 1)

    def executar_comando(self, instance):
        comando = self.comando_input.text.strip()
        if not comando:
            self.status.text = '[Digite um comando válido]'
            self.status.color = (1, 1, 0.3, 1)
            return

        if not self.ia_ativa:
            self.status.text = '[ERRO: IA DESLIGADA]'
            self.status.color = (1, 0.3, 0.3, 1)
        else:
            self.status.text = f'[Executando: {comando}]'
            self.status.color = (0.3, 0.8, 1, 1)
        self.comando_input.text = ''

class PainelIAApp(App):
    def build(self):
        self.title = "Painel de I.A - Estilizado"
        return Painel()

if __name__ == '__main__':
    PainelIAApp().run()
