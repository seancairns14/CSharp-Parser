from dataclasses import dataclass
from typing import List
from interpreter import tokenize, Token


@dataclass
class SharpInfo:
    file: List[Token]

    @property
    def dependencies(self):

        return

    @property
    def methods(self):
        return

    @property
    def classes(self):
        return


def process_sharp(csharp_file):
    tokens = []
    with open(csharp_file, 'r', encoding='utf-8') as file:
        for token in tokenize(file.read()):
            tokens.append(token)
    return tokens




if __name__ == '__main__':
    file = process_sharp('Plugin.cs')
    print(type(file))





