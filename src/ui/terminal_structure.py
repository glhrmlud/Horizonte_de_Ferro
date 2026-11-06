from textual.app import ComposeResult
from textual.containers import VerticalScroll, Horizontal
from textual.widgets import RichLog, Input, Static

class TerminalStructure(VerticalScroll):
  def compose(self) -> ComposeResult:
    #Área de Logs/histórico do terminal
    yield RichLog(id='console', auto_scroll=True, markup=True)

    #Barra inferior caminho atual e input
    with Horizontal(classes='child-box'):
      yield Static(id='path')
      yield Input(id='command')
