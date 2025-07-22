from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class StatusWidget(BoxLayout):
    status_message = StringProperty("Online")  # Propriedade que armazena o status

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 25

        # Label que mostra o status
        self.label = Label(
            text=self.status_message,
            font_size='50sp',
            color=get_color_from_hex('#27ae60'),  # Verde para "Online"
            halign='center',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.add_widget(self.label)

        # Botão para mudar o status
        self.button = Button(
            text="Mudar Status",
            font_size='28sp',
            size_hint=(1, 0.3),
            background_color=get_color_from_hex('#2980b9')  # Azul
        )
        self.button.bind(on_release=self.mudar_status)
        self.add_widget(self.button)

        # Vincula a propriedade status_message ao método que atualiza o label
        self.bind(status_message=self.update_label_text)

        # Fundo claro
        Window.clearcolor = get_color_from_hex('#ecf0f1')

    def update_label_text(self, instance, value):
        # Atualiza o texto do label e muda a cor dependendo do status
        self.label.text = value
        if value == "Online":
            self.label.color = get_color_from_hex('#27ae60')  # Verde
        else:
            self.label.color = get_color_from_hex('#c0392b')  # Vermelho para "Offline"

    def mudar_status(self, instance):
        # Alterna entre Online e Offline
        if self.status_message == "Online":
            self.status_message = "Offline"
        else:
            self.status_message = "Online"

class BindStringApp(App):
    def build(self):
        return StatusWidget()

if __name__ == '__main__':
    BindStringApp().run()
