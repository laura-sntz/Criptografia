import tkinter as tk
from tkinter import filedialog
import sha256bin

# Leitura de um arquivo qualquer de qualquer formato (pdr, docxm jpeg e etc.)

# Oculta a janela principal do Tkinter
janela = tk.Tk()
janela.withdraw()

# Abre o explorador de arquivos para o usuário escolher o arquivo
caminho_arquivo = filedialog.askopenfilename(title="Escolha um arquivo qualquer")

if caminho_arquivo:
    try:
        # Chama a função do arquivo sha256bin.py e calcula o SHA256
        resultado_sha256 = sha256bin.calcular_sha256(caminho_arquivo)
        print(f"\nSHA-256 do arquivo: {resultado_sha256}")

        # Abre outro arquivo para comparar os sha256
        caminho_arquivo_novo = filedialog.askopenfilename(title="Escolha novamente um arquivo qualquer")

        if caminho_arquivo_novo:
            try:
                # Chama a função do arquivo sha256bin.py e calcula o SHA256
                resultado_sha256_novo = sha256bin.calcular_sha256(caminho_arquivo_novo)
                print(f"\nSHA-256 do arquivo novo: {resultado_sha256_novo}")  

            except Exception as e:
                print(f"Ocorreu um erro ao calcular o SHA256: {e}")
        else:
            print("Nenhum arquivo foi selecionado.")

    except Exception as e:
        print(f"Ocorreu um erro ao calcular o SHA256: {e}")
else:
    print("Nenhum arquivo foi selecionado.")

if resultado_sha256 == resultado_sha256_novo:
    print("\nOs arquivos são idênticos!")
else:
    print("\nO último arquivo não condiz com o primeiro!")