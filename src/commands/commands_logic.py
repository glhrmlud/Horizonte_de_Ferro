from pathlib import Path
from textual.widgets import RichLog

COMMAND_REGISTRY = {}

def register_command(name: str, description:str):
  def decorator(func):
    COMMAND_REGISTRY[name] = {
      "description": description,
      "handler": func,
    }
    return func
  return decorator

@register_command("help", description="Para obter mais informações sobre um comando específico digite HELP nome_do_comando")
def handler_help(app, args: str) -> str:
  command_list = [f"{n}: {i['description']}" for n, i in COMMAND_REGISTRY.items()]
  return "\n".join(command_list)

@register_command("cd", description="Altera o diretório atual")
def handler_cd(app, args: str) -> Path | bool:
  if args == '':
    return app.current_path

  target_path = (app.current_path / args).resolve()

  if target_path.is_relative_to(app.BASE_DIR) and target_path.exists() and target_path.is_dir():
    return target_path 

  return False

@register_command("exit", description="Fecha o terminal, terminando o jogo")
def handler_exit(screen, args: str) -> None:
  screen.app.exit()

@register_command("clear", description="Limpa o terminal")
def handler_clear(app, args: str) -> None:
  app.query_one("#console", RichLog).clear()

@register_command("dir", description='Lista conteúdo dentro de um diretório')
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

@register_command('type', description="Utilizado para listar o conteúdo de um arquivo")
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