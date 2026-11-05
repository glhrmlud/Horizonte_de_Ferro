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
    return target_path.relative_to(app.BASE_DIR.parent)

  return False

@register_command("exit", description="Fecha o terminal, terminando o jogo")
def handler_exit(app, args: str) -> None:
  app.exit()

@register_command("clear", description="Limpa o terminal")
def handler_clear(app, args: str) -> None:
  app.query_one("#console", RichLog).clear()

@register_command("dir", description='Lista conteúdo dentro de um diretório')
def handler_dir(app, args: str) -> str | bool:
  if args:
    dir_arg:Path = app.current_path / args
    if dir_arg.is_dir() and dir_arg.exists() and dir_arg.is_relative_to(app.current_path):
      list_archives = [i.name for i in dir_arg.iterdir()]
      return "\n".join(list_archives)
    return False
  if args == '/s':
    list_archives = []
    for i in sorted(app.current_path.rglob("*")):
      relative = i.relative_to(app.current_path)
      deep = len(relative.parts) - 1
      indent = " " * deep
      list_archives.append(f"{indent}|--- {i.name}")
    return "\n".join(list_archives)
  list_archives = [i.name for i in app.current_path.iterdir()]
  return "\n".join(list_archives)