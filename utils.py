from langconv import Converter
from pprint import pprint


def log(*args):
    if len(args) == 1:
        pprint(*args)
    else:
        print(*args)


def format(*args):
    args = [str(i) for i in args]
    return ' '.join(args)


def conv_zhs(char: str):
    return Converter('zh-hans').convert(char)
