# -- imports de elementos da TUI --
from textual.app import App, ComposeResult
from textual.widgets import RichLog, Input, Static
from pyfiglet import Figlet
from textual.widgets import RichLog, Input, Static
from ui.terminal_structure import TerminalStructure #componente importado

# -- imports de componentes lógicos
from textual import on
from pathlib import Path
from commands.commands_logic import COMMAND_REGISTRY #comando do sistema
import core.terminal_logic as terminal#lógica do sistema

# -- class do App --
class Terminal(App):
  # -- caminho arquivo CSS --
  CSS_PATH = 'ui/style/terminal.css'

  # -- variável que indica qual o diretório de origem --
  BASE_DIR = (Path(__file__).resolve().parent.parent / 'galanis-group').resolve()

  # -- estrutura TUI --
  def compose(self) -> ComposeResult:
    yield TerminalStructure(classes="box")

  # -- executado quando o terminal é iniciado --
  def on_mount(self) -> None:
      # -- variáveis de controle de caminhos reias e relativos
      self.current_path = self.BASE_DIR #caminho atual desde a raiz
      self.relative_current_path = self.BASE_DIR.relative_to(self.BASE_DIR.parent) #caminho relativo
      self.base_virtual_path = 'C:\\Usuarios\\Admin\\' #inicio do caminho que aparece no TUI
  
      # -- digitando a inicialização do terminal --
      f = Figlet(font='slant')
      console = self.query_one('#console', RichLog)
      console.write(f"Terminal v7.0 - Digite ajuda para começar.\n{f.renderText('Galanis Group')}")
      
      # -- focus no input --
      input = self.query_one('#command', Input)
      input.focus()
  
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
if __name__ == "__main__":
  Terminal().run()