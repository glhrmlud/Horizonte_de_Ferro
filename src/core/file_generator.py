# -- Imports lógicos
import random
import json
from pathlib import Path
import shutil
import os

# -- Sorteador Culpados
def draw_truth() -> dict:
  path_catalog = (Path(__file__).resolve().parent / 'catalog.json').resolve()
  print(path_catalog)

  with open(path_catalog, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

  peoples = catalog['pessoas'].copy()
  locals = catalog['locais'].copy()
  weapons = catalog['armas'].copy()

  random.shuffle(peoples)
  random.shuffle(locals)
  random.shuffle(weapons)

  draw = {
    "guilty": peoples[0],
    "innocent": peoples[1:],
    "local_crime": locals[0],
    "locals_false": locals[1:],
    "weapon_crime": weapons[0],
    "weapons_false": weapons[1:],
  }

  return draw

# -- Criar mapa de substituição nos arquivos placeholders
def field_map(draw: dict) -> dict:
  map = {
    "{spt1}": draw["guilty"],
    "{arm1}": draw["weapon_crime"],
    "{lcs1}": draw["local_crime"],
  }
  for i, innocent in enumerate(draw["innocent"], start=2):
    map[f"{{spt{i}}}"] = innocent
        
  for i, arm in enumerate(draw["weapons_false"], start=2):
    map[f"{{arm{i}}}"] = arm
      
  for i, local in enumerate(draw["locals_false"], start=2):
    map[f"{{lcs{i}}}"] = local

  return map

# -- Gera os arquivos a serem vasculhados pelo jogador
def generate_archives_galanis(dir_end: Path, map: dict) -> None:
  base_dir = (Path(__file__).resolve().parent.parent / 'placeholder').resolve()

  if dir_end.exists():
    shutil.rmtree(dir_end)

  shutil.copytree(base_dir, dir_end)

  for root, dirs, files in os.walk(dir_end):
    for file in files:
      if file.endswith(".txt"):
        archive_path = Path(root) / file

        with open(archive_path, 'r', encoding="utf-8") as f:
          content = f.read()

        for key, value in map.items():
          content = content.replace(key, value)

        with open(archive_path, 'w', encoding='utf-8') as f:
          f.write(content)