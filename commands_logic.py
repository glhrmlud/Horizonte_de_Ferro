from pathlib import Path

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
def handler_help(args: str | object, current_path: Path | bool, base_dir: Path) -> None:
  for command_name in COMMAND_REGISTRY:
    args.write(f"{command_name} : {COMMAND_REGISTRY[command_name]["description"]}")
