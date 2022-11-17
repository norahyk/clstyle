from clstyle import extract_defined_names
from clstyle.cli import 


def test_list_variables():
    with open('tests/test_repo/simple-repo/src/main.py') as f:
        script = f.read()
    
    defined_names = extract_defined_names(script)