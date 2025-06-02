import numpy as np

class VANT:
    def __init__(self, x=0.0, y=0.0, velocidade=60.0, autonomia=900.0,
                 alcance_radar=100.0, alcance_camera=20.0):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.autonomia = autonomia
        self.alcance_radar = alcance_radar
        self.alcance_camera = alcance_camera
        self.waypoints = []
        self.referencia = []
        self.trajeto = [(x, y)]

    def definir_linhas_paralelas(self, inicial, final, espacamento, num_linhas=3):
        """
        Gera uma rota em zigue-zague com linhas horizontais paralelas.
        Começa no ponto inicial e alterna o sentido a cada linha.

        Parâmetros:
        - inicial: (x, y) início da primeira linha
        - final: valor de x final para cada linha
        - espacamento: espaço vertical entre as linhas (em y)
        - num_linhas: número total de linhas
        """
        self.referencia = [inicial]
        x, y = inicial
        atual_y = y
        direita = True

        for i in range(num_linhas):
            if direita:
                self.referencia.append((final, atual_y))
            else:
                self.referencia.append((x, atual_y))
            
            if i < num_linhas - 1:
                atual_y += espacamento
                self.referencia.append((final if direita else x, atual_y))
            
            direita = not direita

        self.waypoints = self.referencia.copy()

    def step(self):
        if not self.waypoints:
            return

        destino = self.waypoints[0]
        dx = destino[0] - self.x
        dy = destino[1] - self.y
        dist = np.hypot(dx, dy)

        if dist < self.velocidade:
            self.x, self.y = destino
            self.waypoints.pop(0)
        else:
            self.x += self.velocidade * dx / dist
            self.y += self.velocidade * dy / dist

        self.trajeto.append((self.x, self.y))
