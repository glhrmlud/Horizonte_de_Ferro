from pathlib import Path
from textual.widgets import RichLog, TextArea
from core.file_generator import draw_truth, field_map, generate_archives_galanis
import core.terminal_logic as terminal #lógica do sistema

COMMAND_REGISTRY = {}

def register_command(name: str, description:str, sintax: str):
  def decorator(func):
    COMMAND_REGISTRY[name] = {
      "description": description,
      "handler": func,
      "sintaxe": sintax, 
    }
    return func
  return decorator

# -- Comando HELP
@register_command("help", description="Para obter mais informações sobre um comando específico digite HELP nome_do_comando", sintax="help - exibe os comando disponíveis\nhelp <nome_comando> - exibe mais detalhes do comando digitado")
def handler_help(app, args: str) -> str:
  if args != '' and args in COMMAND_REGISTRY:
    return COMMAND_REGISTRY[args]["sintaxe"]
  if args != '':
    return f"[red] Comando {args} não existe [/]"
    
  command_list = [f"{n}: {i['description']}\n" for n, i in COMMAND_REGISTRY.items()]
  return "\n".join(command_list)

# -- Comando CD
@register_command("cd", description="Altera o diretório atual", sintax="cd <nome_dir> - abre o diretório digitado\ncd <caminho_dir> - abre o caminho do diretório digitado")
def handler_cd(app, args: str) -> Path | bool:
  if args == '':
    return app.current_path

  target_path = (app.current_path / args).resolve()

  if target_path.is_relative_to(app.BASE_DIR) and target_path.exists() and target_path.is_dir():
    return target_path 

  return False

# -- Comando EXIT
@register_command("exit", description="Fecha o terminal, terminando o jogo", sintax="exit - fecha o terminal")
def handler_exit(screen, args: str) -> None:
  screen.app.exit()

# -- Comando CLEAR
@register_command("clear", description="Limpa o terminal", sintax="clear - limpa o terminal")
def handler_clear(app, args: str) -> None:
  app.query_one("#console", RichLog).clear()

# -- Comando DIR
@register_command("dir", description='Lista conteúdo dentro de um diretório', sintax="dir - mostra pastas e arquivos dentro do diretório atual\ndir /s - mostra toda a árvore de arquivos dentro do diretório atual")
def handler_dir(app, args: str) -> str | bool:
  if args == '/s':
    list_archives = []
    for i in sorted(app.current_path.rglob("*")):
      relative = i.relative_to(app.current_path)
      deep = len(relative.parts) - 1
      indent = " " * deep
      list_archives.append(f"{indent}|--- {i.name}")
    return "\n".join(list_archives)
  
  if args:
      dir_arg:Path = app.current_path / args
      if dir_arg.is_dir() and dir_arg.exists() and dir_arg.is_relative_to(app.current_path):
        list_archives = [i.name for i in dir_arg.iterdir()]
        return "\n".join(list_archives)
      return False
  
  list_archives = [i.name for i in app.current_path.iterdir()]
  return "\n".join(list_archives)

# -- Comando TYPE
@register_command('type', description="Listar o conteúdo de um arquivo", sintax="type <nome_arquivo> - Lista todo o conteúdo de um arquivo")
def handler_type(app, args: str) -> str:
  if not args:
    return "[bold red]Comando digitado incorretamente \n Uso correto: type <nome_do_arquivo>[/bold red]"

  target_archive = (app.current_path / args).resolve()
  
  if target_archive.is_relative_to(app.BASE_DIR):
    if not target_archive.exists():
      return f"[red]Arquivo '{args}' não encontrado no diretório atual.[/]"
    if target_archive.is_dir():
        return f"[red]'{args}' é um diretório. Use 'dir' para listar o conteúdo.[/]"
    try:
      with open(target_archive, 'r', encoding='utf-8') as f:
        content = f.read()
      return f"{content}"
    except Exception as e:
      return "[bold red]Erro ao acessar arquivo... Tente novamente[/]"
  else:
    return "[bold red]Acesso negado: Tentativa de violação de segurança detectada.[/]"

# -- Comando notepad
@register_command("notepad", description="Ativa e desativa o notepad", sintax="notepad - abre um bloco de nota ao lado do terminal")
def handler_notepade(app, args: str) -> str:
  notepad = app.query_one("#notepad", TextArea)

  notepad.toggle_class("hidden")

  if notepad.has_class("hidden"):
    return "[yellow]Bloco de notas fechado.[/]"
  else:
    notepad.focus()
    return "[green]Bloco de notas aberto."

# -- Comando palpite
@register_command("palpite", description="Dá palpite do culapado, arma e local", sintax="palpite <culpado>;<arma>;<local>")
def handler_palpite(app, args: str) -> str:
  palpite = args.split(";")

  if len(palpite) != 3:
    return "[red]Sintaxe incorreta! Use: palpite <culpado>;<arma>;<local>[/]"

  p_guilty = palpite[0].strip().lower()
  p_arma = palpite[1].strip().lower()
  p_local = palpite[2].strip().lower()

  nomes_pessoas = [p.lower() for p in app.catalog["pessoas"]]
  nomes_armas = [a.lower() for a in app.catalog["armas"]]
  nomes_locais = [l.lower() for l in app.catalog["locais"]]

  if p_guilty not in nomes_pessoas:
    return f"[red]ERRO 404: Indivíduo '{palpite[0].strip()}' não consta nos registros do Grupo Galanis.[/]"
  if p_arma not in nomes_armas:
    return f"[red]ERRO 404: Objeto '{palpite[1].strip()}' desconhecido na investigação.[/]"
  if p_local not in nomes_locais:
    return f"[red]ERRO 404: Setor '{palpite[2].strip()}' não encontrado no mapa de Caelum.[/]"

  g = app.response["guilty"].strip().lower()
  l = app.response["local_crime"].strip().lower()
  w = app.response["weapon_crime"].strip().lower()
  
  if [p_guilty, p_arma, p_local] == [g, w, l]:
    terminal.result_comand(app=app,command_name="reset",command_registry=COMMAND_REGISTRY, args="")
    return "[bold green]CRIPTOGRAFIA QUEBRADA. ACESSO ROOT CONCEDIDO. A VERDADE FOI REVELADA!\nJOGO REINICIADO SINTA-SE A VONTADE PARA JOGAR NOVAMENTE[/]"
  else:
    # 3. A PUNIÇÃO: Em vez de só retornar texto, mandamos a Tela surtar!
    app.init_descon()
    
    # Retorna uma string vazia porque a tela já vai cuidar de mostrar o erro
    return ""

# -- Comando reset
@register_command("reset", description="Reseta o jogo", sintax="reset - reinicia o jogo, alterando o culpado do crime")
def handler_reset(app, args:str) -> str:
  app.response = draw_truth()
  generate_archives_galanis(app.BASE_DIR, field_map(app.response))
