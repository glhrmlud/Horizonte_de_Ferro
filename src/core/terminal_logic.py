from pathlib import Path
from textual.widgets import Input 

def execute_comand(app, args: str, command_name: str, command_registry: dict) -> dict:
  if command_name in command_registry:
    command_info = command_registry[command_name]
    handler = command_info["handler"]
    return {
      "result": handler(app, args),
      "ok": True
    }
  return {
    "result": f"[red]Comando '{command_name}' não reconhecido.[/red]",
    "ok": False
  }

def result_comand(app, args: str, command_name: str, command_registry: dict) -> str:
  comand_dict= execute_comand(app, args, command_name, command_registry)
  result = comand_dict["result"]
  if not comand_dict["ok"]:
    return result
  if isinstance(result, Path):
    app.current_path = result
    app.relative_current_path = result.relative_to(app.BASE_DIR.parent)
    return True
  elif isinstance(result, str):
    return result
  elif result is False:
    return "[bold red]Erro: Diretório inválido ou fora dos limites[/bold red]"

# -- formata o comando enviado pelo usuaário --
def format_command(event: Input.Submitted):
  # -- consulta valor enviado --
  command = event.value.lower().split(maxsplit=1) 
  # -- verifica se um comando foi digitado --
  command_name = command[0] if len(command) > 0 else ''
  args = ''
  # -- verifica se não foi digitado 'cd..' -- 
  if command_name == 'cd..':
    command_name = 'cd'
    args = '..'
  args = command[1] if len(command) > 1 else args
  return command_name, args