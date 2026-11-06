from textual.widgets import Input, RichLog, Static

def print_execute_comand(console:RichLog, command, relative_current_path, base_virtual_path):
  console.write(f"{base_virtual_path}{relative_current_path}>{command}")