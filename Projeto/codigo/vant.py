import numpy as np

class VANT:
    def __init__(self, x=0.0, y=0.0, velocidade=60.0, autonomia=1400.0,
                 alcance_radar=100.0, alcance_camera=20.0, politica="passiva"):
        self.x = x
        self.y = y
        self.trajeto = [(x, y)]
        self.velocidade = velocidade
        self.autonomia = autonomia
        self.waypoints = []
        self.referencia = []
        self.alcance_radar = alcance_radar
        self.alcance_camera = alcance_camera
        self.navios_detectados = []
        self.navios_inspecionados = []
        self.politica = politica

        if self.politica not in ["passiva", "greed", "SA"]:
            raise ValueError(f"Política inválida: {self.politica}")

    def definir_linhas_paralelas(self, inicial, final, espacamento, num_linhas=3):
        """
        Gera uma rota com linhas horizontais paralelas.
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

    def greed(self):
        pass

    def simmulated_annealing(self):
        pass

    def step(self):
        # Atualização de rota conforme política
        if self.politica == "passiva":
            pass  # não recalcula
        elif self.politica == "greed":
            self.greed()
        elif self.politica == "SA":
            self.simmulated_annealing()
        
        if not self.waypoints or self.odometro() >= self.autonomia:
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

    def odometro(self):
        """
        Retorna a distância total percorrida pelo VANT, em milhas náuticas (MN).
        """
        if len(self.trajeto) < 2:
            return 0.0

        return sum(
            np.hypot(x2 - x1, y2 - y1)
            for (x1, y1), (x2, y2) in zip(self.trajeto[:-1], self.trajeto[1:])
    )

    def verificar_navios_proximos(self, ambiente):
        """
        Atualiza os estados dos navios próximos com base nos sensores do VANT.
        Também armazena localmente os navios detectados e inspecionados.
        Retorna uma tupla: (novos_detectados, novos_inspecionados)
        """
        # Radar
        navios_radar = ambiente.obter_navios_em_raio(self.x, self.y, self.alcance_radar)
        for navio in navios_radar:
            if navio.estado == "nao_detectado":
                navio.estado = "detectado"
                self.navios_detectados.append(navio)

        # Câmera
        navios_camera = ambiente.obter_navios_em_raio(self.x, self.y, self.alcance_camera)
        for navio in navios_camera:
            if navio.estado != "inspecionado":
                navio.estado = "inspecionado"
                self.navios_inspecionados.append(navio)
                if navio in self.navios_detectados:
                    self.navios_detectados.remove(navio)

