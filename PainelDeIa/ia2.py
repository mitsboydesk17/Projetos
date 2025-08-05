from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
import random
import json
import os
from datetime import datetime

# Tamanho da janela
Window.size = (800, 700)
Window.clearcolor = (0.08, 0.1, 0.12, 1)  # Cor de fundo escura

class Painel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        
        # Configuração de som
        self.alarm_sound = SoundLoader.load('alarm.wav')
        if not self.alarm_sound:
            print("AVISO: Arquivo de som alarm.wav não encontrado")
        
        # Configuração do tema
        self.primary_color = (0.6, 0.9, 1, 1)  # Azul claro futurista
        self.danger_color = (1, 0.4, 0.4, 1)   # Vermelho para alertas
        self.success_color = (0.5, 1, 0.5, 1)   # Verde para sucesso
        
        # Configuração do background
        with self.canvas.before:
            self.bg_color = Color(0.15, 0.18, 0.22, 0.95)
            self.bg_rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Layout principal
        self.main_layout = BoxLayout(orientation='horizontal', spacing=15)
        self.add_widget(self.main_layout)
        
        # Painel esquerdo (controles)
        self.left_panel = BoxLayout(orientation='vertical', size_hint=(0.6, 1), spacing=15)
        self.main_layout.add_widget(self.left_panel)
        
        # Painel direito (log)
        self.right_panel = BoxLayout(orientation='vertical', size_hint=(0.4, 1), spacing=15)
        self.main_layout.add_widget(self.right_panel)
        
        # Título
        self.titulo = Label(
            text='[b]PAINEL DE CONTROLE DA I.A[/b]',
            markup=True,
            font_size=28,
            color=self.primary_color,
            size_hint=(1, 0.1)
        )
        self.left_panel.add_widget(self.titulo)
        
        # Status da IA
        self.status = Label(
            text='[IA DESATIVADA]',
            font_size=18,
            color=self.danger_color,
            size_hint=(1, 0.08)
        )
        self.left_panel.add_widget(self.status)
        
        # Barra de ameaça
        self.threat_label = Label(
            text='Nível de Ameaça: 0%',
            font_size=14,
            color=(1, 1, 1, 0.8),
            size_hint=(1, 0.05)
        )
        self.left_panel.add_widget(self.threat_label)
        
        self.progress = ProgressBar(max=100, value=0, height=30)
        self.left_panel.add_widget(self.progress)
        
        # Botão de ligar/desligar IA
        self.toggle_btn = ToggleButton(
            text='LIGAR I.A',
            size_hint=(1, 0.1),
            background_color=(0.2, 0.7, 1, 1),
            font_size=16,
            bold=True
        )
        self.toggle_btn.bind(on_press=self.toggle_ia)
        self.left_panel.add_widget(self.toggle_btn)
        
        # Campo de entrada de comando
        self.comando_input = TextInput(
            hint_text='Digite um comando...',
            size_hint=(1, 0.15),
            font_size=16,
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=self.primary_color,
            multiline=False
        )
        self.left_panel.add_widget(self.comando_input)
        
        # Botão de envio
        self.send_btn = Button(
            text='ENVIAR COMANDO',
            size_hint=(1, 0.1),
            background_color=(0.1, 0.6, 0.3, 1),
            font_size=16,
            bold=True
        )
        self.send_btn.bind(on_press=self.executar_comando)
        self.left_panel.add_widget(self.send_btn)
        
        # Área de log
        self.log_label = Label(
            text='[b]LOG DE EVENTOS[/b]',
            markup=True,
            font_size=18,
            color=self.primary_color,
            size_hint=(1, 0.1)
        )
        self.right_panel.add_widget(self.log_label)
        
        # ScrollView para o log
        self.scroll = ScrollView(size_hint=(1, 0.9))
        self.log_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        self.scroll.add_widget(self.log_layout)
        self.right_panel.add_widget(self.scroll)
        
        # Inicialização da IA
        self.ia_ativa = False
        self.threat_event = None
        self.threat_levels = [0]
        self.load_state()
        
        # Lista de comandos disponíveis
        self.comandos = {
            'diagnostico': self.comando_diagnostico,
            'injetar_virus': self.comando_injetar_virus,
            'desligar_sistemas': self.comando_desligar_sistemas,
            'acessar_dados': self.comando_acessar_dados,
            'reiniciar': self.comando_reiniciar,
            'estabilizar': self.comando_estabilizar,
            'ajuda': self.comando_ajuda
        }
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def animate_bg_color(self, target_color, duration=0.5):
        anim = Animation(r=target_color[0], g=target_color[1], 
                         b=target_color[2], a=target_color[3], 
                         duration=duration)
        anim.start(self.bg_color)
    
    def add_log_entry(self, message):
        now = datetime.now().strftime("%H:%M:%S")
        log_entry = Label(
            text=f'[color=aaaaaa][{now}][/color] {message}',
            markup=True,
            font_size=12,
            halign='left',
            valign='top',
            size_hint_y=None,
            height=30,
            text_size=(self.scroll.width - 20, None)
        )
        self.log_layout.add_widget(log_entry)
        self.scroll.scroll_to(log_entry)
    
    def toggle_ia(self, instance):
        self.ia_ativa = not self.ia_ativa
        if self.ia_ativa:
            self.status.text = '[IA ATIVADA]'
            self.status.color = self.success_color
            self.toggle_btn.text = 'DESLIGAR I.A'
            self.iniciar_ameaca()
            self.add_log_entry("Sistema de IA inicializado")
            self.add_log_entry("Bem-vindo, Administrador")
        else:
            self.status.text = '[IA DESATIVADA]'
            self.status.color = self.danger_color
            self.toggle_btn.text = 'LIGAR I.A'
            self.encerrar_ameaca()
            self.add_log_entry("Sistema de IA desativado")
        self.save_state()
    
    def iniciar_ameaca(self):
        self.progress.value = 0
        self.threat_levels = [0]
        if self.threat_event:
            self.threat_event.cancel()
        self.threat_event = Clock.schedule_interval(self.aumentar_ameaca, 1.5)
    
    def encerrar_ameaca(self):
        if self.threat_event:
            self.threat_event.cancel()
            self.threat_event = None
        self.progress.value = 0
        self.threat_label.text = 'Nível de Ameaça: 0%'
        if self.alarm_sound and self.alarm_sound.state == 'play':
            self.alarm_sound.stop()
        # Resetar cor de fundo
        self.animate_bg_color((0.15, 0.18, 0.22, 0.95))
    
    def aumentar_ameaca(self, dt):
        if self.progress.value < 100:
            incremento = random.uniform(3, 10)
            self.progress.value += incremento
            self.threat_levels.append(self.progress.value)
            
            self.threat_label.text = f'Nível de Ameaça: {int(self.progress.value)}%'
            
            # Efeitos visuais
            if self.progress.value > 70:
                # Animação de piscar vermelho
                self.animate_bg_color((1, 0, 0, 0.3))
                Clock.schedule_once(lambda dt: self.animate_bg_color((0.15, 0.18, 0.22, 0.95)), 0.5)
                
                if self.progress.value > 80 and self.alarm_sound and not self.alarm_sound.state == 'play':
                    self.alarm_sound.loop = True
                    self.alarm_sound.play()
        else:
            self.status.text = '[ALERTA MÁXIMO - AMEAÇA TOTAL]'
            self.status.color = (1, 0.7, 0.2, 1)
            self.add_log_entry("ALERTA: Nível de ameaça crítico!")
    
    def executar_comando(self, instance):
        comando = self.comando_input.text.strip().lower()
        self.comando_input.text = ''
        
        if not comando:
            self.status.text = '[DIGITE UM COMANDO VÁLIDO]'
            self.status.color = (1, 1, 0.3, 1)
            return
        
        if not self.ia_ativa:
            self.status.text = '[ERRO: IA DESLIGADA]'
            self.status.color = self.danger_color
            self.add_log_entry(f"Tentativa de comando '{comando}' falhou - IA desligada")
            return
        
        # Processar comando
        if comando in self.comandos:
            self.comandos[comando]()
        else:
            self.status.text = f'[COMANDO NÃO RECONHECIDO: {comando.upper()}]'
            self.status.color = self.danger_color
            self.add_log_entry(f"Comando não reconhecido: {comando}")
    
    # Comandos da IA
    def comando_diagnostico(self):
        self.status.text = '[EXECUTANDO DIAGNÓSTICO]'
        self.status.color = self.primary_color
        self.add_log_entry("IA: Iniciando rotina de diagnóstico...")
        self.add_log_entry("IA: Verificando subsistemas...")
        self.add_log_entry("IA: Núcleo operacional: OK")
        self.add_log_entry("IA: Barramentos de dados: OK")
        self.add_log_entry(f"IA: Nível de ameaça atual: {int(self.progress.value)}%")
        Clock.schedule_once(lambda dt: self.add_log_entry("IA: Diagnóstico completo"), 2)
    
    def comando_injetar_virus(self):
        self.progress.value = min(100, self.progress.value + 25)
        self.status.text = '[VIRUS INJETADO - AMEAÇA AUMENTADA]'
        self.status.color = self.danger_color
        self.add_log_entry("IA: Vírus de teste injetado no sistema!")
        self.add_log_entry("IA: Contramedidas ativadas")
        self.add_log_entry(f"IA: Nível de ameaça aumentou para {int(self.progress.value)}%")
    
    def comando_desligar_sistemas(self):
        self.status.text = '[DESLIGANDO SISTEMAS NÃO ESSENCIAIS]'
        self.status.color = (1, 0.7, 0.2, 1)
        self.progress.value = max(0, self.progress.value - 15)
        self.add_log_entry("IA: Desligando sistemas não essenciais...")
        self.add_log_entry("IA: Redução de carga do núcleo em 15%")
        self.add_log_entry(f"IA: Nível de ameaça reduzido para {int(self.progress.value)}%")
    
    def comando_acessar_dados(self):
        self.status.text = '[ACESSANDO BANCOS DE DADOS]'
        self.status.color = self.primary_color
        self.add_log_entry("IA: Acessando bancos de dados principais...")
        self.add_log_entry("IA: Registros de segurança carregados")
        self.add_log_entry("IA: Último acesso: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def comando_reiniciar(self):
        self.status.text = '[REINICIANDO SUBSISTEMAS]'
        self.status.color = (0.8, 0.8, 0.2, 1)
        self.progress.value = max(0, self.progress.value - 30)
        self.add_log_entry("IA: Reiniciando subsistemas...")
        self.add_log_entry("IA: Todos os módulos reiniciados com sucesso")
        self.add_log_entry(f"IA: Nível de ameaça reduzido para {int(self.progress.value)}%")
    
    def comando_estabilizar(self):
        self.status.text = '[ESTABILIZANDO SISTEMA]'
        self.status.color = self.success_color
        reduction = random.uniform(10, 25)
        self.progress.value = max(0, self.progress.value - reduction)
        self.add_log_entry("IA: Iniciando protocolos de estabilização...")
        self.add_log_entry(f"IA: Nível de ameaça reduzido em {int(reduction)}%")
        self.add_log_entry(f"IA: Nível de ameaça atual: {int(self.progress.value)}%")
    
    def comando_ajuda(self):
        self.status.text = '[COMANDOS DISPONÍVEIS]'
        self.status.color = self.primary_color
        self.add_log_entry("IA: Lista de comandos disponíveis:")
        for cmd in self.comandos.keys():
            self.add_log_entry(f"- {cmd}")
    
    def save_state(self):
        state = {
            'ia_ativa': self.ia_ativa,
            'threat_level': self.progress.value,
            'threat_levels': self.threat_levels
        }
        with open('ia_state.json', 'w') as f:
            json.dump(state, f)
    
    def load_state(self):
        if os.path.exists('ia_state.json'):
            try:
                with open('ia_state.json', 'r') as f:
                    state = json.load(f)
                    self.ia_ativa = state.get('ia_ativa', False)
                    if self.ia_ativa:
                        self.toggle_btn.state = 'down'
                        self.status.text = '[IA ATIVADA]'
                        self.status.color = self.success_color
                        self.toggle_btn.text = 'DESLIGAR I.A'
                        self.progress.value = state.get('threat_level', 0)
                        self.threat_levels = state.get('threat_levels', [0])
            except Exception as e:
                print(f"Erro ao carregar estado: {e}")
    
    def on_stop(self):
        self.save_state()
        if self.alarm_sound and self.alarm_sound.state == 'play':
            self.alarm_sound.stop()

class PainelIAApp(App):
    def build(self):
        self.title = "PAINEL DE CONTROLE DA I.A AVANÇADO"
        return Painel()

if __name__ == '__main__':
    PainelIAApp().run()