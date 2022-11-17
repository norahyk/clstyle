from enum import Enum
from dataclasses import dataclass
from typing import Union

Type = Enum('Type', ['FUNC', 'VAR'])

@dataclass
class DefinedName():
    line_no: int
    name: str
    type: Type
    word_count: int
    module_path: Union[str, None] = None