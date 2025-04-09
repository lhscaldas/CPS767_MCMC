import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, norm

# Parâmetros
n = 1000
p = 0.2
mu = n * p
sigma = np.sqrt(n * p * (1 - p))

# Intervalo de interesse
x = np.arange(150, 250)  # Valores inteiros de 150 a 250

# Distribuição Binomial (discreta)
q = binom.pmf(x, n, p)

# Distribuição Gaussiana (contínua, discretizada nos mesmos pontos)
p_vals = norm.pdf(x, mu, sigma)

# Encontrar a constante c (máximo da razão q/p)
ratio = q / p_vals
c_index = np.argmax(ratio)
c = ratio[c_index]
print(f"Constante c encontrada: {c}")
print(f"Ponto de máximo da razão: x = {x[c_index]}")
print(f"Eficiência: {1/c*100:.2f}%")

# Plot
plt.figure(figsize=(12, 6))
plt.bar(x, q, width=0.8, alpha=0.7, label=f'Binomial (n={n}, p={p})')
plt.plot(x, p_vals, 'r-', linewidth=2, label=f'Gaussiana (μ={mu}, σ²={sigma**2:.1f})')
plt.plot(x, c * p_vals, 'g--', linewidth=2, label=f'{c:.4f} × Gaussiana')

plt.title('Comparação entre Distribuição Binomial e Gaussiana')
plt.xlabel('x')
plt.ylabel('Probabilidade')

plt.legend()
plt.grid(True)
plt.show()