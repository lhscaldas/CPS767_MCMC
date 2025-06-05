import numpy as np
import random

class VANT:
    def __init__(self, x=0.0, y=0.0, velocidade=60.0, autonomia=1400.0,
                 alcance_radar=100.0, alcance_camera=20.0, politica="passiva",
                 delta_t=30):
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
        self.delta_t = delta_t

        if self.politica not in ["passiva", "greed", "greed_melhorada", "SA"]:
            raise ValueError(f"Política inválida: {self.politica}")

    def definir_linhas_paralelas(self, inicial, final, espacamento, num_linhas=3,
                                 gap=50):
        self.referencia = [inicial]
        x, y = inicial
        atual_y = y
        direita = True
        x = x + gap
        final = final - gap

        for i in range(num_linhas):
            if direita:
                self.referencia.append((final, atual_y))
            else:
                self.referencia.append((x, atual_y))
            
            if i < num_linhas - 1:
                atual_y += espacamento
                self.referencia.append((final if direita else x, atual_y))
            
            direita = not direita

        x, y = self.referencia[-1]            # pega o ponto final
        self.referencia[-1] = (x + gap, y)  # soma com o alcance do radar

        self.waypoints_restantes = self.referencia.copy()
        self.nodes = self.waypoints_restantes.copy()

    def _navio_dentro_do_retangulo(self, pos_navio, wp1, wp2, alcance_radar, K=1.0):
        x0, y0 = pos_navio
        x1, y1 = wp1
        x2, y2 = wp2

        if y1 == y2:
            # Segmento horizontal
            x_min = min(x1, x2) - alcance_radar / K
            x_max = max(x1, x2) + alcance_radar / K
            y_min = y1 - alcance_radar
            y_max = y1 + alcance_radar
        elif x1 == x2:
            # Segmento vertical
            x_min = x1 - alcance_radar
            x_max = x1 + alcance_radar
            y_min = min(y1, y2) - alcance_radar / K
            y_max = max(y1, y2) + alcance_radar / K
        else:
            raise ValueError("Segmento não é horizontal nem vertical.")

        return x_min <= x0 <= x_max and y_min <= y0 <= y_max

    def greed_melhorada(self):
        detectados = [(navio.x, navio.y) for navio in self.navios_detectados]
        ultimo_wp = self.ultimo_wp
        proximo_wp = self.waypoints_restantes[0] if len(self.waypoints_restantes)>1 else ultimo_wp
        pontos = [coord for coord in detectados if self._navio_dentro_do_retangulo(coord, ultimo_wp, proximo_wp, self.alcance_radar)] # Filtrar navios próximos à reta
        pontos.sort(key=lambda coord: np.hypot(coord[0] - self.x, coord[1] - self.y)) # Ordenar por distância ao VANT
        self.nodes = pontos + self.waypoints_restantes

    def greed(self):
        detectados = [(navio.x, navio.y) for navio in self.navios_detectados]
        pontos = detectados + self.waypoints_restantes
        pontos.sort(key=lambda coord: np.hypot(coord[0] - self.x, coord[1] - self.y)) # Ordenar por distância ao VANT
        self.nodes = pontos

    def _custo_rota(self, rota):
        custo = 0.0
        for i in range(len(rota) - 1):
            dx = rota[i+1][0] - rota[i][0]
            dy = rota[i+1][1] - rota[i][1]
            custo += np.hypot(dx, dy)
        return custo

    def simulated_annealing(self):
        detectados = [(navio.x, navio.y) for navio in self.navios_detectados]
        pontos = detectados + self.waypoints_restantes

        if not pontos:
            self.nodes = []
            return

        # Ponto inicial = posição atual do VANT
        inicio = (self.x, self.y)

        # Solução inicial (ordem aleatória dos pontos)
        rota_atual = pontos[:]
        random.shuffle(rota_atual)
        custo_atual = self._custo_rota([inicio] + rota_atual)

        melhor_rota = rota_atual[:]
        melhor_custo = custo_atual

        # Parâmetros do SA
        T = 100.0  # temperatura inicial
        T_min = 1e-3
        alpha = 0.995
        iter_por_T = 100

        while T > T_min:
            for _ in range(iter_por_T):
                # Gerar vizinho trocando dois pontos da rota
                i, j = random.sample(range(len(rota_atual)), 2)
                nova_rota = rota_atual[:]
                nova_rota[i], nova_rota[j] = nova_rota[j], nova_rota[i]

                novo_custo = self._custo_rota([inicio] + nova_rota)

                delta = novo_custo - custo_atual
                if delta < 0 or np.exp(-delta / T) > random.random():
                    rota_atual = nova_rota
                    custo_atual = novo_custo
                    if custo_atual < melhor_custo:
                        melhor_rota = rota_atual[:]
                        melhor_custo = custo_atual
            T *= alpha

        self.nodes = melhor_rota


    def step(self):
        # Atualização de rota conforme política
        if self.politica == "greed":
            self.greed()
        if self.politica == "greed_melhorada":
            self.greed_melhorada()
        elif self.politica == "SA" and self.novo_detectado:
            self.simulated_annealing()
            self.novo_detectado = False

        # Checar se continua o voo
        if len(self.nodes) < 1 or self.odometro() >= self.autonomia:
            self.continuar_voo = False
            return

        destino = self.nodes[0]
        dx = destino[0] - self.x
        dy = destino[1] - self.y
        dist = np.hypot(dx, dy)

        deslocamento = self.velocidade * self.delta_t / 60 
        if dist < deslocamento:
            self.x, self.y = destino
            self.nodes.pop(0)
            if (self.x,self.y) in self.waypoints_restantes:
                self.ultimo_wp = (self.x, self.y)
                self.waypoints_restantes.remove((self.x, self.y))
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

