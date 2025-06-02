import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import RegularPolygon


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
        self.navios = [
            Navio(
                x=np.random.uniform(0, self.largura),
                y=np.random.uniform(0, self.altura)
            )
            for _ in range(self.num_navios)
        ]

    def plotar_cenario(self, vant=None):
        fig, ax = plt.subplots(figsize=(8, 6))

        self._plotar_navios()
        if vant is not None:
            self._plotar_referencia(vant)
            self._plotar_trajeto(vant)
            self._plotar_vant(vant, ax)
            self._plotar_estatisticas(ax, vant)

        ax.set_xlim(0, self.largura)
        ax.set_ylim(0, self.altura)
        ax.set_title("Cenário Marítimo - Estados dos Navios")
        ax.set_xlabel("MN (Largura)")
        ax.set_ylabel("MN (Altura)")
        leg = ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
        frame = leg.get_frame()
        frame.set_edgecolor("black")
        ax.grid(True)
        fig.tight_layout()
        plt.show()


    def animar_cenario(self, vant, filename="output.gif", max_steps=100):
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.subplots_adjust(right=0.75)

        def update(frame):
            ax.clear()

            # Atualiza posição do VANT
            if frame < max_steps:
                vant.step()

            # Plotar cenário com modularização
            self._plotar_navios()
            self._plotar_referencia(vant)
            self._plotar_trajeto(vant)
            self._plotar_vant(vant, ax)
            self._plotar_estatisticas(plt.gca(), vant)
            

            ax.set_xlim(0, self.largura)
            ax.set_ylim(0, self.altura)
            ax.set_title(f"Cenário Marítimo - Step {frame}")
            ax.set_xlabel("MN (Largura)")
            ax.set_ylabel("MN (Altura)")
            leg = ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
            frame = leg.get_frame()
            frame.set_edgecolor("black")
            ax.grid(True)

            return []

        ani = animation.FuncAnimation(fig, update, frames=max_steps, repeat=False)
        ani.save(filename, writer='pillow', fps=5)
        plt.close(fig)


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
            plt.plot(ref[:, 0], ref[:, 1], '--k', label="Rota planejada")

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

        # Adicionar comprimento do trajeto, se VANT for fornecido
        if vant is not None and len(vant.trajeto) >= 2:
            total_milhas = sum(
                np.hypot(x2 - x1, y2 - y1)
                for (x1, y1), (x2, y2) in zip(vant.trajeto[:-1], vant.trajeto[1:])
            )
            texto += f"\nDistância percorrida: {total_milhas:.1f} MN"

        ax.text(1.045, 0.75, texto, transform=ax.transAxes,
                ha='left', va='top', fontsize=10,
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))


