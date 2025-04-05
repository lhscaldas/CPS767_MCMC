from random import random
import matplotlib.pyplot as plt

def amostra_V():
    soma = 0
    contador = 0
    while soma < 1:
        x = random()
        soma += x
        contador += 1
    return contador

def estimador_E(n):
    soma = 0
    for i in range(n):
        x = amostra_V()
        soma += x
    return soma / n

def grafico_E(n_max):
    
    n_values = list(range(1, n_max + 1))
    E_values = []

    soma = 0
    for n in n_values:
        x = amostra_V()
        soma += x
        E_values.append(soma / n)

    plt.plot(n_values, E_values, label='E[V] a cada n')
    label = f'E[V] = {E_values[-1]}'
    plt.axhline(y=E_values[-1], color='r', linestyle='--', label=label)
    plt.title('Estimador de E[V] em função de n')
    plt.xlabel('n')
    plt.ylabel('E[V]')
    plt.grid(True)
    plt.legend()
    plt.show()

grafico_E(10000)