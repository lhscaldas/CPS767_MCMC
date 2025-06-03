from ambiente import AmbienteMaritimo
from vant import VANT

# Criar o ambiente marítimo e gerar navios
ambiente = AmbienteMaritimo(largura=350, altura=400, num_navios=15)

# Criar o VANT e definir a rota de patrulha
vant = VANT(x=50.0, y=100.0, velocidade=60.0, autonomia=1400.0,
            alcance_radar=50.0, alcance_camera=20.0, politica="SA")
vant.definir_linhas_paralelas(inicial=(50, 100), final=300, espacamento=100, num_linhas=3)

# Simular o voo por alguns steps
# ambiente.plotar_cenario(vant=vant, max_steps=50)

# Gerar animação da missão e salvar como GIF
ambiente.animar_cenario(vant, filename="patrulha.gif", max_steps=50)