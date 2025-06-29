## 🚀 Estrutura Geral de Sprints – Projeto VANT para Patrulha Marítima

### 🧭 Sprint 1 – Estruturação base do sistema
- [x] Criar classe `Navio`
- [x] Criar classe `AmbienteMaritimo`
- [x] Gerar navios aleatórios
- [x] Plotar navios com estados diferentes
- [x] Exibir cenário com `matplotlib`

---

### 🛩 Sprint 2 – Lógica do VANT
- [x] Criar classe `VANT` com atributos de posição, velocidade e autonomia
- [x] Implementar rota de patrulha com linhas paralelas
- [x] Implementar movimentação por waypoints (`step()`)
- [x] Registrar trajetória real
- [x] Plotar VANT e trajetória no ambiente

---

### 📊 Sprint 3 – Visualização incremental
- [x] Adicionar método `animar_cenario()` com `matplotlib.animation`
- [x] Mostrar legenda e estatísticas (navios detectados / inspecionados)
- [x] Corrigir layout para não cortar texto no GIF
- [x] Ajustar rotação do VANT conforme direção do movimento

---

### 🧠 Sprint 4 – Lógica de detecção
- [x] Radar: identificar navios dentro de 100 MN
- [x] Câmera: inspecionar navios dentro de 20 MN
- [x] Atualizar estado dos navios no ambiente
- [x] Sincronizar estados entre `VANT` e `AmbienteMaritimo`
- [x] Plotar círculo referente ao radar e a câmera

---

### 🧭 Sprint 5 – Implementação das políticas de navegação
- [x] Adicionar atributo `politica` à classe `VANT`
- [x] Modularizar `step()` para despachar por política
- [x] Limitar número de steps pela autonomia (função odômetro)
- [x] Política `passiva`: seguir apenas os waypoints (atual)
- [x] Mudar a lógica do step para considerar self.nodes()
- [x] Política `greed`: desviar para inspecionar navios próximos (gananciosa)
- [x] Política `SA`: replanejar com Simulated Annealing a cada novo alvo

---

### 🧪 Sprint 6 – Estatísticas e relatório final
- [x] Simulação sem imagem
- [x] Função para salvar todas as execuções em CSV por política e cenário
- [ ] Calibrar o Simulated Annealing
- [ ] Coletar resultados
- [ ] Calcular métricas desempenho: cobertura, eficiência, distância total
- [ ] Comparar resultados entre políticas
- [ ] Gerar visualização final da missão (GIF ou imagem)
