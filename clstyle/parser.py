import tokenize as tk
from loguru import logger

class Value:
    """A generic object with a list of preset fields."""

    def __init__(self, *args):
        if len(self._fields) != len(args):
            raise ValueError(
                f'got {len(args)} arguments for {len(self._fields)} fields for {self.__class__.__name__}: {self._fields}'
            )
        vars(self).update(zip(self._fields, args))
    
    def __hash__(self):
        return hash(repr(self))
    
    def __eq__(self, other):
        return other and vars(self) == vars(other)

    def __repr__(self):
        kwargs = ', '.join(f'{field}={getattr(self, field)}' for field in self._fields)
        return f'{self.__class__.__name__}({kwargs})'


class TokenKind(int):
    def __repr__(self):
        return f"tk.{tk.tok_name[self]}"

class Token(Value):
    _fields = 'kind value start end source'.split()

    def __init__(self, *args):
        super().__init__(*args)
        self.kind = TokenKind(self.kind)
    
    def __str__(self):
        return f'{self.kind}({self.value})'


class TokenStream:
    LOGICAL_NEWLINES = {tk.NEWLINE, tk.INDENT, tk.DEDENT}

    def __init__(self, filelike):
        self._generator = tk.generate_tokens(filelike.readline)
        self.current = Token(*next(self._generator, None))
        self.line = self.current.start[0]
        self.got_logical_newline = True

    def move(self):
        previous = self.current
        current = self._next_from_generator()
        self.current = None if current is None else Token(*current)
        self.line = self.current.start[0] if self.current else self.line
        is_logical_blank = previous.kind in (tk.NL, tk.COMMENT)
        self.got_logical_newline = (
            previous.kind in self.LOGICAL_NEWLINES
            or (self.got_logical_newline and is_logical_blank)
        )
        return previous
    
    def _next_from_generator(self):
        try:
            return next(self._generator, None)
        except (SyntaxError, tk.TokenError):
            logger.warning('error generating tokens', exc_info=True)
            return None
    
    def __iter__(self):
        while True:
            if self.current is not None:
                yield self.current
            else:
                return
            self.move()


class ParseError(Exception):
    """An error parsing contents of a Python file."""

    def __str__(self):
        return "Cannot parse file."


def parse_variable_difinition():
    pass


def parser(filelike, filename):
    source = filelike.readlines()
    src = ''.join(source)
    try:
        compile(src, filename, 'exec')
    except SyntaxError as error:
        raise ParseError() from error
    tokens = tk.generate_tokens(StringIO(src).readline)

    previous = None
    for token in tokens:
        print(token)
        print(token.type == tk.NAME)
        if token.type == tk.NAME:
            if previous in ['def', 'class']:
                if token.string.startswith('__') and token.string.endswith('__'):
                    continue
                print(token.string)
            if token.string == "=":
                print(previous)
        previous = token.string
            
            


if __name__ == '__main__':
    # from io import StringIO
    # with tk.open('tests/test_repo/simple-repo/src/calc/add.py') as f:
    #     filelike = StringIO(''.join(f.readlines()))
    #     # tokens = tk.generate_tokens(filelike.readline)
    #     parser(filelike, "test")
    
    # for token in tokens:
        # print(token)

    from tree_sitter import Language, Parser

    Language.build_library('build/my-languages.so', ['vendor/tree-sitter-python'])
    