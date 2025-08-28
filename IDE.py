import tkinter as tk
from tkinter import filedialog, messagebox
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token

class MiniIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini IDE - Compilador ANTLR")
        self.text = tk.Text(root, wrap="word", font=("Consolas", 12))
        self.text.pack(expand=1, fill="both")


        menu = tk.Menu(root)
        root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Abrir", command=self.abrir)
        file_menu.add_command(label="Guardar", command=self.guardar)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=root.quit)


        compile_btn = tk.Button(root, text="Compilar", command=self.compilar)
        compile_btn.pack(side="bottom", fill="x")

    def abrir(self):
        file = filedialog.askopenfilename(filetypes=[("Archivos de código", "*.txt *.code *.py")])
        if file:
            with open(file, "r", encoding="utf-8") as f:
                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", f.read())

    def guardar(self):
        file = filedialog.asksaveasfilename(defaultextension=".code", filetypes=[("Archivos de código", "*.code"), ("Todos", "*.*")])
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", tk.END))

    def compilar(self):
        code = self.text.get("1.0", tk.END)
        messagebox.showinfo("Compilador", "Compilación aún no implementada.\nCódigo recibido:\n" + code[:100])

if __name__ == "__main__":
    root = tk.Tk()
    ide = MiniIDE(root)
    root.mainloop()
