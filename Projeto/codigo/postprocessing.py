import pandas as pd
import matplotlib.pyplot as plt

# combinar dois csvs em um só
def combinar_csvs(caminho_csv1, caminho_csv2):
    df1 = pd.read_csv(caminho_csv1)
    df2 = pd.read_csv(caminho_csv2)

    # Verificar se as colunas são compatíveis
    if set(df1.columns) != set(df2.columns):
        raise ValueError("Os CSVs não possuem as mesmas colunas.")

    # Concatenar os DataFrames
    df_combinado = pd.concat([df1, df2], ignore_index=True)

    # Ordenar o DataFrame combinado por política [passiva, greed, SA] e por número de navios
    df_combinado['politica'] = pd.Categorical(df_combinado['politica'], categories=['passiva', 'greed', 'SA'], ordered=True)
    df_combinado = df_combinado.sort_values(by=['politica', 'navios'])

    # Retornar o DataFrame combinado em um novo CSV
    return df_combinado

def resumir_resultados_csv(df):
    # Agrupar por política e quantidade de navios
    agrupado = df.groupby(["politica", "navios"]).mean(numeric_only=True)

    # Exibir os resultados formatados
    for idx, linha in agrupado.iterrows():
        politica = idx[0] # type: ignore
        navios = idx[1] # type: ignore
        print(f"\nPolítica: {politica} | Navios: {int(navios)}")
        print(f"  - Média de inspecionados: {linha['inspecionados']:.2f}")
        print(f"  - Média de distância percorrida: {linha['distancia_percorrida']:.2f}")
        print(f"  - Média de tempo de execução: {linha['tempo_execucao']:.2f} s")

def plotar_resultados_por_politica(df, coluna_y, percentual=False, y_limit=None):
    # Verifica se a coluna existe
    if coluna_y not in df.columns:
        print(f"Coluna '{coluna_y}' não encontrada no CSV.")
        return
    
    # Se for detectados, soma inspecionados e detectados
    if coluna_y == 'detectados':
        df['detectados'] += df['inspecionados']

    # Se for percentual, cria nova coluna normalizada pelo total de navios
    if percentual and coluna_y in ['inspecionados', 'detectados']:
        df[coluna_y + '_percentual'] = df[coluna_y] / df['navios'] * 100
        coluna_y_plot = coluna_y + '_percentual'
        ylabel = f"{coluna_y.capitalize()} (%)"
    else:
        coluna_y_plot = coluna_y
        ylabel = coluna_y.replace("_", " ").capitalize()

    # Agrupar por política e número de navios
    agrupado = df.groupby(['politica', 'navios'], observed=True)[coluna_y_plot].mean().reset_index()

    # Plotar
    plt.figure(figsize=(10, 6))
    for politica in agrupado['politica'].unique():
        dados = agrupado[agrupado['politica'] == politica]
        plt.plot(dados['navios'], dados[coluna_y_plot], marker='o', label=politica)

    plt.title(f"Média de {ylabel} por número de navios")
    plt.xlabel("Número de navios")
    plt.xlim([0, 200])
    plt.ylabel(ylabel)
    plt.ylim(y_limit if y_limit else [0, None])
    plt.grid(True)
    plt.legend(title="Política")
    plt.tight_layout()
    # plt.show()
    plt.savefig(f"resultado_{coluna_y[0:3]}.png")

if __name__ == "__main__":
    # resumir_resultados_csv("resultados_simulacoes.csv")
    
    df = combinar_csvs("SA.csv", "passiva_greed.csv")

    plotar_resultados_por_politica(df, "inspecionados", percentual=True, y_limit=[0, 100])
    plotar_resultados_por_politica(df, "detectados", percentual=True, y_limit=[60, 100])
    plotar_resultados_por_politica(df, "distancia_percorrida", y_limit=[500, 2500])
    plotar_resultados_por_politica(df, "tempo_execucao", y_limit=[-0.5,40])
    