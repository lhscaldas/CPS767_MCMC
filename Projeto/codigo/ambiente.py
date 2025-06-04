import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import RegularPolygon
import matplotlib.patches as patches


@dataclass
class Navio:
    x: float
    y: float
    estado: str = "nao_detectado"  # 'nao_detectado', 'detectado', 'inspecionado'

class AmbienteMaritimo:
    def __init__(self, largura=350.0, altura=400.0, num_navios=20):
        self.largura = largura
        self.altura = altura
        self.num_navios = num_navios
        self.navios = []
        self.gerar_navios()

    def gerar_navios(self):
        np.random.seed(42)  # Para reprodutibilidade
        self.navios = [
            Navio(
                x=np.random.uniform(0, self.largura),
                y=np.random.uniform(0, self.altura)
            )
            for _ in range(self.num_navios)
        ]
    
    def obter_navios_em_raio(self, x, y, raio):
        """
        Retorna a lista de navios dentro de um raio específico da posição (x, y).
        """
        navios_proximos = []
        for navio in self.navios:
            distancia = np.hypot(navio.x - x, navio.y - y)
            if distancia <= raio:
                navios_proximos.append(navio)
        return navios_proximos
    
    def simular(self, vant):
        vant.step(delta_t=30) 
        vant.verificar_navios_proximos(self)

    def plotar_cenario(self, vant=None):
        if vant is not None:
            while vant.continuar_voo:
                self.simular(vant)

        fig, ax = plt.subplots(figsize=(8, 6))

        self._plotar_elementos_cenario(ax, vant)
        self._configurar_eixos(ax, vant)
        fig.tight_layout()
        plt.show()

    def animar_cenario(self, vant, filename="output.gif"):
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.subplots_adjust(right=0.75)

        def update(frame):
            ax.clear()
            if vant.continuar_voo:
                self.simular(vant)

            self._plotar_elementos_cenario(ax, vant)
            self._plotar_raios(vant, ax)
            self._configurar_eixos(ax, vant, titulo=f"Cenário Marítimo - Step {frame}")
            return []
        
        def frame_counter():
            frame = 0
            while vant.continuar_voo:
                yield frame
                frame += 1

            # Após voo terminar, adiciona frames extras "parados"
            for _ in range(20):
                yield frame
                frame += 1

        ani = animation.FuncAnimation(
            fig,
            update,
            frames=frame_counter,
            repeat=False,
            cache_frame_data=False
        )

        ani.save(filename, writer='pillow', fps=5)
        plt.close(fig)

    def _plotar_elementos_cenario(self, ax, vant):
        self._plotar_navios()
        self._plotar_referencia(vant)
        self._plotar_trajeto(vant)
        self._plotar_vant(vant, ax)

    def _configurar_eixos(self, ax, vant=None, titulo="Cenário Marítimo"):
        ax.set_xlim(0, self.largura)
        ax.set_ylim(0, self.altura)
        ax.set_title(titulo)
        ax.set_xlabel("MN (Largura)")
        ax.set_ylabel("MN (Altura)")

        # Legenda fora do gráfico com moldura personalizada
        leg = ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
        frame = leg.get_frame()
        frame.set_edgecolor("black")
        frame.set_facecolor("white")
        frame.set_alpha(0.7)
        frame.set_boxstyle("round")

        # Estatísticas
        if vant is not None:
            self._plotar_estatisticas(ax, vant)

        ax.grid(True)

    def _plotar_navios(self):
        cores = {
            "nao_detectado": "gray",
            "detectado": "orange",
            "inspecionado": "green"
        }
        simbolos = {
            "nao_detectado": "x",
            "detectado": "^",
            "inspecionado": "o"
        }

        for navio in self.navios:
            plt.scatter(navio.x, navio.y,
                        c=cores[navio.estado],
                        marker=simbolos[navio.estado],
                        label=navio.estado if navio.estado not in plt.gca().get_legend_handles_labels()[1] else "")

    def _plotar_referencia(self, vant):
        if hasattr(vant, 'referencia') and vant.referencia:
            ref = np.array(vant.referencia)
            plt.plot(ref[:, 0], ref[:, 1], '-sk', label="Rota planejada")

    def _plotar_trajeto(self, vant):
        if hasattr(vant, 'trajeto') and vant.trajeto:
            traj = np.array(vant.trajeto)
            plt.plot(traj[:, 0], traj[:, 1], '-b', label="Trajeto real")

    def _plotar_vant(self, vant, ax):
        # Coordenada atual
        x, y = vant.x, vant.y

        # Se houver pelo menos 2 pontos na trajetória, calcula o ângulo
        if len(vant.trajeto) >= 2:
            x_prev, y_prev = vant.trajeto[-2]
            dx = x - x_prev
            dy = y - y_prev
            angle_rad = np.arctan2(dy, dx)
            angle_deg = np.degrees(angle_rad)
        else:
            angle_deg = 0  # padrão: apontando para o norte

        # Criar triângulo rotacionado representando o VANT
        triangle = RegularPolygon((x, y), numVertices=3, radius=5,
                                orientation=np.radians(angle_deg - 90),
                                color='blue', ec='black')
        ax.add_patch(triangle)


    def _plotar_estatisticas(self, ax, vant=None):
        # Estatísticas dos navios
        total = len(self.navios)
        detectados = sum(n.estado in ["detectado", "inspecionado"] for n in self.navios)
        inspecionados = sum(n.estado == "inspecionado" for n in self.navios)

        texto = (
            f"Navios: {total}\n"
            f"Detectados: {detectados}\n"
            f"Inspecionados: {inspecionados}"
        )

        # Usar odômetro do VANT, se fornecido
        if vant is not None:
            total_milhas = vant.odometro()
            texto += f"\nTrajetória: {total_milhas:.1f} MN"

            ax.text(1.045, 0.15, texto, transform=ax.transAxes,
                    ha='left', va='top', fontsize=10,
                    bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))
        
    def _plotar_raios(self, vant, ax):
        # Círculo do radar
        radar_circle = patches.Circle(
            (vant.x, vant.y),
            vant.alcance_radar,
            edgecolor="orange",
            facecolor="none",
            linestyle="--",
            linewidth=1,
            label="Radar (100 MN)"
        )
        ax.add_patch(radar_circle)

        # Círculo da câmera
        camera_circle = patches.Circle(
            (vant.x, vant.y),
            vant.alcance_camera,
            edgecolor="green",
            facecolor="none",
            linestyle=":",
            linewidth=1,
            label="Câmera (20 MN)"
        )
        ax.add_patch(camera_circle)



