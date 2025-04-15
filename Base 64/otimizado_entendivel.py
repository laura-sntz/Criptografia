import time

def codificar_base64(mensagem):
    binario = ""
    for c in mensagem:
        binario += f'{ord(c):08b}'  # Converte para binário
    
    while len(binario) % 6 != 0:
        binario += '0'  # Preenche até múltiplo de 6
    
    caracteres_base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    resultado = ""
    
    for i in range(0, len(binario), 6):
        resultado += caracteres_base64[int(binario[i:i+6], 2)]
    
    while len(resultado) % 4 != 0:
        resultado += "="  # Preenchendo com '='
    
    return resultado

def decodificar_base64(codificado):
    caracteres_base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    codificado = codificado.rstrip("=")  # Remove preenchimento
    
    binario = ""
    for c in codificado:
        binario += f'{caracteres_base64.index(c):06b}'  # Procura c na base64 e converte em binário de 6 bits
    
    mensagem = ""
    for i in range(0, len(binario), 8): # i vai de 0 até o tamanho do binário total com um passo de 8
        mensagem += chr(int(binario[i:i+8], 2)) # transforma o binário de 6 bits em inteiro, pulando de 8 em 8 bits. Depois, transforma o inteiro em caractere.  
    
    return mensagem

# Entrada do usuário
txt = input("Digite a palavra para codificar: ")

inicio = time.time()

codificado = codificar_base64(txt)
decodificado = decodificar_base64(codificado)

print("Codificado:", codificado)
print("Decodificado:", decodificado)

fim = time.time()

print(f"Tempo de execução: {fim - inicio:.6f} segundos")