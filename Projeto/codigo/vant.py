import numpy as np

class VANT:
    def __init__(self, x=0.0, y=0.0, velocidade=60.0, autonomia=1400.0,
                 alcance_radar=100.0, alcance_camera=20.0, politica="passiva"):
        self.x = x
        self.y = y
        self.trajeto = [(x, y)]
        self.ultimo_wp= (x, y)
        self.velocidade = velocidade
        self.autonomia = autonomia
        self.referencia = []
        self.waypoints_restantes = []
        self.nodes = []
        self.alcance_radar = alcance_radar
        self.alcance_camera = alcance_camera
        self.navios_detectados = []
        self.novo_detectado = False
        self.navios_inspecionados = []
        self.politica = politica
        self.continuar_voo = True

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

        self.waypoints_restantes = self.referencia.copy()
        self.nodes = self.waypoints_restantes.copy()

    def distancia_navio_para_reta(self, pos_navio, wp1, wp2):
        x0, y0 = pos_navio
        x1, y1 = wp1
        x2, y2 = wp2

        numerador = abs((x2 - x1)*(y1 - y0) - (x1 - x0)*(y2 - y1))
        denominador = np.hypot(x2 - x1, y2 - y1)

        if denominador == 0:
            # wp1 e wp2 coincidem — considera distância direta ao ponto
            return np.hypot(x0 - x1, y0 - y1)

        return numerador / denominador

    def obter_pontos_politica(self):
        """
        Retorna os pontos relevantes para a política.
        """
        detectados = [(navio.x, navio.y) for navio in self.navios_detectados]
        proximo_wp = self.waypoints_restantes[0]
        ultimo_wp = self.ultimo_wp
        pontos = [coord for coord in detectados if self.distancia_navio_para_reta(coord, ultimo_wp, proximo_wp) <= self.alcance_radar] # Filtrar navios próximos à reta
        pontos.append(proximo_wp) # Adicionar o próximo waypoint
        return pontos

    def greed(self):
        pontos = self.obter_pontos_politica()
        pontos.sort(key=lambda coord: np.hypot(coord[0] - self.x, coord[1] - self.y)) # Ordenar por distância ao VANT
        self.nodes = pontos + self.waypoints_restantes[1:] # Adicionar os outros waypoints restantes

    def simulated_annealing(self):
        pass

    def step(self, delta_t=10):
        # Checar se continua o voo
        if not self.nodes or self.odometro() >= self.autonomia:
            self.continuar_voo = False
            return

        # Atualização de rota conforme política
        if self.novo_detectado:
            if self.politica == "greed":
                self.greed()
            elif self.politica == "SA":
                self.simulated_annealing()
            self.novo_detectado = False

        destino = self.nodes[0]
        dx = destino[0] - self.x
        dy = destino[1] - self.y
        dist = np.hypot(dx, dy)

        deslocamento = self.velocidade * delta_t / 60 
        if dist < deslocamento:
            self.x, self.y = destino
            self.nodes.pop(0)
            if (self.x,self.y) in self.waypoints_restantes:
                self.ultimo_wp = (self.x, self.y)
                self.waypoints_restantes.pop(0)
        else:
            self.x += deslocamento * dx / dist # deslocamento * cos(direção)
            self.y += deslocamento * dy / dist # deslocamento * sin(direção)

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
                self.novo_detectado = True

        # Câmera
        navios_camera = ambiente.obter_navios_em_raio(self.x, self.y, self.alcance_camera)
        for navio in navios_camera:
            if navio.estado != "inspecionado":
                navio.estado = "inspecionado"
                self.navios_inspecionados.append(navio)
                if navio in self.navios_detectados:
                    self.navios_detectados.remove(navio)

