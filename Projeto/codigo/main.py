from ambiente import AmbienteMaritimo
from vant import VANT

# Criar o ambiente marítimo e gerar navios
ambiente = AmbienteMaritimo(largura=350, altura=400, num_navios=15)

# Criar o VANT e definir a rota de patrulha
vant = VANT(x=0.0, y=0.0)
vant.definir_linhas_paralelas(inicial=(50, 100), final=300, espacamento=100, num_linhas=3)

# Simular o voo por alguns steps
# ambiente.plotar_cenario(vant=vant, max_steps=30)

# Gerar animação da missão e salvar como GIF
ambiente.animar_cenario(vant, filename="patrulha.gif", max_steps=30)