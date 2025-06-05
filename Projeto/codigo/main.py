from ambiente import AmbienteMaritimo
from vant import VANT

# Criar o ambiente marítimo e gerar navios
ambiente = AmbienteMaritimo(largura=300, altura=300, num_navios=50)

# Criar o VANT e definir a rota de patrulha
vant = VANT(x=0.0, y=50.0, velocidade=60.0, autonomia=6000,
            alcance_radar=50.0, alcance_camera=10.0, politica="greed", delta_t=30)
vant.definir_linhas_paralelas(inicial=(0, 50), final=300, espacamento=100, num_linhas=3, gap=50)

# Simular o voo por alguns steps
# ambiente.plotar_cenario(vant=vant)

# Gerar animação da missão e salvar como GIF
ambiente.animar_cenario(vant, filename="patrulha.gif")