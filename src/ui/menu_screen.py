# -- imports de elementos da TUI --
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from pyfiglet import Figlet

# -- imports de componentes lógicos
from textual.events import Enter, Leave
from textual import on

class MenuStructure(Vertical):
  def compose(self) -> ComposeResult:
    # -- Caixa de título
    f = Figlet(font='slant', width=200)
    logo_art = f.renderText("Horizonte de Ferro")
    yield Static(logo_art, id="title")

    # -- Caixa botões
    with Horizontal(id="btn-box"):
      yield Button("Começar Investigação", id="start-btn")
      yield Button("Desistir", id="quit-btn")


class MenuScreen(Screen):
  # -- CSS TUI
  CSS_PATH = "style/menu.css"

  # -- Desativando AutoFocus botões
  AUTO_FOCUS = False

  # -- Estrutura TUI
  def compose(self) -> ComposeResult:
    yield MenuStructure()

  @on(Enter, "Button")
  def roubar_foco_no_hover(self, event: Enter) -> None:
      # Pega o botão exato que o mouse encostou e transfere o foco para ele
      event.control.focus()

  @on(Leave, "Button")
  def limpar_foco_ao_sair(self, event: Leave) -> None:
      # Quando o mouse sai do botão, mandamos a tela "zerar" o foco atual
      self.set_focus(None)

  # -- Começar jogo (iniciar Terminal)
  @on(Button.Pressed, "#start-btn")
  def start_game(self, event: Button.Pressed) -> None:
    self.app.push_screen("terminal")

  # -- Fechar jogo
  @on(Button.Pressed, "#quit-btn")
  def quit_game(self, event: Button.Pressed) -> None:
    self.app.exit()