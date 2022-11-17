import os
import ast
from typing import Union, List


from clstyle.models import DefinedName, Type
from clstyle.helpers import is_module


def list_module_paths(top):
    modules = []
    for root, dirs, files in os.walk(top=top):
        for f in files:
            if is_module(f):
                file_path = os.path.join(root, f)
                modules.append(file_path)
    return modules


def extract_defined_names(script) -> List[DefinedName]:
    """与えられた文字列の中から、定義名を抽出する"""
    root = ast.parse(script)

    all_defined = []
    for node in ast.walk(root):
        defined = None
        if isinstance(node, ast.FunctionDef):
            name = node.name
            word_count = len(name)
            defined = DefinedName(node.lineno, name, Type.FUNC, word_count)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            name = node.id
            word_count = len(name)
            defined = DefinedName(node.lineno, name, Type.VAR, word_count)
        elif isinstance(node, ast.Attribute):
            name = node.attr
            word_count = len(name)
            defined = DefinedName(node.lineno, name, Type.VAR, word_count)
        
        if defined:
            all_defined.append(defined)
    return all_defined