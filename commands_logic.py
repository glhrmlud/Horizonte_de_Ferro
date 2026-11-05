from pathlib import Path

def help(console, command = False):
  if command:
    return
  #comandos
  exit = 'EXIT - fechar terminal'
  clear = 'CLEAR - limpar terminal'
  cd = 'CD - exibe o nome do diretório atual ou acessa pastas'
  comand_list = [exit, clear, cd]

  #exibindo comandos na tela
  console.write('Para obter mais informações sobre um comando específico digite HELP nome_do_comando:\n')
  for c in comand_list:
    console.write(f'{c}')

def cd(comand, current_path:Path, BASE_DIR):
  required_path = comand[2:] #path solicitado pelo usuário
  target_path:Path = (current_path / required_path).resolve()

  if not target_path.is_relative_to(BASE_DIR): return False
  elif target_path.exists() and target_path.is_dir():
    return target_path.relative_to(BASE_DIR.parent)