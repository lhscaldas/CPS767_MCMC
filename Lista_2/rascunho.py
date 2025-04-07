import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

# plotar a função de densidade de probabilidade da distribuição binomial para diferentes valores de n e p
def plotar_binomial(n, p):
    x = np.linspace(0, n + 1, 100)
    y = comb(n, x) * (p ** x) * ((1 - p) ** (n - x))
    plt.plot(x, y, linestyle='-', label=f'n={n}, p={p}')

    plt.title('Distribuição Binomial')
    plt.xlabel('x')
    plt.ylabel('P(X = x)')
    plt.legend()
    plt.grid(True)

# # plotagem das distribuições
# plotar_binomial(20, 0.3)
# plotar_binomial(20, 0.5)
# plotar_binomial(20, 0.7)

# # mostrar o gráfico após as duas chamadas
# plt.show()

mu = 200
sigma = 12.65
print(f" {mu-4*sigma} < X < {mu+4*sigma}")
