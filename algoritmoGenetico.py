import random
import math
from tabelaDeCustos import tabelaDeCustos

# O genótipo será representado pelas cidades visitadas ex: [3, 5, 2, 1, 4], partindo da cidade 3 indo pra 5, depois pra 2, depois pra 1, depois pra 4 e voltando pra 3

#N = int(input("Insira o numero de cidades: "))
N = 15
TamanhoDaPopulacao = 100
NumDeGeracoes = 100
TaxaDeMutacao = 0.1

def calcularCusto(rota):
    custo = 0
    for i in range(len(rota)):
        custo += tabelaDeCustos[rota[i]][rota[(i+1) % len(rota)]]
    return custo

def gerarPopInicial(tamanhoDaPop):
    populacao = []
    for i in range(tamanhoDaPop):
        individuo = list(range(N))
        random.shuffle(individuo)
        populacao.append(individuo)
    return populacao

def calcularFitnessRoleta(populacao):
    custos = [calcularCusto(pessoa) for pessoa in populacao]
    fitnesses = [1 / custo for custo in custos]
    return fitnesses

def calcularFitnessTorneio(populacao):
    custos = [calcularCusto(pessoa) for pessoa in populacao]
    fitnesses = [custo for custo in custos]
    return fitnesses

def selecaoPorRoleta(populacao, fitnesses):
    total_fitness = sum(fitnesses)
    valor_sorteado = random.uniform(0, total_fitness)
    soma_acumulada = 0
    for i, fitness in enumerate(fitnesses):
        soma_acumulada += fitness
        if soma_acumulada >= valor_sorteado:
            return populacao[i]
        
def selecaoPorTorneio(populacao, fitnesses, k=3):
    participantes_indices = random.sample(range(len(populacao)), k)
    melhor_indice = min(participantes_indices, key=lambda idx: fitnesses[idx])
    
    return populacao[melhor_indice]

def crossover(pai, mae):
    n = len(pai)
    inicio, fim = sorted(random.sample(range(n), 2))
    filho = [-1] * n
    filho[inicio:fim] = pai[inicio:fim]

    pos = fim
    for gene in mae:
        if gene not in filho:
            if pos == n:
                pos = 0
            filho[pos] = gene
            pos += 1
    return filho

def mutacao(individuo, taxaMutacao):
    if random.random() < taxaMutacao:
        i, j = random.sample(range(len(individuo)), 2)
        aux = individuo[i]
        individuo[i] = individuo[j]
        individuo[j] = aux

def algoritmoGenetico():
    populacao = gerarPopInicial(TamanhoDaPopulacao)
    melhorCusto = math.inf
    melhorRota = None

    for geracao in range(NumDeGeracoes):
        fitnessesRoleta = calcularFitnessRoleta(populacao)
        fitnessesTorneio = calcularFitnessTorneio(populacao)

        novaPopulacao = []

        for i in range(TamanhoDaPopulacao // 2):
            pai = selecaoPorTorneio(populacao, fitnessesTorneio)
            mae = selecaoPorTorneio(populacao, fitnessesTorneio)

            #pai = selecaoPorRoleta(populacao, fitnessesRoleta)
            #mae = selecaoPorRoleta(populacao, fitnessesRoleta)

            filho1 = crossover(pai, mae)
            filho2 = crossover(pai, mae)

            mutacao(filho1, TaxaDeMutacao)
            mutacao(filho2, TaxaDeMutacao)

            novaPopulacao.extend([filho1, filho2])

        populacao = novaPopulacao

        melhorSolucao = min(populacao, key=lambda ind: calcularCusto(ind))
        custoMelhorSolucao = calcularCusto(melhorSolucao)

        #print(f"Geração {geracao + 1}: Melhor custo = {custoMelhorSolucao}")
        print(f"{custoMelhorSolucao}")
        if custoMelhorSolucao < melhorCusto:
            melhorCusto = custoMelhorSolucao
            melhorRota = melhorSolucao
    
    return melhorRota

melhorRota = algoritmoGenetico()

print(f"Melhor rota encontrada: {melhorRota}")
print(f"Custo da melhor rota: {calcularCusto(melhorRota)}")