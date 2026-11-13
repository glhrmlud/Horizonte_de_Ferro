# -- imports de elementos da TUI --
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import VerticalScroll, Horizontal
from textual.widgets import RichLog, Input, Static, TextArea
from pyfiglet import Figlet
import asyncio
import random as r

# -- imports de componentes lógicos
import random
import string
import json
from textual import on, work
from pathlib import Path
from commands.commands_logic import COMMAND_REGISTRY #comando do sistema
import core.terminal_logic as terminal #lógica do sistema
from core.file_generator import draw_truth, field_map, generate_archives_galanis #criar arquivos


class TerminalStructure(VerticalScroll):
  def compose(self) -> ComposeResult:
    #Área de Logs/histórico do terminal
    yield RichLog(id='console', auto_scroll=True, markup=True)

    #Barra inferior caminho atual e input
    with Horizontal(classes='child-box'):
      yield Static(id='path')
      yield Input(id='command')

class TerminalScreen(Screen):
  # -- caminho arquivo CSS --
  CSS_PATH = 'style/terminal.css'

  # -- variável que indica qual o diretório de origem --
  BASE_DIR = (Path(__file__).resolve().parent.parent.parent / 'galanis_group').resolve()

  # -- estrutura TUI --
  def compose(self) -> ComposeResult:
    with Horizontal(id="main-screen-container"):
      yield TerminalStructure(id="terminal-structure")

      yield TextArea("--- ANOTAÇÕES DO CASO ---\n\n", id="notepad", classes="hidden")

  # -- animação de inicio do terminal
  @work
  async def init_animation(self) -> None:
    # -- digitando a inicialização do terminal --
    boot_messages = [
      "Estabelecendo handshake seguro [104.22.75.12]...",
      "Roteando pacotes via proxy offshore (Ilhas Cayman)... [OK]",
      "Bypass de firewall TCP/IP do Galanis Group...",
      "Injetando payload de camuflagem de IP... [SUCESSO]",
      "Descriptografando chaves RSA-2048...",
      "Acesso não autorizado detectado. Mascarando assinatura...",
      "Extraindo permissões de nível ROOT...",
      "Montando sistema de arquivos virtual..."
    ]

    console = self.query_one('#console', RichLog)
    input = self.query_one('#command', Input)

    input.disabled = True

    for msg in boot_messages:
      console.write(msg)
      time_sleep = r.uniform(0.05, 0.8)
      await asyncio.sleep(time_sleep)

    console.write("\nAutenticando credenciais...")
    await asyncio.sleep(1.5)

    console.write("\n[bold green]ACESSO CONCEDIDO.[/]\n")
    await asyncio.sleep(0.5)
    
    f = Figlet(font='slant')
    console.write(f"Terminal v7.0 - Digite HELP para começar\n{f.renderText('GOS')}Galanis Operational System\n")

    # -- focus no input --
    input.disabled = False
    input.focus()

  
  @work(exclusive=True)
  async def init_descon(self) -> None:
    console = self.query_one('#console', RichLog)
    input_cmd = self.query_one('#command', Input)

    input_cmd.disabled = True 
    
    console.write("\n[bold red]ATENÇÃO: DIVERGÊNCIA CRÍTICA DE DADOS.[/]")
    await asyncio.sleep(1)
    console.write("[bold red]FIREWALL DO GRUPO GALANIS ATIVADO. RASTREANDO IP...[/]")
    await asyncio.sleep(1.5)
    
    # Efeito Glitch: Imprime 15 a 20 linhas de lixo hexadecimal/ASCII
    for _ in range(20):
      caracteres_loucos = string.ascii_uppercase + string.digits + "!@#$%&*?_X"
      lixo = ''.join(random.choices(caracteres_loucos, k=50))
      
      console.write(f"[red]{lixo}[/]")

      await asyncio.sleep(random.uniform(0.02, 0.1)) 
        
    console.write("\n[bold red]CONEXÃO PERDIDA. FORÇANDO REINICIALIZAÇÃO...[/]\n")
    await asyncio.sleep(2)
    
    console.clear()
    console.write("[yellow]Reestabelecendo nova conexão proxy... (O caso foi resetado)[/]")
    
    terminal.result_comand(app=self,command_name="reset",command_registry=COMMAND_REGISTRY, args="")

    self.app.exit()
    
  # -- executado quando o terminal é iniciado --
  def on_mount(self) -> None:
    # -- variáveis de controle de caminhos reias e relativos
    self.current_path = self.BASE_DIR #caminho atual desde a raiz
    self.relative_current_path = self.BASE_DIR.relative_to(self.BASE_DIR.parent) #caminho relativo
    self.base_virtual_path = 'C:\\Usuarios\\Admin\\' #inicio do caminho que aparece no TUI

    # -- dicionário resposta
    path_catalog = (Path(__file__).resolve().parent.parent / 'core' / 'catalog.json').resolve()
    with open(path_catalog, 'r', encoding='utf-8') as f:
      self.catalog = json.load(f)

    self.response = draw_truth()
    generate_archives_galanis(self.BASE_DIR, field_map(self.response))

    # -- animação de entrada do terminal
    self.init_animation()

    # -- exibindo path atual --
    path_element = self.query_one('#path', Static)
    path_element.update(f'{self.base_virtual_path}{self.relative_current_path}>')

    # -- localizando input, caso o terminal esteja muito pequeno --
    self.query_one('#terminal-structure', TerminalStructure).scroll_end(animate=False)

  # -- executado quando usuário atualiza input --
  @on(Input.Changed, '#command')
  def locate_input(self, event: Input.Changed) -> None:
    self.query_one('#terminal-structure', TerminalStructure).scroll_end(animate=False)

  # -- executado quando um comando é enviado --
  @on(Input.Submitted, '#command')
  def process_command(self, event: Input.Submitted) -> None:
    console = self.query_one('#console', RichLog) #capturando elemento de id="console"
    pathElement = self.query_one('#path', Static) #capturando elemento de id="path"

    event.input.value = '' #limpando input

    command_name, args = terminal.format_command(event) #formatando o comando capturado

    console.write(f"{self.base_virtual_path}{self.relative_current_path}>{event.value}")

    # -- só é executado se o comando digitado não é '' --
    if (command_name != ''):
      ## -- executa o comando e exibe o resultado no terminal
      result = terminal.result_comand(self, args, command_name, COMMAND_REGISTRY)

      if result is True:
        pathElement.update(f"{self.base_virtual_path}{self.relative_current_path}>")
      elif result:
        console.write(result)

    # -- garante que o terminal exiba a linha de input --
    self.query_one('#terminal-structure', TerminalStructure).scroll_end(animate=False)