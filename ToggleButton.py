from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class ToggleStateWidget(BoxLayout):
    is_active = BooleanProperty(False)  # Propriedade booleana para estado

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 25

        # ToggleButton que alterna o estado
        self.toggle_btn = ToggleButton(
            text="Ativar / Desativar",
            size_hint=(1, 0.4),
            font_size='28sp',
            background_color=get_color_from_hex('#2980b9'),
            color=(1,1,1,1)
        )
        self.toggle_btn.bind(on_state=self.on_toggle_state)
        self.add_widget(self.toggle_btn)

        # Label que mostra o estado atual
        self.status_label = Label(
            text="Inativo",
            font_size='40sp',
            color=get_color_from_hex('#c0392b'),  # Vermelho = inativo
            halign='center',
            valign='middle'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.add_widget(self.status_label)

        # Fundo claro
        Window.clearcolor = get_color_from_hex('#ecf0f1')

        # Atualiza o label conforme o valor inicial
        self.atualizar_label()

    def on_toggle_state(self, instance, state):
        # Atualiza a propriedade is_active com base no estado do ToggleButton
        self.is_active = (state == 'down')
        self.atualizar_label()

    def atualizar_label(self):
        # Atualiza o texto e cor do label com base no valor de is_active
        if self.is_active:
            self.status_label.text = "Ativo"
            self.status_label.color = get_color_from_hex('#27ae60')  # Verde
        else:
            self.status_label.text = "Inativo"
            self.status_label.color = get_color_from_hex('#c0392b')  # Vermelho

class BoolPropApp(App):
    def build(self):
        return ToggleStateWidget()

if __name__ == '__main__':
    BoolPropApp().run()
