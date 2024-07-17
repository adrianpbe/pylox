from typing import List
import sys

from pylox.tokenizer import Token, tokenize


class Lox:
    def __init__(self):
        self.had_error = False
    
    def run(self, code: str):
        print(code)
        tokens = tokenize(code)
        print("\n".join([token.to_str() for token in tokens]))

    def run_file(self, file: str):
        with open(file, "r") as f:
            code = f.read()
        self.run(code)

    def run_prompt(self):
        while True:
            line = input("> ")
            # TODO: deal with exiting
            self.run(line)
            self.had_error = False
