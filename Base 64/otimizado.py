import time

def texto_para_base64(texto: str) -> str:
    #Codifica uma string para Base64
    binario = ''.join(format(ord(letra), '08b') for letra in texto)
    
    # Preenchimento de bits para múltiplos de 6
    preenchimento = (6 - len(binario) % 6) % 6
    binario += '0' * preenchimento
    
    # Divide os bits em grupos de 6
    indices = [int(binario[i:i+6], 2) for i in range(0, len(binario), 6)]
    
    # Mapeamento Base64
    tabela_base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    base64 = ''.join(tabela_base64[i] for i in indices)
    
    # Adiciona '=' se necessário
    caractere_preenchimento = '=' * ((4 - len(base64) % 4) % 4)
    return base64 + caractere_preenchimento


def base64_para_texto(base64_texto: str) -> str:
    """Decodifica uma string Base64 para texto normal."""
    tabela_base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    base64_texto = base64_texto.rstrip('=')
    
    # Converte caracteres em índices da tabela Base64
    binario = ''.join(format(tabela_base64.index(c), '06b') for c in base64_texto)
    
    # Remove bits extras adicionados pelo preenchimento
    binario = binario[:len(binario) - (len(binario) % 8)]
    
    # Converte blocos de 8 bits em caracteres
    texto = ''.join(chr(int(binario[i:i+8], 2)) for i in range(0, len(binario), 8))
    return texto


# Teste da codificação e decodificação
palavra = input('Digite a palavra desejada: ')

inicio = time.time()

codificada = texto_para_base64(palavra)
print(f"Palavra codificada: {codificada}")

descodificada = base64_para_texto(codificada)
print(f"Palavra descodificada: {descodificada}")

fim = time.time()

print(f"Tempo de execução: {fim - inicio:.6f} segundos")