import tkinter as tk
from tkinter import filedialog, messagebox
import os, sys

# --- Importes de ANTLR ---
from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

# Asegura que Python encuentre el paquete "src"
ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

# IMPORTA TU GRAMÁTICA de prueba (Hello)
# Nota: estamos usando la que generaste en src/hello/grammar
try:
    from src.hello.grammar.HelloLexer import HelloLexer
    from src.hello.grammar.HelloParser import HelloParser
except Exception as e:
    # Si falla, muestra un mensaje claro
    print("No se pudieron importar HelloLexer/HelloParser. "
          "Verifica que existan en src/hello/grammar y que tengas antlr4-python3-runtime instalado.")
    raise

# Regla de inicio de la gramática (para Hello.g4, la regla se llama 'r')
START_RULE = "r"


class SyntaxErrorListener(ErrorListener):
    """Captura errores léxicos y sintácticos."""
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Línea {line}, columna {column}: {msg}")


class MiniIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini IDE - Compilador ANTLR (Hello.g4)")

        # Editor
        self.text = tk.Text(root, wrap="word", font=("Consolas", 12))
        self.text.pack(expand=1, fill="both")

        # Barra de menú
        menu = tk.Menu(root)
        root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Abrir", command=self.abrir)
        file_menu.add_command(label="Guardar", command=self.guardar)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=root.quit)

        # Botón Compilar
        compile_btn = tk.Button(root, text="Compilar", command=self.compilar)
        compile_btn.pack(side="bottom", fill="x")

    def abrir(self):
        file = filedialog.askopenfilename(
            filetypes=[("Archivos de código", "*.code *.txt *.src *.hello *.py"), ("Todos", "*.*")]
        )
        if file:
            with open(file, "r", encoding="utf-8") as f:
                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", f.read())

    def guardar(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".code",
            filetypes=[("Archivos de código", "*.code *.txt *.src *.hello"), ("Todos", "*.*")]
        )
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", tk.END))

    def compilar(self):
        code = self.text.get("1.0", "end-1c")  # sin el salto final
        if not code.strip():
            messagebox.showwarning("Compilador", "El editor está vacío.")
            return

        # Configura lexer y parser
        lexer = HelloLexer(InputStream(code))
        lex_err = SyntaxErrorListener()
        lexer.removeErrorListeners()
        lexer.addErrorListener(lex_err)

        tokens = CommonTokenStream(lexer)
        parser = HelloParser(tokens)
        parse_err = SyntaxErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(parse_err)

        # Llama dinámicamente a la regla de inicio
        try:
            start = getattr(parser, START_RULE)  # por ahora 'r'
        except AttributeError:
            messagebox.showerror("Compilador", f"No existe la regla de inicio '{START_RULE}' en el parser.")
            return

        tree = start()  # ejecuta el parse

        # Si hubo errores léxicos o sintácticos, muéstralos
        all_errors = lex_err.errors + parse_err.errors
        if all_errors:
            self._show_output("\n".join(all_errors), title="Errores de compilación")
        else:
            # Árbol sintáctico en formato textual de ANTLR
            tree_text = tree.toStringTree(recog=parser)
            self._show_output(f"Árbol sintáctico:\n{tree_text}", title="Árbol sintáctico")

    def _show_output(self, content: str, title: str = "Salida"):
        win = tk.Toplevel(self.root)
        win.title(title)
        txt = tk.Text(win, wrap="word", font=("Consolas", 11), height=24, width=100)
        txt.pack(expand=1, fill="both")
        txt.insert("1.0", content)
        txt.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    ide = MiniIDE(root)
    ide.text.insert("1.0", "hello world\n")
    root.mainloop()
