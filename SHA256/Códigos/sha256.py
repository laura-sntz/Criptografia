# Transforma o texto inserido em binário
def texto_para_binario(frase):
    frase_bin = ''
    for letra in frase:
        frase_bin += bin(ord(letra)).removeprefix('0b').rjust(8, '0')
    return frase_bin

# Pega o tamanho do texto inserido e transforma em binário
def tamanho_frase(frase):
    # O enconde retorna os bytes ocupados. Multiplica por 8 pois cada byte ocupada 8 bits.
    #return bin(len(frase.encode('utf-8'))*8).removeprefix('0b').rjust(64, '0')
    return bin(len(texto_para_binario(frase))).removeprefix('0b').rjust(64, '0')

# Completa o resto da frase em binário com 0s e junta com o tamanho binário
def padding_juncao(frase_binario, tamanho_frase_bin):
    frase_binario = frase_binario + '1'
    num = int((len(frase_binario)+64)/512)+1;
    num = 512*num

    while len(frase_binario) != (num - 64):
        frase_binario += '0'

    return frase_binario+tamanho_frase_bin

# Separação das chunks por bloco de 512 bits cada
def separa_bloco(frase_padding):
    blocos = []

    for i in range(0, len(frase_padding), 512):
        blocos.append(frase_padding[i:i+512])

    return blocos

# Faz as 16 palavras de 32 bits cada por bloco
def palavra_32bits(bloco_unitario):
    palavras = []

    for i in range(0, len(bloco_unitario), 32):
        palavras.append(bloco_unitario[i:i+32])

    return palavras

# i >= 16
# palavra0 =  palavra[i-15]
# palavra1 = palavra[i-2]
def rotacoes(palavra0, palavra1):
    # Rotação σ_0(x)
    rotacao7 = int((palavra0[(32-7):] + palavra0[:(32-7)]), 2)
    rotacao18 = int((palavra0[(32-18):] + palavra0[:(32-18)]), 2)
    deslocamento3 = int(palavra0, 2) >> 3

    # ^ = XOR
    palavra0 = rotacao7 ^ rotacao18 ^ deslocamento3

    # Rotação σ_1(x)
    rotacao17 = int(palavra1[(32-17):] + palavra1[:(32-17)] , 2)
    rotacao19 = int(palavra1[(32-19):] + palavra1[:(32-19)] , 2)
    deslocamento10 = int(palavra1 , 2) >> 10

    palavra1 = rotacao17 ^ rotacao19 ^ deslocamento10

    return palavra0, palavra1

# i >= 16
# palavra[i] = palavra[i-16] + palavra0 + palavra[i-7] + palavra1
def expansao_mensagem(palavras):
    for i in range(len(palavras), 64):
        palavra0, palavra1 = rotacoes(palavras[i-15], palavras[i-2])
        palavra_nova = int(palavras[i-16],2) + palavra0 + int(palavras[i-7], 2) + palavra1
        
        palavra_nova = bin(palavra_nova)[2:].rjust(32, '0')

        # Estava tendo excesso de bits por conta da soma das palavras, com isso, eu retirei esse excesso (diferença de tamanho da palavra que quero inserir para 32 bits)
        palavras.append(palavra_nova[(len(palavra_nova) % 32):])
    
    return palavras

def primo(numero):
    # Não precisa procurar um divisor até o número, só apenas até a raiz dele+1. 
    for i in range(2, int(numero**0.5)+1):
        if numero % i == 0:
            return False
        
    return True

def hash_inicial():
    # Registradores de 32 bits
    H = [
        bin(0x6a09e667)[2:].rjust(32, '0'),
        bin(0xbb67ae85)[2:].rjust(32, '0'),
        bin(0x3c6ef372)[2:].rjust(32, '0'),
        bin(0xa54ff53a)[2:].rjust(32, '0'),
        bin(0x510e527f)[2:].rjust(32, '0'),
        bin(0x9b05688c)[2:].rjust(32, '0'),
        bin(0x1f83d9ab)[2:].rjust(32, '0'),
        bin(0x5be0cd19)[2:].rjust(32, '0')
    ]

    return H

def constante_K():
    K = []
    numero = 2

    # 64 primeiros números primos 
    while(len(K) != 64):
        if(primo(numero)):
            K.append(numero)
        numero+=1

    for i in range(0, 64):
        numero = pow(K[i], 1/3) # Raiz cúbica sem biblioteca
        numero = int((numero - int(numero)) * 2**32)   # Pegando a parte fracionária e multiplicando por 2^32 para dar 32 bits
        K[i] = bin(numero)[2:].rjust(32, '0')

    return K

def somatorios_majoritario_escolha(a, b, c, e, f, g):
    # Fazendo as rotações de 'e' e somatório 1
    rotacao6 = int((e[(32-6):] + e[:(32-6)]), 2)
    rotacao11 = int((e[(32-11):] + e[:(32-11)]), 2)
    rotacao25 = int((e[(32-25):] + e[:(32-25)]), 2)

    somatorio1 = rotacao6 ^ rotacao11 ^ rotacao25

    # Fazendo rotações de 'a' e somatório 0
    rotacao2 = int((a[(32-2):] + a[:(32-2)]), 2)
    rotacao13 = int((a[(32-13):] + a[:(32-13)]), 2)
    rotacao22 = int((a[(32-22):] + a[:(32-22)]), 2)

    somatorio0 = rotacao2 ^ rotacao13 ^ rotacao22

    # Fazendo as variáveis de trabalho virarem inteiros 
    a = int(a,2)
    b = int(b,2)
    c = int(c,2)
    e = int(e,2)
    f = int(f,2)
    g = int(g,2)

    # Fazendo majority
    majoritario = (a & b) ^ (a & c) ^ (b & c)

    # Fazendo choice
    escolha = (e & f) ^ ((~ e) & g)
 
    return somatorio0, somatorio1, majoritario, escolha

def variaveis_trabalho(palavras_expandidas, H):
    K = constante_K()

    a = H[0]
    b = H[1]
    c = H[2]
    d = H[3]
    e = H[4]
    f = H[5]
    g = H[6]
    h = H[7]

    for i in range(0, 64):
        somatorio0, somatorio1, majoritario, escolha = somatorios_majoritario_escolha(a, b, c, e, f, g)

        Temp1 = int(h,2) + somatorio1 + escolha + int(K[i], 2) + int(palavras_expandidas[i], 2)
        Temp2 = somatorio0 + majoritario

        h = g
        g = f
        f = e
        e = bin(int(d,2) + Temp1)[2:].rjust(32,'0')
        d = c
        c = b
        b = a
        a = bin(Temp1 + Temp2)[2:].rjust(32, '0')

        a = a[len(a) % 32:]
        b = b[len(b) % 32:]
        c = c[len(c) % 32:]
        d = d[len(d) % 32:]
        e = e[len(e) % 32:]
        f = f[len(f) % 32:]
        g = g[len(g) % 32:]
        h = h[len(h) % 32:]

    ultimas_variaveis = [a, b, c, d, e, f, g, h]

    return ultimas_variaveis

# Mexer aqui para outros blocos
def primeiro_hash(ultimas_variaveis):
    H = hash_inicial()
    
    for i in range(0, 8):
        H[i] = bin(int(H[i], 2) + int(ultimas_variaveis[i], 2))[2:].rjust(32,'0')
        H[i] = (H[i])[len(H[i]) % 8:]
    
    return H

def outros_hashs(ultimas_variaveis, H):
    for i in range(0, 8):
        H[i] = bin(int(H[i], 2) + int(ultimas_variaveis[i], 2))[2:].rjust(32,'0')
        H[i] = (H[i])[len(H[i]) % 8:]
    
    return H

def sha256(H, ultimas_variaveis):
    sha256 = ''
    
    for i in range(0, 8):
        H[i] = hex(int(H[i], 2) + int(ultimas_variaveis[i], 2))

    for i in range(0, 8):
        sha256 += (H[i])[len(H[i]) % 8:]
    
    return sha256

# -----------------------------------------------------------
# Para botar na main depois

frase = input('Digite a frase desejada: ')
frase_binario = texto_para_binario(frase)
tamanho_frase_bin = tamanho_frase(frase)
frase_padding = padding_juncao(frase_binario, tamanho_frase_bin)
blocos = separa_bloco(frase_padding)

for i in range(len(blocos)):
    palavras = palavra_32bits(blocos[i]);
    palavras_expandidas = expansao_mensagem(palavras)

    if len(blocos) == 1:
        H = hash_inicial()
        ultimas_variaveis = variaveis_trabalho(palavras_expandidas, H)
    elif i == 0 and len(blocos) != 1:
        ultimas_variaveis = variaveis_trabalho(palavras_expandidas, hash_inicial())
        H = primeiro_hash(ultimas_variaveis)
    else:
        ultimas_variaveis = variaveis_trabalho(palavras_expandidas, H)
       
print(sha256(H, ultimas_variaveis))