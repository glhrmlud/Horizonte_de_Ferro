from commands_logic import COMMAND_REGISTRY
from terminal_logic import print_execute_comand
from textual.app import App, ComposeResult
from textual import on
from textual.containers import VerticalScroll, Horizontal
from textual.widgets import RichLog, Input, Static
from pathlib import Path
from pyfiglet import Figlet

class Terminal(App):
  CSS_PATH = 'Style/terminal.css'

  BASE_DIR = Path('galanis-group').resolve()

  # Estrutura do terminal
  def compose(self) -> ComposeResult:
    with VerticalScroll(classes='box'):
      yield RichLog(id='console', auto_scroll=True)
      with Horizontal(classes='child-box'):
        yield Static(id='path')
        yield Input(id='command')

  # Executado quando iniciado
  def on_mount(self) -> None:
    self.current_path = self.BASE_DIR.relative_to(self.BASE_DIR.parent)#caminho atual
    self.base_virtual_path = 'C:\\Usuarios\\Admin\\'

    #digitando a inicialização do terminal
    f = Figlet(font='slant')
    console = self.query_one('#console', RichLog)
    console.write(f'Terminal v7.0 - Digite ajuda para começar.\n{f.renderText('Galanis Group')}')
    
    #dando foco ao input
    input = self.query_one('#command', Input)
    input.focus()

    #exibindo path atual
    path_element = self.query_one('#path', Static)
    path_element.update(f'{self.base_virtual_path}{self.current_path}>')

    #localizando input, caso o terminal esteja muito pequeno
    self.query_one('.box', VerticalScroll).scroll_end(animate=False)

  # Executado quando usuário atualiza input
  @on(Input.Changed, '#command')
  def locate_input(self, event: Input.Changed) -> None:
    self.query_one('.box', VerticalScroll).scroll_end(animate=False)

  # Executado quando um comando é digitado
  @on(Input.Submitted, '#command')
  def process_command(self, event: Input.Submitted) -> None:
    console = self.query_one('#console', RichLog)
    pathElement = self.query_one('#path', Static)

    event.input.value = '' #limpando input

    command = event.value.lower().split(maxsplit=1) #tratando comando recebido
    command_name = command[0]
    args = command[1] if len(command) > 1 else ''
    if command_name == 'help': args = console #em caso de ser o help 

    print_execute_comand(console, event.value, self.current_path, self.base_virtual_path)

    if command_name in COMMAND_REGISTRY:
      command_info = COMMAND_REGISTRY[command_name]
      handler = command_info["handler"]

      result = handler(args, self.current_path, self.BASE_DIR)
    
      if isinstance(result, Path):
        self.current_path = result
        pathElement.update(f'{self.base_virtual_path}{self.current_path}>')
      elif isinstance(result, str):
        console.write(result)
      elif result == None:
        pass
      elif result is False:
        console.write("[bold red]Erro: Diretório inválido ou fora dos limites[/bold red]")
    else:
      console.write(f"[red]Comando '{command_name}' não reconhecido.[/red]")

    #garante que o terminal exiba a linha de input
    self.query_one('.box', VerticalScroll).scroll_end(animate=False)
if __name__ == "__main__":
  Terminal().run()