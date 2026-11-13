# -- imports de elementos da TUI --
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.app import ComposeResult
from textual.containers import VerticalScroll, Horizontal
from pyfiglet import Figlet
import asyncio

# -- imports de componentes lógicos
from textual.events import Enter, Leave
from textual import on, work

class StoryStructure(VerticalScroll):
  def compose(self) -> ComposeResult:
    # -- Título
    yield Static(id="title")
    # -- Campo de texto -- 
    with VerticalScroll(id="story-container"):
      pass

    # -- Botão de avançar e voltar
    with Horizontal(id="btn-box"):
      yield Button("Pular História", id="skip")
      yield Button("Próximo", id="next")

class StoryScreen(Screen):
  # -- CSS TUI
  CSS_PATH = "style/story.css"

  # -- Desativando AutoFocus botões
  AUTO_FOCUS = False

  # -- Estrutura TUI
  def compose(self) -> ComposeResult:
    yield StoryStructure(id="story-structure")

  # -- Animação de carregamento da história
  @work
  async def animate_history(self, text: str, btn: Button, block: Static) -> None:
    container = self.query_one("#story-container", VerticalScroll)
    btn.disabled = True

    text_animate = ""

    for l in text:
      text_animate += l
      block.update(text_animate)
      container.scroll_end(animate=False)

      await asyncio.sleep(0.03)

    btn.disabled = False  

  def on_mount(self):
    # -- Escrevendo texto na tela
    title = self.query_one("#title", Static)
    f = Figlet("slant", width=200)
    title.update(f"{f.renderText("Historia")}")
    # -- Dicionário História
    self.story = {
      "intro": "'Em um futuro onde tecnologia e poder caminham lado a lado, encontra-se Caelum, uma cidade monumental, marcada por contrastes sociais, conspirações e segredos.\nNo centro de tudo está o Grupo Galanis, uma poderosa corporação envolvida no desenvolvimento de uma arma biológica conhecida como BiOS.\nMas algo deu errado.",
      "climax": "O desaparecimento de César Galanis e o misterioso roubo da BiOS desencadearam uma investigação que pode revelar muito mais do que aparenta.\nMarcus Galanis, Marta Peregrino, Vicenzo Calvini, Sarah Lithos, Nikolas Prometheus e William Lopes estão entre as figuras envolvidas nesse complexo mistério.",
      "missao": "Agora, sua missão é investigar os dados do sistema operacional do Grupo Galanis, analisar registros, encontrar evidências e conectar informações que podem revelar a verdade por trás dos acontecimentos.",
      "questionamentos": "Quem está por trás do roubo?\nQuais segredos foram escondidos?\nE, principalmente...\nEm quem você pode confiar?",
    }

    # -- Exibindo texto na tela e salvando variáveis de controle
    self.story_keys = list(self.story.keys())
    self.current_step = 0

    self.current_key = self.story_keys[self.current_step]
    text = self.story[self.current_key]

    btn = self.query_one("#next", Button)
    container = self.query_one("#story-container", VerticalScroll)

    new_block = Static("", classes="story-block")
    container.mount(new_block)

    self.animate_history(text, btn, new_block)
    self.current_step += 1
  

  @on(Enter, "Button")
  def roubar_foco_no_hover(self, event: Enter) -> None:
      # Pega o botão exato que o mouse encostou e transfere o foco para ele
      event.control.focus()

  @on(Leave, "Button")
  def limpar_foco_ao_sair(self, event: Leave) -> None:
      # Quando o mouse sai do botão, mandamos a tela "zerar" o foco atual
      self.set_focus(None)

  # -- Pular história (inicia Terminal)
  @on(Button.Pressed, "#skip")
  def skip_story(self, event: Button.Pressed) -> None:
    self.app.push_screen("terminal")
  
  # -- Passa a história
  @on(Button.Pressed, "#next")
  def next_story(self, event: Button.Pressed) -> None:
    container = self.query_one("#story-container", VerticalScroll)

    if self.current_step < len(self.story_keys):
      self.current_key = self.story_keys[self.current_step]
      text = self.story[self.current_key]

      new_block = Static("", classes="story-block")
      container.mount(new_block)

      self.animate_history(text, event.button, new_block)
      self.current_step += 1
    else:
      new_block = Static("[FIM.]", classes="story-block")
      container.mount(new_block)

      block_points = Static("", classes="story-block")
      container.mount(block_points)

      self.animate_history("...", event.button, block_points)
      
      container.scroll_end(animate=False)
      event.button.disabled = True

      self.app.push_screen("terminal")
      
          