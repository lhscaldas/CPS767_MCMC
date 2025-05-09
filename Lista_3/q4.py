import random

# Simula o caminho amostral
def simular_caminho(p, t):
    X_0 = (1, 1)  # Estado inicial
    X = [X_0]     # Lista para armazenar o caminho amostral

    for _ in range(t):
        i, j = X[-1]  # Último estado
        vizinhos = [
        (i + 1, j),         # Norte
        (i, j + 1),         # Leste
        (i - 1, j) if i > 1 else (i, j),  # Sul ou borda inferior
        (i, j - 1) if j > 1 else (i, j)   # Oeste ou borda esquerda
    ]
        probs = [p/2, p/2, (1-p)/2, (1-p)/2] # Probabilidades
        X_new = random.choices(vizinhos, weights=probs)[0]  # Próximo estado
        X.append(X_new)
    return X

# Estima a probabilidade estacionária estado (1, 1)
def estimar_pi_11(X):
    visitas = sum(1 for estado in X if estado == (1, 1))
    return visitas / len(X)

def item_2():
    p_list = [0.25, 0.35, 0.45]
    for p in p_list:
        X = simular_caminho(p, t=int(1e7))
        pi_11 = estimar_pi_11(X)
        print(f"p = {p}, pi_11 = {pi_11:.4f}")
        print()

# Calcula a distância de Manhattan para a origem
def distancia_manhattan(X):
    i, j = X[11] # t = 10, pois começa em t=0
    d_10 = abs(i) + abs(j)
    i, j = X[101] # t = 100, pois começa em t=0
    d_100 = abs(i) + abs(j)
    i, j = X[1001] # t = 1000, pois começa em t=0
    d_1000 = abs(i) + abs(j)
    return [d_10, d_100, d_1000]

def item_3():
    p_list = [0.25, 0.35, 0.45]
    for p in p_list:
        dt_list = []
        for _ in range(30):
            X = simular_caminho(p, t=1001)
            dt_list.append(distancia_manhattan(X))
        d_t = [sum(d[0] for d in dt_list) / len(dt_list),
                sum(d[1] for d in dt_list) / len(dt_list),
                sum(d[2] for d in dt_list) / len(dt_list)]
        print(f"p = {p}, d_10 = {d_t[0]}, d_100 = {d_t[1]}, d_1000 = {d_t[2]}")
        print()

if __name__ == "__main__":
    item_3()
