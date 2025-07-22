from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class PlayerInfo(BoxLayout):
    player_name = StringProperty("Jogador 1")
    player_score = NumericProperty(0)
    is_online = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        # Label do nome do jogador
        self.label_nome = Label(
            text=f"Nome: {self.player_name}",
            font_size='28sp',
            color=get_color_from_hex('#34495e')
        )
        self.add_widget(self.label_nome)

        # TextInput para alterar o nome do jogador
        self.input_nome = TextInput(
            multiline=False,
            font_size=22,
            hint_text="Digite novo nome"
        )
        self.input_nome.bind(text=self.atualizar_nome)
        self.add_widget(self.input_nome)

        # Label da pontuação
        self.label_pontuacao = Label(
            text=f"Pontuação: {self.player_score}",
            font_size='28sp',
            color=get_color_from_hex('#2980b9')
        )
        self.add_widget(self.label_pontuacao)

        # Botão para aumentar pontuação
        self.btn_aumentar = Button(
            text="Aumentar Pontuação",
            font_size='24sp',
            size_hint=(1, 0.3),
            background_color=get_color_from_hex('#27ae60'),
            color=(1,1,1,1)
        )
        self.btn_aumentar.bind(on_release=lambda x: self.aumentar_pontuacao())
        self.add_widget(self.btn_aumentar)

        # ToggleButton para status online/offline
        self.toggle_status = ToggleButton(
            text="Offline",
            font_size='24sp',
            size_hint=(1, 0.3),
            background_color=get_color_from_hex('#c0392b'),
            color=(1,1,1,1),
            state='normal'
        )
        self.toggle_status.bind(on_state=self.alternar_status)
        self.add_widget(self.toggle_status)

        # Atualiza os labels quando as propriedades mudam
        self.bind(player_name=self.atualizar_label_nome,
                  player_score=self.atualizar_label_pontuacao,
                  is_online=self.atualizar_toggle_status)

        # Fundo claro
        Window.clearcolor = get_color_from_hex('#ecf0f1')

    def aumentar_pontuacao(self):
        self.player_score += 1

    def alternar_status(self, instance, state):
        self.is_online = (state == 'down')

    def atualizar_nome(self, instance, value):
        self.player_name = value

    def atualizar_label_nome(self, instance, value):
        self.label_nome.text = f"Nome: {value}"

    def atualizar_label_pontuacao(self, instance, value):
        self.label_pontuacao.text = f"Pontuação: {value}"

    def atualizar_toggle_status(self, instance, value):
        if value:
            self.toggle_status.text = "Online"
            self.toggle_status.background_color = get_color_from_hex('#27ae60')
        else:
            self.toggle_status.text = "Offline"
            self.toggle_status.background_color = get_color_from_hex('#c0392b')

class CustomPropApp(App):
    def build(self):
        return PlayerInfo()

if __name__ == '__main__':
    CustomPropApp().run()
