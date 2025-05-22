from math import comb

n = 2
p1 = 0.1
p2 = 0.8
alpha = 0.3  # P(K=1)

def P_X_given_K(x, k):
    if x < 0 or x > n:
        return 0.0
    if k == 1:
        p = p1
    elif k == 2:
        p = p2
    else:
        raise ValueError("k must be 1 or 2")
    
    return comb(n, x) * (p ** x) * ((1 - p) ** (n - x))

def P_K_given_X(k, x):
    if k not in [1, 2]:
        raise ValueError("k must be 1 or 2")
    if x < 0 or x > n:
        return 0.0

    # Prior
    P_K = alpha if k == 1 else (1 - alpha)

    # Likelihood
    likelihood = P_X_given_K(x, k)

    # Marginal
    px = alpha * P_X_given_K(x, 1) + (1 - alpha) * P_X_given_K(x, 2)

    return (likelihood * P_K) / px if px > 0 else 0.0

for k in [1, 2]:
    for x in range(3):
        print(f"P(X={x} | K={k}) = {P_X_given_K(x, k):.4f}")

for x in range(3):
    for k in [1, 2]:
        print(f"P(K={k} | X={x}) = {P_K_given_X(k,x):.4f}")