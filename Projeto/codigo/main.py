from ambiente import AmbienteMaritimo
from vant import VANT

# Criar o ambiente marítimo e gerar navios
ambiente = AmbienteMaritimo(largura=250, altura=200, num_navios=15)

# Criar o VANT e definir a rota de patrulha
vant = VANT(x=0.0, y=0.0)
vant.definir_linhas_paralelas(inicial=(50, 50), final=200, espacamento=50, num_linhas=3)

# Simular o voo por alguns steps
# for _ in range(15):
#     vant.step()
# ambiente.plotar_cenario(vant=vant)

# Gerar animação da missão e salvar como GIF
ambiente.animar_cenario(vant, filename="patrulha.gif", max_steps=10)