from antlr4 import InputStream, CommonTokenStream
from .HelloLexer import HelloLexer
from .HelloParser import HelloParser

def parse_text(text: str):
    lexer = HelloLexer(InputStream(text))
    tokens = CommonTokenStream(lexer)
    parser = HelloParser(tokens)
    tree = parser.r()
    return tree, parser

if __name__ == "__main__":
    sample = "hello world"
    tree, parser = parse_text(sample)
    print("Árbol:", tree.toStringTree(recog=parser))