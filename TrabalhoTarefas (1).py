import tkinter as tk
import sqlite3
import re

def adicionar_tarefa():
    descricao = entrada_descricao.get()
    data_limite = entrada_data_limite.get()

    if descricao and data_limite and re.match(r"\d{2}/\d{2}/\d{4}", data_limite):
        cursor.execute("INSERT INTO tarefas (descricao, data_limite) VALUES (?, ?)", (descricao, data_limite))
        conn.commit()
        listar_tarefas()
        limpar_campos()

def listar_tarefas():
    lista_tarefas.delete(0, tk.END)
    cursor.execute("SELECT * FROM tarefas")
    tarefas = cursor.fetchall()
    for tarefa in tarefas:
        lista_tarefas.insert(tk.END, f"{tarefa[1]} - {tarefa[2]}")

def atualizar_tarefa():
    selecao = lista_tarefas.curselection()
    if selecao:
        nova_descricao = entrada_descricao.get()
        nova_data_limite = entrada_data_limite.get()
        tarefa_selecionada = lista_tarefas.get(selecao[0])

        descricao_atual, data_limite_atual = tarefa_selecionada.split(" - ")

        if nova_descricao and nova_data_limite and re.match(r"\d{2}/\d{2}/\d{4}", nova_data_limite):
            cursor.execute("UPDATE tarefas SET descricao=?, data_limite=? WHERE descricao=? AND data_limite=?",
                           (nova_descricao, nova_data_limite, descricao_atual, data_limite_atual))
            conn.commit()
            listar_tarefas()
            limpar_campos()

def excluir_tarefa():
    selecao = lista_tarefas.curselection()
    if selecao:
        tarefa_selecionada = lista_tarefas.get(selecao[0])
        descricao, data_limite = tarefa_selecionada.split(" - ")
        cursor.execute("DELETE FROM tarefas WHERE descricao=? AND data_limite=?", (descricao, data_limite))
        conn.commit()
        listar_tarefas()
        limpar_campos()

def limpar_campos():
    entrada_descricao.delete(0, tk.END)
    entrada_data_limite.delete(0, tk.END)

def formatar_data(event):
    data_limite = entrada_data_limite.get()
    if data_limite:
        data_limite = re.sub(r'\D', '', data_limite)
        if len(data_limite) > 8:
            data_limite = data_limite[:8]
        if len(data_limite) >= 2:
            dia = data_limite[:2]
            if int(dia) > 31:
                dia = "31"
            data_limite = f"{dia}/" + data_limite[2:]
        if len(data_limite) >= 5:
            mes = data_limite[3:5]
            if int(mes) > 12:
                mes = "12"
            data_limite = f"{data_limite[:3]}{mes}/" + data_limite[5:]
        entrada_data_limite.delete(0, tk.END)
        entrada_data_limite.insert(0, data_limite)

# conectando sqlite

conn = sqlite3.connect("tarefas.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY,
    descricao TEXT,
    data_limite TEXT
)
""")
conn.commit()

#Criamos a janela para o gerenciador.
janela = tk.Tk()
janela.title("Gerenciador de Tarefas")
janela.configure(bg="#34495e")

# Colocamos botoes e componentes personalizados, cores, posições.
frame_botoes = tk.Frame(janela, bg="#34495e")
frame_botoes.pack(side=tk.LEFT)

frame_lista = tk.Frame(janela, bg="#34495e")
frame_lista.pack(side=tk.RIGHT)

etiqueta_descricao = tk.Label(frame_botoes, text="Nome da tarefa:", bg="#34495e", fg="white", font=("Microsoft Sans Serif", 12,))
etiqueta_descricao.pack()

entrada_descricao = tk.Entry(frame_botoes, width=20, font=("Arial", 12))
entrada_descricao.pack(pady=5) 

etiqueta_data_limite = tk.Label(frame_botoes, text="Data Limite (DD/MM/AAAA):", bg="#34495e", fg="white", font=("Microsoft Sans Serif", 12,))
etiqueta_data_limite.pack()

entrada_data_limite = tk.Entry(frame_botoes, width=20, font=("Arial", 12))
entrada_data_limite.pack(pady=10) 

entrada_data_limite.bind('<KeyRelease>', formatar_data)

botao_adicionar = tk.Button(frame_botoes, text="Adicionar Tarefa", command=adicionar_tarefa, bg="#106b21", fg="white", font=("Arial", 10))
botao_adicionar.pack()

botao_atualizar = tk.Button(frame_botoes, text="Alterar Tarefa", command=atualizar_tarefa, bg="#e74c3c", fg="white", font=("Arial", 10))
botao_atualizar.pack()

botao_excluir = tk.Button(frame_botoes, text="Apagar Tarefa", command=excluir_tarefa, bg="#ce0018", fg="white", font=("Arial", 10))
botao_excluir.pack()

lista_tarefas = tk.Listbox(frame_lista, font=("Arial", 12))
lista_tarefas.pack()

listar_tarefas()

janela.geometry("400x250") #Mudamos o tamanho da janela (mantivemos o padrão da tela login)
janela.mainloop()
