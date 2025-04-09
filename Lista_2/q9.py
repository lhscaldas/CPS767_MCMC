import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt

# Definindo a função a ser integrada
def g(x):
    return np.exp(-x**2)

def monte_carlo_integration(a, b, n):
    soma=0
    for i in range(n):
        x = np.random.uniform(a, b)
        y = g(x)
        soma += y
    return soma/n

def is_integration(a, b, n):
    A = 1/(1 - np.exp(-1))
    print(f"A: {A:.6f}")
    soma=0
    for i in range(n):
        U = np.random.uniform(a, b)
        x = np.log(A)-np.log(A-U)
        soma += g(x) * np.exp(x)
    return soma/(n*A)

def plot_function(n, I):
    A = 1/(1 - np.exp(-1))
    soma_mc=0
    soma_is=0
    erro_mc=[]
    erro_is=[]
    for i in range(n):
        # Gerando um número aleatório U entre 0 e 1 
        U = np.random.uniform(0, 1)
        # Calculando a integral pelo método de Monte Carlo
        x_mc = U
        soma_mc += g(x_mc)
        I_mc = soma_mc/(i+1)
        erro_mc.append(abs(I-I_mc)/I)
        # Calculando a integral pelo método de Monte Carlo com importance sampling
        x_is = np.log(A)-np.log(A-U)
        soma_is += g(x_is) * np.exp(x_is)
        I_is = soma_is/((i+1)*A)
        erro_is.append(abs(I-I_is)/I)

    # Plotando os erros relativos
    plt.plot(erro_mc, label='Monte Carlo Simples')
    plt.plot(erro_is, label='Monte Carlo com Importance Sampling')
    plt.xscale('log')
    plt.xlabel('Número de amostras')
    plt.ylabel('Erro relativo')
    plt.title('Erro relativo da integração numérica')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    # Calculando a integral pela Regra de Simpson
    n = int(1e6)
    x=np.linspace(0, 1, int(1e3))
    I = spi.simpson(g(x), x)
    print(f"Simpson: {I:.6f}")

    # Calculando a integral pelo Método de Monte Carlo
    n = int(1e3)
    I_mc = monte_carlo_integration(0, 1, n)
    print(f"Monte Carlo: {I_mc:.6f}")
    print(f"Erro relativo MC: {abs(I-I_mc)/I*100:.2f}\%")

    #Usando importance sampling
    n = int(1e3)
    I_is = is_integration(0, 1, n)
    print(f"Importance Sampling: {I_is:.6f}")
    print(f"Erro relativo IS: {abs(I-I_is)/I*100:.2f}\%")

    # Plotando os erros relativos
    n = int(1e6)
    plot_function(n, I)