from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class ListaItensWidget(BoxLayout):
    # Lista inicial com alguns itens
    lista_de_compras = ListProperty(['Leite', 'Ovos', 'Pão'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        # Label para mostrar os itens da lista separados por vírgula
        self.label_lista = Label(
            text=', '.join(self.lista_de_compras),
            font_size='24sp',
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=60,
            color=get_color_from_hex('#34495e')  # Azul escuro
        )
        self.label_lista.bind(size=self.label_lista.setter('text_size'))
        self.add_widget(self.label_lista)

        # Caixa horizontal para o TextInput e o botão
        caixa_input = BoxLayout(size_hint_y=None, height=40, spacing=10)

        # TextInput para adicionar novo item
        self.text_input = TextInput(
            multiline=False,
            font_size=22
        )
        caixa_input.add_widget(self.text_input)

        # Botão para adicionar o item da TextInput na lista
        botao_adicionar = Button(
            text="Adicionar Item",
            size_hint_x=0.4,
            font_size=20,
            background_color=get_color_from_hex('#27ae60'),
            color=(1,1,1,1)
        )
        botao_adicionar.bind(on_release=self.adicionar_item)
        caixa_input.add_widget(botao_adicionar)

        self.add_widget(caixa_input)

        # Atualiza o label quando a lista mudar
        self.bind(lista_de_compras=self.atualizar_label)

        # Fundo claro
        Window.clearcolor = get_color_from_hex('#ecf0f1')

    def adicionar_item(self, instance):
        item = self.text_input.text.strip()
        if item:
            self.lista_de_compras.append(item)  # Adiciona o item na lista
            self.text_input.text = ""  # Limpa o input

    def atualizar_label(self, instance, value):
        # Atualiza o texto do label com os itens separados por vírgula
        self.label_lista.text = ', '.join(value)

class ListPropApp(App):
    def build(self):
        return ListaItensWidget()

if __name__ == '__main__':
    ListPropApp().run()
