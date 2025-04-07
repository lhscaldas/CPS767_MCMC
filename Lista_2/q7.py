import random
import string
import socket
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed

random.seed(42)  # Para reprodutibilidade

# Gerador de palavra aleatória com 1 até k letras minúsculas
def gerar_palavra_aleatoria(k):
    tamanho = random.randint(1, k)
    return ''.join(random.choices(string.ascii_lowercase, k=tamanho))

# Verifica se o domínio existe consultando o DNS
def dominio_existe(nome):
    try:
        socket.gethostbyname(f"www.{nome}.ufrj.br")
        return True
    except socket.gaierror:
        return False

# Estimativa Monte Carlo de domínios válidos
def estimar_dominios_validos(k, n_amostras):
    omega = sum([26**i for i in range(1, k+1)])
    soma = 0
    for i in range(n_amostras):
        palavra = gerar_palavra_aleatoria(k) # Gera palavra aleatória de tamanho k
        existe = dominio_existe(palavra) # Verifica se o domínio existe
        x = omega if existe else 0
        soma += x
    return soma / n_amostras

# Estimativa Monte Carlo de domínios válidos salvando E_n a cada n
def estimar_dominios_validos_com_grafico(k, n_amostras):
    omega = sum([26**i for i in range(1, k+1)])
    soma = 0
    E_n = []
    for i in range(n_amostras):
        palavra = gerar_palavra_aleatoria(k) # Gera palavra aleatória de tamanho k
        existe = dominio_existe(palavra) # Verifica se o domínio existe
        x = omega if existe else 0
        soma += x
        E_n.append(soma / (i + 1))
    return E_n

# Estimativa Monte Carlo concorrente
def estimar_dominios_validos_concorrente(k, n_amostras, max_threads=50):
    omega = sum([26**i for i in range(1, k+1)])
    soma = 0
    E_n = []
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(dominio_existe, gerar_palavra_aleatoria(k)) for _ in range(n_amostras)]

        for i, future in enumerate(as_completed(futures), 1):
            existe = future.result()
            soma += omega if existe else 0
            E_n.append(soma / i)

    return E_n

# Plotando E_n em escala semi-log
def plotar_E_n(E_n):
    plt.plot(E_n, label='$\hat{w}_n$')
    label = f' {E_n[-1]}'
    plt.axhline(y=E_n[-1], color='r', linestyle='--', label=label)
    plt.xscale('log')
    plt.title('Estimativa de D em escala semi-log')
    plt.xlabel('n')
    plt.ylabel('$\hat{w}_n$')
    plt.grid(True)
    plt.legend()
    plt.show()

# Parâmetros
k = 4
n = 1e4  # Você pode aumentar esse valor se quiser mais precisão
n = int(n)

# estimativa = estimar_dominios_validos(k, n)
# print(f"Estimativa do número de domínios válidos para k={k} com {n} amostras: {int(estimativa)}")

E_n = estimar_dominios_validos_com_grafico(k, n)
plotar_E_n(E_n)
