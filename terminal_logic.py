from textual.widgets import Input, RichLog, Static

def print_execute_comand(console:RichLog, command, current_path, base_virtual_path):
  console.write(f"{base_virtual_path}{current_path}>{command}")