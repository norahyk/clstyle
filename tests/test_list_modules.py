import os

from clstyle import list_module_paths


def test_list_modules():
    root_path = 'tests/test_repo/simple_repo'
    module_paths = list_module_paths(root_path)
    
    expected = {
        os.path.join(root_path, 'main.py'),
        os.path.join(root_path,'calc', 'add.py'),
        os.path.join(root_path, 'calc', 'prod.py')
    }

    assert set(module_paths) == expected