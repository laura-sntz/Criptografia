import time

# -------------CODIFICAÇÃO---------------

palavra = input('Digite a palavra desejada: ')

inicio = time.time()

# Converte as letras para ASCII e depois binário
juncao = ''

# ord() transforma caractere em unicode (ASCII)
# bin() transforma decimal em binário
for letra in palavra:
    binario = bin(ord(letra)).replace("0b", "0")
    binario = binario.rjust(8, '0')
    juncao += binario

# Adicionando 0 para não múltiplos de 3
# Variável para ver se colocar = no final
usou16 = False
usou8 = False
if len(palavra) % 3 == 1:
    usou16 = True
    juncao += '0000000000000000'
elif len(palavra) % 3 == 2:
    usou8 = True
    juncao += '00000000'

# Separa os 24 bits em 4 blocos de 6 bits cada
contador = 0
lista = []
seis = ''
for numero in juncao:
    seis += numero
    contador+=1
    if contador == 6:
        lista.append(seis)
        seis = ''
        contador = 0

# Transforma cada bloco de 6 bits em decimal
lista_convertido = []
for binario in lista:
    lista_convertido.append(int(binario, 2))

# Valores da base 64
valores = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: 'a', 27: 'b', 28: 'c', 29: 'd', 30: 'e', 31: 'f', 32: 'g', 33: 'h', 34: 'i', 35: 'j', 36: 'k', 37: 'l', 38: 'm', 39: 'n', 40: 'o', 41: 'p', 42: 'q', 43: 'r', 44: 's', 45: 't', 46: 'u', 47: 'v', 48: 'w', 49: 'x', 50: 'y', 51: 'z', 52: '0', 53: '1', 54: '2', 55: '3', 56: '4', 57: '5', 58: '6', 59: '7', 60: '8', 61: '9', 62: '+', 63: '/'}

# Conversão de decimal para letra
palavra_final = ''
for numero in lista_convertido:
    if numero in valores:
        palavra_final += valores[numero]

if usou8:
    palavra_final = palavra_final.removesuffix('A')
    palavra_final += '='
elif usou16: 
    palavra_final = palavra_final.removesuffix('AA') 
    palavra_final += '=='

print(f"Palavra codificada: {palavra_final}")

# -------------DESCODIFICAÇÃO---------------

# Inverter o dicionário para as chaves serem as letras
valores_invertidos = {v: k for k, v in valores.items()}

# Se adicionou + 8 bits coloca A
# Se adicionou + 16 bits coloca AA
if usou8:
    palavra_final = palavra_final.removesuffix('=')
    palavra_final += 'A'
elif usou16: 
    palavra_final = palavra_final.removesuffix('==') 
    palavra_final += 'AA'

# Transforma as letras em números da base64
num_base64 = []
for letra in palavra_final:
    if letra in valores_invertidos:
        num_base64.append(valores_invertidos[letra]) 

# Transforma os números da base 64 em cadeias de 6 bits
num6bit = ''
for num in num_base64:
    numero = bin(num)[2:]
    if len(numero) != 6:
        # Adiciona zeros a esqeurda até len ser 6
        numero = numero.rjust(6, '0')
    num6bit+= numero

# Transforma as cadeias de 6 bits em cadeias de 8 bits
num8bit = []
contador = 0
numero = ''
for num in num6bit:
    contador+=1
    numero += num
    if contador == 8:
        num8bit.append(numero)
        numero = ''
        contador = 0

# Transforma as cadeias de 8 bits em decimais
decimal = []
for num in num8bit:
    decimal.append(int(num, 2))

# Transforma os decimais(unicode) para caractere
# chr(): de unicode(valor ASCII) para caractere
palavra_descodificada = ''
for num in decimal:
    palavra_descodificada += chr(num)

print(f"Palavra descodificada: {palavra_descodificada}")

fim = time.time()

print(f"Tempo de execução: {fim - inicio:.6f} segundos")