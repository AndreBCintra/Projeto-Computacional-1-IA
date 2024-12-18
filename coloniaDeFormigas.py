import numpy as np
import random
from tabelaDeCustos import tabelaDeCustos

taxaFeromonio = 1.0
taxaHeuristica = 2.0
Evaporacao = 0.5
Formigas = 15
Iteracoes = 100
q = 100

def calcularProbabilidade(feromonio, heuristica, visitadas, atual):
    probabilidades = []
    soma = 0

    for j in range(len(feromonio)):
        if j not in visitadas:
            prob = (feromonio[atual][j] ** taxaFeromonio) * (heuristica[atual][j] ** taxaHeuristica)
            probabilidades.append((j, prob))
            soma += prob

    probabilidades = [(cidade, prob / soma) for cidade, prob in probabilidades]
    return probabilidades

def escolherProxima(probabilidades):
    rand = random.random()
    acumulado = 0

    for cidade, prob in probabilidades:
        acumulado += prob
        if rand <= acumulado:
            return cidade
    return probabilidades[-1][0]

def coloniaDeFormigas(tabelaDeCustos):
    n = len(tabelaDeCustos)
    feromonio = np.ones((n, n))
    heuristica = 1 / (np.array(tabelaDeCustos) + np.eye(n) * 1e10)

    melhorCusto = float('inf')
    melhorRota = None

    for iteracao in range(Iteracoes):
        rotas = []
        custos = []

        for formiga in range(Formigas):
            atual = random.randint(0, n - 1)
            rota = [atual]
            visitadas = set(rota)

            while len(rota) < n:
                probabilidades = calcularProbabilidade(feromonio, heuristica, visitadas, atual)
                proxima = escolherProxima(probabilidades)
                rota.append(proxima)
                visitadas.add(proxima)
                atual = proxima

            rota.append(rota[0])
            custo = sum(tabelaDeCustos[rota[i]][rota[i+1]] for i in range(len(rota) - 1))
            rotas.append(rota)
            custos.append(custo)
            print(f"Iteração {iteracao + 1}: Custo da formiga {formiga+1} = {custo}")

        melhorCustoIteracao = min(custos)
        melhorRotaIteracao = rotas[custos.index(melhorCustoIteracao)]

        if melhorCustoIteracao < melhorCusto:
            melhorCusto = melhorCustoIteracao
            melhorRota = melhorRotaIteracao

        # Atualizar os feromônios
        novoFeromonio = np.zeros((n, n))

        for i in range(len(melhorRotaIteracao) - 1):
            origem = melhorRota[i]
            destino = melhorRota[i + 1]

            for rota, custo in zip(rotas, custos):
                for j in range(len(rota) - 1):
                    if rota[j] == origem and rota[j + 1] == destino:
                        novoFeromonio[origem][destino] += q / custo
                        novoFeromonio[destino][origem] += q / custo
    
        for rota, custo in zip(rotas, custos):
            for j in range(len(rota) - 1):
                novoFeromonio[rota[j]][rota[j + 1]] += q / custo
                novoFeromonio[rota[j + 1]][rota[j]] += q / custo

        feromonio = (1 - Evaporacao) * feromonio + novoFeromonio

        print(f"Iteração {iteracao + 1}: Melhor custo = {melhorCusto}")

    return melhorRota, melhorCusto

melhorRotaFinal, melhorCustoFinal = coloniaDeFormigas(tabelaDeCustos)
print("Melhor rota encontrada:", melhorRotaFinal)
print("Custo da melhor rota:", melhorCustoFinal)