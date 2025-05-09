import numpy as np

# Verificar se a matriz de transição P é estocástica
def is_stochastic(P):
    # Verifica se cada linha soma 1
    return np.all(np.isclose(np.sum(P, axis=1), 1))

# Calcular a matriz de transição
def transition_matrix(n, p):
    P = np.zeros((n, n))

    for i in range(n):
        if i < n - 1:
            P[i, 0] = 1 - p       # Volta ao estado 1 (índice 0)
            P[i, i + 1] = p       # Avança para o próximo estado
        else:
            P[i, 0] = 1 - p       # Volta ao estado 1
            P[i, i] = p           # Permanece no último estado

    return P

def spectral_gap(P):
    eigvals = np.linalg.eigvals(P)
    eigvals = np.flip(np.sort(np.abs(eigvals)))  # ordenar em valor absoluto decrescente
    return eigvals, 1 - eigvals[1]  # gap = 1 - |lambda_2|
    # return eigvals, eigvals[0] - eigvals[1]  # gap = 1 - |lambda_2|

def item_2():
    for p in [0.25, 0.5, 0.75]:
        P = transition_matrix(10, p)
        eigvals, gap = spectral_gap(P)
        print(f"p = {p}:")
        # print("Matriz de transição:")
        # print(P)
        # print("Verificação de estocasticidade:", is_stochastic(P))
        # print("Módulo dos autovalores:", eigvals)
        print("Vão espectral:", gap)

def stationary_distribution(P):
    eigvals, eigvecs = np.linalg.eig(P.T)  # autovalores/vetores à esquerda
    idx = np.argmin(np.abs(eigvals - 1))  # índice do autovalor mais próximo de 1
    pi = np.real(eigvecs[:, idx])         # pega a parte real do autovetor
    pi = pi / np.sum(pi)                  # normaliza para soma 1

    return pi

# Verificar se a distribuição pi é estacionária
def is_stationary(P, pi):
    # Verifica se P @ pi = pi
    pi_next = pi @ P
    error = np.abs(pi_next - pi)
    max_err = np.max(error)
    if max_err > 1e-10:
        return max_err
    return True

def item_3():
    for p in [0.25, 0.5, 0.75]:
        P = transition_matrix(10, p)
        pi = stationary_distribution(P)
        print(f"p = {p}:")
        print("Distribuição estacionária:")
        print(pi)
        # print("Verificação de estacionariedade:")
        # print(is_stationary(P, pi))

# Calcular os limites inferior e superior do tempo de mistura
def mixing_time_bounds(P, epsilon=1e-6):
    _, delta = spectral_gap(P)
    pi = stationary_distribution(P)
    pi_o = np.min(pi)
    L_inf = (1/delta - 1) * np.log(1/(2*epsilon))  # limite inferior
    L_sup = (1/delta) * np.log(1/(pi_o*epsilon))  # limite superior
    return L_inf, L_sup

def item_4():
    for p in [0.25, 0.5, 0.75]:
        P = transition_matrix(10, p)
        L_inf, L_sup = mixing_time_bounds(P)
        print(f"p = {p}:")
        print("Limite inferior do tempo de mistura:", L_inf)
        print("Limite superior do tempo de mistura:", L_sup)

if __name__ == "__main__":
    item_2()