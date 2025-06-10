from ambiente import AmbienteMaritimo
from vant import VANT
import csv
from postprocessing import resumir_resultados_csv

def preparar_simulacao(num_navios=50, politica="passiva", seed=42):
    ambiente = AmbienteMaritimo(largura=300, altura=300, num_navios=num_navios, seed=seed)
    vant = VANT(x=0.0, y=50.0, velocidade=300.0, autonomia=2400,
                alcance_radar=50.0, alcance_camera=10.0, politica=politica, delta_t=5)
    vant.definir_linhas_paralelas(inicial=(0, 50), final=300, espacamento=50, num_linhas=3, gap=50)
    return ambiente, vant

def simulacao_estatica(num_navios=50, politica="passiva", seed=42):
    ambiente, vant = preparar_simulacao(num_navios, politica, seed)
    ambiente.plotar_cenario(vant=vant, save=True)

def simulacao_animada(num_navios=50, politica="passiva", seed=42):
    ambiente, vant = preparar_simulacao(num_navios, politica, seed)
    filename = vant.politica + ".gif"
    ambiente.animar_cenario(vant, filename=filename)

def simulacao_texto(num_navios=50, politica="passiva", seed=42):
    ambiente, vant = preparar_simulacao(num_navios, politica, seed)
    resultado = ambiente.executar_simulacao(vant)
    return resultado

def simulacao_csv(nome_arquivo="resultados_simulacoes.csv"):
    # lista_politicas = ["passiva", "greed", "SA"]
    lista_politicas = ["SA"]
    lista_navios = [10, 25, 50, 75, 100, 125, 150, 175, 200]
    num_iteracoes = 100
    resultados = []

    for num_navios in lista_navios:
        for politica in lista_politicas:
            for iteracao in range(1, num_iteracoes + 1):
                resultado = simulacao_texto(num_navios=num_navios, politica=politica, seed=iteracao)
                resultado["iteracao"] = iteracao
                resultados.append(resultado)
                print(f"Rodando política={politica}, iteração={iteracao}, navios={num_navios}, inspecionados={resultado['inspecionados']}, distanca_percorrida={resultado['distancia_percorrida']:.2f}, tempo_execucao={resultado['tempo_execucao']:.2f}s")

    campos = list(resultados[0].keys())
    with open(nome_arquivo, mode="w", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(resultados)

if __name__ == "__main__":
    simulacao_csv(nome_arquivo="SA.csv")
    # resumir_resultados_csv("resultados_simulacoes.csv")

    # num = 80
    # simulacao_estatica(num_navios=num, politica="greed", seed=1)
    # simulacao_estatica(num_navios=num, politica="SA", seed=1)

    # simulacao_animada(num_navios=50, politica="greed", seed=1)
    # simulacao_animada(num_navios=50, politica="SA", seed=1)
