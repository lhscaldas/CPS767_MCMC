import numpy as np
import matplotlib.pyplot as plt

# Verificar se a matriz de transição P é estocástica
def is_stochastic(P):
    # Verifica se cada linha soma 1
    return np.all(np.isclose(np.sum(P, axis=1), 1))

# Verificar se a distribuição pi é estacionária
def is_stationary(P, pi):
    # Verifica se P @ pi = pi
    pi_next = pi @ P
    error = np.abs(pi_next - pi)
    max_err = np.max(error)
    if max_err > 1e-10:
        return {max_err}
    return True

# Verificar o erro de convergência da distribuição pi para a distribuição estacionária
def check_stationarity_error(P, pi):
    pi_next = pi @ P
    error = np.abs(pi_next - pi)
    max_err = np.max(error)
    return max_err


# Criar a matriz de transição P e a distribuição estacionária pi para um grafo em anel
def create_ring_graph(n=125):
    P = np.zeros((n, n))
    pi = np.ones(n) / n  # distribuição uniforme
    for i in range(n):
        P[i][i] = 0.5
        P[i][(i - 1) % n] = 0.25
        P[i][(i + 1) % n] = 0.25
    return P, pi

def create_tree_graph(n=127):
    P = np.zeros((n, n))
    pi = np.zeros(n)
    for i in range(n):
        if i == 0:  # raiz (i=1)
            pi[i] = 1 / 126
            for j in [1, 2]:  # filhos: 2, 3
                P[i][j] = 0.25
            P[i][i] = 0.5
        elif 1 <= i <= int(n/2)-1:  # nós internos (i ∈ {2,...,63})
            pi[i] = 1 / 84
            parent = (i - 1) // 2
            children = [2 * i + 1, 2 * i + 2]
            for j in [parent] + [c for c in children if c < n]:
                P[i][j] = 1 / 6
            P[i][i] = 0.5
        else:  # folhas (i ∈ {64,...,127})
            pi[i] = 1 / 252
            parent = (i - 1) // 2
            P[i][parent] = 0.5
            P[i][i] = 0.5
    return P, pi

def create_grid_graph(k=11):
    n = k * k
    P = np.zeros((n, n))
    pi = np.zeros(n)
    for r in range(k): # linha
        for c in range(k): # coluna
            i = r * k + c # índice do vértice
            neighbors = []
            if r > 0: neighbors.append((r - 1) * k + c)
            if r < k - 1: neighbors.append((r + 1) * k + c)
            if c > 0: neighbors.append(r * k + (c - 1))
            if c < k - 1: neighbors.append(r * k + (c + 1))
            # Tipo do vértice
            if (r, c) in [(0, 0), (0, k - 1), (k - 1, 0), (k - 1, k - 1)]: # canto
                pi[i] = 1 / 220
                prob = 1 / 4
            elif r in [0, k - 1] or c in [0, k - 1]: # borda
                pi[i] = 3 / 440
                prob = 1 / 6
            else: # interior
                pi[i] = 1 / 110
                prob = 1 / 8
            for j in neighbors:
                P[i][j] = prob
            P[i][i] = 0.5
    return P, pi

def plot_total_variation_distance(pi_0, pi_stationary, P, tipo, t_max=int(1e5)):
    d_tv_list = []
    pi_t = pi_0.copy()
    for t in range(1, t_max + 1):
        pi_t = pi_t @ P
        d_tv = 0.5 * np.sum(np.abs(pi_t - pi_stationary))
        d_tv_list.append(d_tv)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, t_max + 1), d_tv_list)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('t (log scale)')
    plt.ylabel('Total Variation Distance (log scale)')
    plt.title(f"Convergência para a distribuição estacionária do grafo em {tipo}")
    plt.grid(True, which="both", ls="--")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Para o anel:
    pi_0 = np.zeros(125)
    pi_0[0] = 1  # distribuição inicial
    P, pi = create_ring_graph()
    print("Matriz de transição P é estocástica para o anel?", is_stochastic(P))
    print("Distribuição pi é estacionária para o anel?", is_stationary(P, pi))
    # plot_total_variation_distance(pi_0, pi, P, "anel")

    # Para a árvore:
    pi_0 = np.zeros(127)
    pi_0[0] = 1  # distribuição inicial
    P, pi = create_tree_graph()
    print("Matriz de transição P é estocástica para a árvore?", is_stochastic(P))
    print("Distribuição pi é estacionária para a árvore?", is_stationary(P, pi))
    plot_total_variation_distance(pi_0, pi, P, "árvore binária cheia")

    # Para a grade:
    pi_0 = np.zeros(121)
    pi_0[0] = 1  # distribuição inicial
    P, pi = create_grid_graph()
    print("Matriz de transição P é estocástica para a grade?", is_stochastic(P))
    print("Distribuição pi é estacionária para a grade?", is_stationary(P, pi))
    # plot_total_variation_distance(pi_0, pi, P, "grade 2D")







