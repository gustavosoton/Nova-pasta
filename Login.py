import tkinter as tk
from tkinter import messagebox
import sqlite3

def fazer_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    
    cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
    if cursor.fetchone():
        messagebox.showinfo("Login", "Login concluído!")
        janela_login.destroy()
        import TrabalhoTarefas  #para abrir o nosso gerenciador após o login.
    else:
        messagebox.showerror("Login", "senha ou usuário incorretos")

def registrar():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    
    if usuario and senha:
        try:
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
            conn.commit()
            messagebox.showinfo("Registro", "Cadastro foi um sucesso!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Registro", "Escolha outro nome de usuário, esse já está em uso!")
    else:
        messagebox.showerror("Registro", "usuário e senha são campos obrigatórios.")

# conectando sqlite
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    usuario TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
""")
conn.commit()

#Criamos a janela para login
janela_login = tk.Tk()
janela_login.title("Tela de Login")  

#Escolhemos a cor e uma fonte diferente para Usuário e senha.
janela_login.configure(bg="#34495e")
etiqueta_usuario = tk.Label(janela_login, text="Usuário:", bg="#34495e", fg="white", font=("Microsoft Sans Serif", 17, "italic"))
etiqueta_usuario.pack()
entrada_usuario = tk.Entry(janela_login, width=40, font=("Arial", 12))
entrada_usuario.pack(pady=5)  #Aumentamos o espaço entre os componentes.

etiqueta_senha = tk.Label(janela_login, text="Senha:", bg="#34495e", fg="white", font=("Microsoft Sans Serif", 17, "italic"))
etiqueta_senha.pack()
entrada_senha = tk.Entry(janela_login, show="*", width=40, font=("Arial", 12))
entrada_senha.pack(pady=10)  #Aumentamos o espaço entre os componentes.

botao_login = tk.Button(janela_login, text="Entrar", command=fazer_login, bg="#106b21", fg="white", font=("Arial", 14))
botao_login.pack(pady=10)

botao_registro = tk.Button(janela_login, text="Registrar", command=registrar, bg="#e74c3c", fg="white", font=("Arial", 14))
botao_registro.pack()

janela_login.geometry("400x250")  #Mudamos o tamanho da janela.
janela_login.mainloop()
