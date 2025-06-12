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
        self.novo_detectado = 0
        self.navios_inspecionados = []
        self.politica = politica
        self.continuar_voo = True
        self.delta_t = delta_t

        if self.politica not in ["passiva", "greed", "SA"]:
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

    def greed(self):
        detectados = [(navio.x, navio.y) for navio in self.navios_detectados]
        pontos = detectados + self.waypoints_restantes
        pontos.sort(key=lambda coord: np.hypot(coord[0] - self.x, coord[1] - self.y)) # Ordenar por distância ao VANT
        self.nodes = pontos

    def _custo_rota(self, rota):
        return sum(
            np.hypot(rota[i+1][0] - rota[i][0], rota[i+1][1] - rota[i][1])
            for i in range(len(rota) - 1)
        )

    def simulated_annealing(self):
        detectados = [(navio.x, navio.y) for navio in self.navios_detectados]
        pontos = detectados + self.waypoints_restantes

        # Ponto inicial = posição atual do VANT
        inicio = (self.x, self.y)

        # Solução inicial (ordem aleatória dos pontos)
        rota_atual = pontos[:]
        random.shuffle(rota_atual)

        if len(rota_atual) < 2: # Se não há pontos suficientes, não há rota a otimizar
            self.nodes = rota_atual 
            return

        custo_atual = self._custo_rota([inicio] + rota_atual)

        melhor_rota = rota_atual[:]
        melhor_custo = custo_atual

        # # Parâmetros do SA_old
        # T = 5000.0
        # T_min = 1e-4
        # beta = 0.95
        # iter_por_T = 100

        # Parâmetros do SA (best)
        T = 10.0
        T_min = 1e-4
        beta = 0.9
        iter_por_T = 50

        while T > T_min:
            for _ in range(iter_por_T):
                i = random.randint(0, len(rota_atual) - 2)
                j = random.randint(i + 1, len(rota_atual) - 1)
                nova_rota = rota_atual[:i] + rota_atual[i:j+1][::-1] + rota_atual[j+1:]

                novo_custo = self._custo_rota([inicio] + nova_rota)
                delta = novo_custo - custo_atual

                if delta < 0 or random.random() < np.exp(-delta / T):
                    rota_atual = nova_rota
                    custo_atual = novo_custo
                    if custo_atual < melhor_custo:
                        melhor_custo = custo_atual
                        melhor_rota = rota_atual[:]
            T *= beta

        self.nodes = melhor_rota
        
    def step(self):
        # if self.novo_detectado > 0:
        # Atualização de rota conforme política
        if self.politica == "greed":
            self.greed()
        elif self.politica == "SA":
            self.simulated_annealing()
        # self.novo_detectado = 0

        if len(self.nodes) < 1:
            self.continuar_voo = False
            return

        destino = self.nodes[0]
        dx = destino[0] - self.x
        dy = destino[1] - self.y
        dist = np.hypot(dx, dy)
        deslocamento = self.velocidade * self.delta_t / 60

        # Verificar se próximo passo ultrapassa autonomia
        proximo_odometro = self.odometro() + min(deslocamento, dist)
        if proximo_odometro >= self.autonomia:
            self.continuar_voo = False
            return

        # Atualizar posição
        if dist < deslocamento:
            self.x, self.y = destino
            self.nodes.pop(0)
            if (self.x, self.y) in self.waypoints_restantes:
                self.ultimo_wp = (self.x, self.y)
                self.waypoints_restantes.remove((self.x, self.y))
        else:
            self.x += deslocamento * dx / dist
            self.y += deslocamento * dy / dist

        self.trajeto.append((self.x, self.y))


    def odometro(self):
        if len(self.trajeto) < 2:
            return 0.0

        return sum(
            np.hypot(x2 - x1, y2 - y1)
            for (x1, y1), (x2, y2) in zip(self.trajeto[:-1], self.trajeto[1:])
    )

    def verificar_navios_proximos(self, ambiente):
        # Radar
        navios_radar = ambiente.obter_navios_em_raio(self.x, self.y, self.alcance_radar)
        for navio in navios_radar:
            if navio.estado == "nao_detectado":
                navio.estado = "detectado"
                self.navios_detectados.append(navio)
                self.novo_detectado += 1

        # Câmera
        navios_camera = ambiente.obter_navios_em_raio(self.x, self.y, self.alcance_camera)
        for navio in navios_camera:
            if navio.estado != "inspecionado":
                navio.estado = "inspecionado"
                self.navios_inspecionados.append(navio)
                if navio in self.navios_detectados:
                    self.navios_detectados.remove(navio)

