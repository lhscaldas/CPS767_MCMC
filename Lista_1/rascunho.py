import numpy as np
import math

# k=10
# mu=10
# t=1

# P=np.exp(-mu*t)*((mu*t)**k)/math.factorial(k)

# # formata P em notação científica
# P = "{:.2e}".format(P)
# print(P)
# print(math.factorial(k))

# print(12*np.log(10))

n = (1+np.sqrt(1+4*730*np.log(2)))/2
print(n)
print(365/n)