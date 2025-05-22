import random

def is_valid(seq):
    """Verifica se uma sequência binária não tem 1s adjacentes."""
    return '11' not in seq

def flip_bit(seq, i):
    """Inverte o bit na posição i da sequência."""
    flipped = list(seq)
    flipped[i] = '1' if seq[i] == '0' else '0'
    return ''.join(flipped)

def get_valid_neighbors(seq):
    """Retorna todas as sequências válidas alcançáveis por um flip de um bit."""
    neighbors = []
    for i in range(len(seq)):
        flipped = flip_bit(seq, i)
        if is_valid(flipped):
            neighbors.append(flipped)
    return neighbors

# Contar o número de sequências válidas
def count_valid_sequences(s):
    """Conta o número de sequências válidas de comprimento s."""
    if s == 0:
        return 1
    if s == 1:
        return 2
    if s == 2:
        return 3
    return count_valid_sequences(s - 1) + count_valid_sequences(s - 2)

def generate_sample_path(s, steps):
    """Gera o caminho amostral de sequências válidas usando Metropolis-Hastings."""
    current = '0' * s  # Estado inicial válido
    path = []

    for _ in range(steps):
        neighbors = get_valid_neighbors(current)
        proposed = random.choice(neighbors)
        d_current = len(neighbors)
        d_proposed = len(get_valid_neighbors(proposed))

        acceptance_prob = min(1.0, d_current / d_proposed)
        if random.random() < acceptance_prob:
            current = proposed
        path.append(current)

    return path

def estimate_mu_from_path(path):
    """Estima mu_s a partir do caminho amostral."""
    ones_counts = [seq.count('1') for seq in path]
    mu_hat = sum(ones_counts) / len(ones_counts)
    return mu_hat

if __name__ == "__main__":
    for s in [4, 8, 12, 16]:
        steps = 100000
        
        sample_path = generate_sample_path(s, steps)
        mu_estimate = estimate_mu_from_path(sample_path)

        print(f"Estimativa de mu_{s}, com {count_valid_sequences(s)} sequências válidas: {mu_estimate:.4f}")
