# Este programa implementa o algoritmo A* para encontrar o caminho mais curto entre duas estações de metrô,
# levando em consideração os tempos de viagem entre as estações e informações em tempo real sobre as linhas.
1   

def A_star(start, end):
    lista_estacoes = []  # Fronteira que armazena estações a serem exploradas
    lista_estacoes.append(start)
    estacoes_finais = []  # Fronteira final que armazena estações já exploradas
    custo_atual = {}  # Armazena o custo atual para chegar a cada estação
    pais_estacao = {}  # Armazena a estação predecessora para reconstruir o caminho final
    custo_atual[start] = 0
    pais_estacao[start] = start

    while len(lista_estacoes) != 0:
        estacao_atual = 0
        for estacao in lista_estacoes:
            if estacao_atual == 0:
                estacao_atual = estacao
            if custo_atual[estacao] + time_matrix[estacao[0] - 1][end[0] - 1] < custo_atual[estacao_atual] + time_matrix[estacao_atual[0] - 1][end[0] - 1]:
                estacao_atual = estacao

        if estacao_atual != end:
            for (numero, distancia, linha) in vizinhos(estacao_atual[0]):
                vizinho = (numero, linha)
                if vizinho not in lista_estacoes and vizinho not in estacoes_finais:
                    lista_estacoes.append(vizinho)
                    pais_estacao[vizinho] = estacao_atual
                    custo_atual[vizinho] = custo_atual[estacao_atual] + distancia
                    if estacao_atual[1] != vizinho[1]:
                        custo_atual[vizinho] += 4  # Penalidade por mudar de linha
                else:
                    if custo_atual[vizinho] > custo_atual[estacao_atual] + distancia:
                        custo_atual[vizinho] = custo_atual[estacao_atual] + distancia
                        pais_estacao[vizinho] = estacao_atual
                        if numero in estacoes_finais:
                            estacoes_finais.remove(vizinho)
                            lista_estacoes.append(vizinho)

        if estacao_atual == end:
            caminho = []
            while pais_estacao[estacao_atual] != estacao_atual:
                caminho.append(estacao_atual)
                estacao_atual = pais_estacao[estacao_atual]
            caminho.append(start)
            caminho.reverse()
            print('Caminho:', caminho)
            print('Menor tempo:', custo_atual[estacao] + time_matrix[estacao[0] - 1][end[0] - 1], 'minutos')
            return caminho

        lista_estacoes.remove(estacao_atual)
        estacoes_finais.append(estacao_atual)

def vizinhos(estacao):
    if estacao in realtime_data:
        return realtime_data[estacao]

# Matriz de tempos de viagem entre as estações
time_matrix = [
    [0.0, 20.0, 37.0, 49.6, 72.8, 77.6, 71.6, 50.8, 35.2, 18.2, 33.4, 54.6, 55.2, 59.6],
    [20.0, 0.0, 17.0, 29.6, 53.2, 58.2, 52.2, 34.6, 20.0, 7.0, 31.0, 41.8, 38.2, 43.6],
    [37.0, 17.0, 0.0, 12.6, 36.4, 41.2, 35.2, 27.2, 18.8, 20.6, 39.0, 38.2, 24.2, 33.2],
    [49.6, 29.6, 12.6, 0.0, 24.0, 28.8, 23.0, 24.8, 25.2, 33.4, 47.2, 37.2, 21.2, 30.8],
    [72.8, 53.2, 36.4, 24.0, 0.0, 6.0, 4.8, 38.8, 46.6, 56.4, 68.4, 49.6, 29.0, 35.8],
    [77.6, 58.2, 41.2, 28.8, 6.0, 0.0, 6.6, 44.6, 51.4, 60.6, 73.4, 55.2, 30.4, 36.4],
    [71.6, 52.2, 35.2, 23.0, 4.8, 6.6, 0.0, 40.0, 46.0, 54.6, 68.4, 51.4, 24.8, 31.2],
    [50.8, 34.6, 27.2, 24.8, 38.8, 44.6, 40.0, 0.0, 16.4, 40.6, 32.2, 12.8, 45.4, 55.2],
    [35.2, 20.0, 18.8, 25.2, 46.6, 51.4, 46.0, 16.4, 0.0, 27.0, 22.4, 21.8, 42.4, 53.2],
    [18.2, 7.0, 20.6, 33.4, 56.4, 60.6, 54.6, 40.6, 27.0, 0.0, 35.2, 48.4, 37.4, 42.4],
    [33.4, 31.0, 39.0, 47.2, 68.4, 73.4, 68.4, 32.2, 22.4, 35.2, 0.0, 31.8, 67.4, 78.8],
    [54.6, 41.8, 38.2, 37.2, 49.6, 55.2, 51.4, 12.8, 21.8, 48.4, 31.8, 0.0, 59.2, 69.8],
    [55.2, 38.2, 24.2, 21.2, 29.0, 30.4, 24.8, 45.4, 42.4, 37.4, 67.4, 59.2, 0.0, 13.4],
    [59.6, 43.6, 33.2, 30.8, 35.8, 36.4, 31.2, 55.2, 53.2, 42.4, 78.8, 69.8, 13.4, 0.0],
]

# Informações em tempo real sobre as linhas de metrô
realtime_data = {
    1: [(2, 20, 'azul')],
    2: [(3, 17, 'azul'), (1, 20, 'azul'), (9, 20, 'amarela'), (10, 7, 'amarela')],
    3: [(2, 17, 'azul'), (4, 12.6, 'azul'), (9, 18.8, 'vermelha'), (13, 37.4, 'vermelha')],
    4: [(3, 12.6, 'azul'), (5, 26, 'azul'), (8, 30.6, 'verde'), (13, 25.6, 'verde')],
    5: [(4, 26, 'azul'), (6, 6, 'azul'), (7, 4.8, 'amarela'), (8, 60, 'amarela')],
    6: [(5, 6, 'azul')],
    7: [(5, 4.8, 'amarela')],
    8: [(5, 60, 'amarela'), (4, 30.6, 'verde'), (9, 19.2, 'amarela'), (12, 12.8, 'verde')],
    9: [(8, 19.2, 'amarela'), (2, 20, 'amarela'), (3, 18.8, 'vermelha'), (11, 24.4, 'vermelha')],
    10: [(2, 7, 'amarela')],
    11: [(9, 24.4, 'vermelha')],
    12: [(8, 12.8, 'verde')],
    13: [(3, 37.4, 'vermelha'), (4, 25.6, 'verde'), (14, 10.2, 'verde')],
    14: [(13, 10.2, 'verde')]
}

# Solicita informações ao usuário
print("Número da estação de partida:")
partida = int(input())
print(50 * "-")
print("Cor da linha de partida:")
linha_partida = input()
print(50 * "-")
print("Número da estação de Chegada:")
chegada= int(input())
print(50 * "-")
print("Cor da linha de chegada:")
linha_chegada = input()
print(50 * "-")

# Todos a Booooooordooooo!
A_star((partida, linha_partida), (chegada, linha_chegada))
