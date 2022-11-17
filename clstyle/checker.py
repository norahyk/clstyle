import tokenize as tk

from loguru import logger


def check_source(source, filename):
    module = parse(StringIO(source), filename)


def check(*filenames):
    for filename in filenames:
        logger.info(f'Checking file {filename}.')

        try:
            with tk.open(filename) as file:
                source = file.read()
        except tk.TokenError:
            yield SyntaxError(f'invalid syntax in file {filename}')
            