import typer
import subprocess
from subprocess import PIPE
import os
import pydocstyle
from pathlib import Path


from clstyle.utils import extract_defined_names, list_module_paths


app = typer.Typer()


def list_defined_names(module_path):
    with open(module_path, 'r') as f:
        script = f.read()
    defined_names = extract_defined_names(script)
    for dn in defined_names:
        dn.module_path = f"{module_path}:{dn.line_no}"
    return defined_names


def sort_defined():
    pass

def print_difined(defined_names):
    if len(defined_names) == 0:
        return
    max_length = max(dn.word_count for dn in defined_names)
    for dn in defined_names:
        print(f'{dn.name: <{max_length}}\t{dn.type}\t{dn.module_path}')
 
@app.command()
def defined_names(root_path: str):
    module_paths = list_module_paths(root_path)

    # TODO: 指定されたモジュールを無視できる機能
    
    for module_path in module_paths:
        defined_names = list_defined_names(module_path)
        print_difined(defined_names)
    
    # TODO: よくない変数を判別

@app.command()
def docstring(root_path: str):
    pydocstyle_path = Path(pydocstyle.__file__).parent
    proc = subprocess.run(['python', pydocstyle_path, root_path, '--select=D102,D103', '--count' ,'-s'], cwd=os.getcwd())
    print(proc.stdout)
            

def main():
    app()

if __name__ == '__main__':
    # main()
    import pkgutil
    print([m.name for m in pkgutil.walk_packages(['clstyle'])])