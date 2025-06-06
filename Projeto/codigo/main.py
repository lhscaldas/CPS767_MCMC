from ambiente import AmbienteMaritimo
from vant import VANT
import csv

def preparar_simulacao(num_navios=50, politica="passiva"):
    ambiente = AmbienteMaritimo(largura=300, altura=300, num_navios=50)
    vant = VANT(x=0.0, y=50.0, velocidade=60.0, autonomia=2400,
                alcance_radar=50.0, alcance_camera=10.0, politica=politica, delta_t=5)
    vant.definir_linhas_paralelas(inicial=(0, 50), final=300, espacamento=100, num_linhas=3, gap=50)
    return ambiente, vant

def simulacao_estatica():
    ambiente, vant = preparar_simulacao()    
    ambiente.plotar_cenario(vant=vant, save=True)

def simulacao_animada():
    ambiente, vant = preparar_simulacao()
    filename = vant.politica + ".gif"
    ambiente.animar_cenario(vant, filename=filename)

def simulacao_texto(num_navios=50, politica="passiva"):
    ambiente, vant = preparar_simulacao(num_navios, politica)
    resultado = ambiente.executar_simulacao(vant)
    return resultado

def salvar_csv(resultados, nome_arquivo="resultados_simulacoes.csv"):
    campos = list(resultados[0].keys())
    with open(nome_arquivo, mode="w", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(resultados)

def simulacao_csv():
    lista_politicas = ["passiva", "greed", "SA"]
    lista_navios = list(range(10, 201, 25))
    num_iteracoes = 30
    resultados = []

    for politica in lista_politicas:
        for num_navios in lista_navios:
            for iteracao in range(1, num_iteracoes + 1):
                print(f"Rodando política={politica}, navios={num_navios}, iteração={iteracao}")
                resultado = simulacao_texto(num_navios=num_navios, politica=politica)
                resultado["politica"] = politica
                resultado["num_navios"] = num_navios
                resultado["iteracao"] = iteracao
                resultados.append(resultado)

    salvar_csv(resultados)

if __name__ == "__main__":
    simulacao_csv()