from commands_logic import help, cd
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
    event.input.value = '' #limpando input

    command = event.value.strip().lower()
    console = self.query_one('#console', RichLog)

    #exit
    if command == 'exit':
      self.exit()

    #help
    elif command == 'help':
      print_execute_comand(console, command, self.current_path, self.base_virtual_path)
      help(console)

    #clear
    elif command == 'clear':
      console.clear()

    #cd
    elif command[:2] == 'cd':
      #exibindo comando executado na tela
      print_execute_comand(console, command, self.current_path, self.base_virtual_path)

      #executando o comando solicitado
      result_cd = cd(command, self.current_path, self.BASE_DIR)

      #erro de caminho inexistente
      if not result_cd: 
        #exibindo erro no terminal
        console.write("O sistema não pode encontrar o caminho especificado\n")
      else:
        #atualizando path em que o usuario sem encontra
        self.current_path = Path(result_cd)

        #mostrando visualmente que o path foi atualizado
        path_element = self.query_one('#path', Static)
        path_element.update(f'{self.base_virtual_path}{self.current_path}>')

    #erro de comando
    elif command == '':
      print_execute_comand(console, command, self.current_path, self.base_virtual_path)
    else: 
      print_execute_comand(console, command, self.current_path, self.base_virtual_path)
      console.write(f'{command} não é reconhecido como um comando')

    #garante que o terminal exiba a linha de input
    self.query_one('.box', VerticalScroll).scroll_end(animate=False)
if __name__ == "__main__":
  Terminal().run()