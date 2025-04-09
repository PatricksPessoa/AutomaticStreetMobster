import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import requests
import zipfile
import os
import sys
import shutil

# Versão atual do script
VERSAO_ATUAL = "1.0.0"

# Configurações do GitHub
USUARIO_GITHUB = 'SEU_USUARIO'
REPOSITORIO_GITHUB = 'SEU_REPOSITORIO'
URL_VERSAO = f'https://raw.githubusercontent.com/{USUARIO_GITHUB}/{REPOSITORIO_GITHUB}/main/versao.txt'
URL_ZIP = f'https://github.com/{USUARIO_GITHUB}/{REPOSITORIO_GITHUB}/releases/latest/download/Automatic%20StreetMobster.zip'

def verificar_atualizacao():
    try:
        resposta = requests.get(URL_VERSAO)
        resposta.raise_for_status()
        versao_remota = resposta.text.strip()
        if versao_remota > VERSAO_ATUAL:
            return versao_remota
    except requests.RequestException as e:
        print(f"Erro ao verificar atualização: {e}")
    return None

def baixar_atualizacao(progresso, label_status):
    try:
        resposta = requests.get(URL_ZIP, stream=True)
        resposta.raise_for_status()
        tamanho_total = int(resposta.headers.get('content-length', 0))
        caminho_zip = os.path.join(os.getcwd(), 'Automatic StreetMobster.zip')
        with open(caminho_zip, 'wb') as arquivo:
            baixado = 0
            for dados in resposta.iter_content(1024):
                arquivo.write(dados)
                baixado += len(dados)
                progresso['value'] = (baixado / tamanho_total) * 100
                label_status.config(text=f"Baixando: {int((baixado / tamanho_total) * 100)}%")
        return caminho_zip
    except requests.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao baixar atualização: {e}")
        return None

def aplicar_atualizacao(caminho_zip):
    try:
        pasta_temp = os.path.join(os.getcwd(), 'temp_atualizacao')
        if os.path.exists(pasta_temp):
            shutil.rmtree(pasta_temp)
        os.makedirs(pasta_temp)
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            zip_ref.extractall(pasta_temp)
        for item in os.listdir(pasta_temp):
            origem = os.path.join(pasta_temp, item)
            destino = os.path.join(os.getcwd(), item)
            if os.path.isdir(origem):
                if os.path.exists(destino):
                    shutil.rmtree(destino)
                shutil.move(origem, destino)
            else:
                shutil.move(origem, destino)
        shutil.rmtree(pasta_temp)
        os.remove(caminho_zip)
        messagebox.showinfo("Sucesso", "Atualização aplicada com sucesso! Reiniciando o aplicativo.")
        reiniciar_aplicacao()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao aplicar atualização: {e}")

def reiniciar_aplicacao():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def checar_e_atualizar(progresso, label_status):
    nova_versao = verificar_atualizacao()
    if nova_versao:
        if messagebox.askyesno("Atualização Disponível", f"Uma nova versão ({nova_versao}) está disponível. Deseja atualizar agora?"):
            caminho_zip = baixar_atualizacao(progresso, label_status)
            if caminho_zip:
                aplicar_atualizacao(caminho_zip)
    else:
        messagebox.showinfo("Sem Atualizações", "Você já está usando a versão mais recente.")

def iniciar_interface():
    root = tk.Tk()
    root.title("Automatic StreetMobster")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    label = ttk.Label(frame, text="Bem-vindo ao Automatic StreetMobster!")
    label.grid(row=0, column=0, columnspan=2, pady=10)

    btn_verificar = ttk.Button(frame, text="Verificar Atualizações", command=lambda: checar_e_atualizar(progresso, label_status))
    btn_verificar.grid(row=1, column=0, columnspan=2, pady=5)

    progresso = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
    progresso.grid(row=2, column=0, columnspan=2, pady=5)

    label_status = ttk.Label(frame, text="")
    label_status.grid(row=3, column=0, columnspan=2, pady=5)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()
