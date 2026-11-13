# -- imports de elementos da TUI --
from textual.app import App

# -- imports de telas --
from ui.menu_screen import MenuScreen
from ui.terminal_screen import TerminalScreen
from ui.story_screen import StoryScreen 

# -- class do App --
class GalanisApp(App):
  SCREENS = {
    "menu": MenuScreen,
    "story": StoryScreen,
    "terminal": TerminalScreen,
  }

  # -- Executado ao iniciar
  def on_mount(self) -> None:
    self.app.push_screen("menu")

 
if __name__ == "__main__":
  GalanisApp().run()