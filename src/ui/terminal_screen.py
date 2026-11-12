# -- imports de elementos da TUI --
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import VerticalScroll, Horizontal
from textual.widgets import RichLog, Input, Static
from pyfiglet import Figlet
import asyncio
import random as r

# -- imports de componentes lógicos
from textual import on, work
from pathlib import Path
from commands.commands_logic import COMMAND_REGISTRY #comando do sistema
import core.terminal_logic as terminal #lógica do sistema

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
    yield TerminalStructure(classes="box")

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
    
  # -- executado quando o terminal é iniciado --
  def on_mount(self) -> None:
    # -- variáveis de controle de caminhos reias e relativos
    self.current_path = self.BASE_DIR #caminho atual desde a raiz
    self.relative_current_path = self.BASE_DIR.relative_to(self.BASE_DIR.parent) #caminho relativo
    self.base_virtual_path = 'C:\\Usuarios\\Admin\\' #inicio do caminho que aparece no TUI

    # -- animação de entrada do terminal
    self.init_animation()

    # -- exibindo path atual --
    path_element = self.query_one('#path', Static)
    path_element.update(f'{self.base_virtual_path}{self.relative_current_path}>')

    # -- localizando input, caso o terminal esteja muito pequeno --
    self.query_one('.box', TerminalStructure).scroll_end(animate=False)

  # -- executado quando usuário atualiza input --
  @on(Input.Changed, '#command')
  def locate_input(self, event: Input.Changed) -> None:
    self.query_one('.box', TerminalStructure).scroll_end(animate=False)

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
    self.query_one('.box', TerminalStructure).scroll_end(animate=False)