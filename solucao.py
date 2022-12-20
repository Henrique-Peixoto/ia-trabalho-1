from queue import Queue, LifoQueue, PriorityQueue
from math import inf 
from random import random
from itertools import count

def determinarProximoEstado(acao, estado):
    posicaoEspacoVazio = estado.find('_')
    peca = ''

    if acao == 'esquerda':
        peca = estado[posicaoEspacoVazio - 1:posicaoEspacoVazio]
    elif acao == 'direita':
        peca = estado[posicaoEspacoVazio + 1:posicaoEspacoVazio + 2]
    elif acao == 'acima':
        peca = estado[posicaoEspacoVazio - 3:posicaoEspacoVazio - 2]
    elif acao == 'abaixo':
        peca = estado[posicaoEspacoVazio + 3:posicaoEspacoVazio + 4]

    posicaoPeca = estado.find(peca)
    novoEstado = estado.replace('_', peca)
    novoEstado = novoEstado[:posicaoPeca] + '_' + novoEstado[posicaoPeca + 1:]

    return acao, novoEstado


def sucessor(estado):
    posicaoEspacoVazio = estado.find('_')
    estadosPossiveis = []

    # Dois movimentos possiveis
    if posicaoEspacoVazio in [0, 2, 6, 8]:
        if posicaoEspacoVazio == 0:
            estadosPossiveis.append(determinarProximoEstado('direita', estado))
            estadosPossiveis.append(determinarProximoEstado('abaixo', estado))
        elif posicaoEspacoVazio == 2:
            estadosPossiveis.append(determinarProximoEstado('esquerda', estado))
            estadosPossiveis.append(determinarProximoEstado('abaixo', estado))
        elif posicaoEspacoVazio == 6:
            estadosPossiveis.append(determinarProximoEstado('acima', estado))
            estadosPossiveis.append(determinarProximoEstado('direita', estado))
        elif posicaoEspacoVazio == 8:
            estadosPossiveis.append(determinarProximoEstado('esquerda', estado))
            estadosPossiveis.append(determinarProximoEstado('acima', estado))
    # Tres movimentos possiveis
    elif posicaoEspacoVazio in [1, 3, 5, 7]:
        if posicaoEspacoVazio == 1:
            estadosPossiveis.append(determinarProximoEstado('direita', estado))
            estadosPossiveis.append(determinarProximoEstado('esquerda', estado))
            estadosPossiveis.append(determinarProximoEstado('abaixo', estado))
        elif posicaoEspacoVazio == 3:
            estadosPossiveis.append(determinarProximoEstado('acima', estado))
            estadosPossiveis.append(determinarProximoEstado('direita', estado))
            estadosPossiveis.append(determinarProximoEstado('abaixo', estado))
        elif posicaoEspacoVazio == 5:
            estadosPossiveis.append(determinarProximoEstado('acima', estado))
            estadosPossiveis.append(determinarProximoEstado('esquerda', estado))
            estadosPossiveis.append(determinarProximoEstado('abaixo', estado))
        elif posicaoEspacoVazio == 7:
            estadosPossiveis.append(determinarProximoEstado('acima', estado))
            estadosPossiveis.append(determinarProximoEstado('esquerda', estado))
            estadosPossiveis.append(determinarProximoEstado('direita', estado))
    # Quatro movimentos possiveis
    else:
        estadosPossiveis.append(determinarProximoEstado('acima', estado))
        estadosPossiveis.append(determinarProximoEstado('esquerda', estado))
        estadosPossiveis.append(determinarProximoEstado('direita', estado))
        estadosPossiveis.append(determinarProximoEstado('abaixo', estado))

    return estadosPossiveis


class Nodo:
    def __init__(self, estado, pai,acao, custo):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

    def __repr__(self):
        return '(' \
            + self.estado + ', '\
            + self.pai.estado + ', ' \
            + self.acao + ', ' \
            + str(self.custo) + \
            ')'
    

def expande(nodo):
    estadosPossiveis = sucessor(nodo.estado)
    nodos = []

    for tupla in estadosPossiveis:
        acao = tupla[0]
        estado = tupla[1]
        novoNodo = Nodo(estado, nodo, acao, nodo.custo + 1)
        nodos.append(novoNodo)

    return nodos


def pegarCaminho(nodo):
    caminho = []

    while nodo.pai is not None:
        caminho.append(nodo.acao)
        nodo = nodo.pai

    caminho.reverse()
    return caminho


def dfs(estado):
    if estado == '12345678_':
        return []

    nodoInicial = Nodo(estado, None, '', 0)
    explorados = set()
    fronteira = LifoQueue(0)
    nodos = expande(nodoInicial)

    for nodo in nodos:
        fronteira.put(nodo)

    while fronteira.qsize() > 0:
        nodoExpandivel = fronteira.get()
        print(fronteira.qsize())

        if (nodoExpandivel.estado == '12345678_'):
            return pegarCaminho(nodoExpandivel)

        if nodoExpandivel.estado not in explorados:
            explorados.add(nodoExpandivel.estado)
            nodos = expande(nodoExpandivel)
            for nodo in nodos:
                fronteira.put(nodo)

    return None


def bfs(estado):
    if estado == '12345678_':
        return []

    nodoInicial = Nodo(estado, None, '', 0)
    explorados = set()
    fronteira = Queue(0)
    nodos = expande(nodoInicial)

    for nodo in nodos:
        fronteira.put(nodo)

    while fronteira.qsize() > 0:
        nodoExpandivel = fronteira.get()

        if nodoExpandivel.estado == '12345678_':
            return pegarCaminho(nodoExpandivel)

        if nodoExpandivel.estado not in explorados:
            explorados.add(nodoExpandivel.estado)
            nodos = expande(nodoExpandivel)
            for nodo in nodos:
                fronteira.put(nodo)

    return None



# A*


def getDistanciaHamming(estado):
    distancia = 0
    for i in range(1, 9):
        distancia += 1 if str(i) == estado[i] else 0
    return distancia

def getDistanciaManhattan(estado):
    distancia = 0
    for i in range(1, 9):
        if (estado[i] != '_'):
            distancia += abs(int(estado[i]) - i)
    return distancia


def astar_hamming(estado):
    if estado == '12345678_':
        return []

    nodoInicial = Nodo(estado, None, '', 0)
    explorados = set()
    fronteira = PriorityQueue()
    nodos = expande(nodoInicial)
    iterator = count()

    for nodo in nodos:
        fronteira.put(((nodo.custo + getDistanciaHamming(estado), next(iterator)),  nodo))

    while not fronteira.empty():
        nodoExpandivel = fronteira.get()[1]

        if nodoExpandivel.estado == '12345678_':
            return pegarCaminho(nodoExpandivel)

        if nodoExpandivel.estado not in explorados:
            explorados.add(nodoExpandivel.estado)
            nodos = expande(nodoExpandivel)
            for nodo in nodos:
                fronteira.put(((nodo.custo + getDistanciaHamming(estado), next(iterator)), nodo))

    return None

def astar_manhattan(estado):
    if estado == '12345678_':
        return []

    nodoInicial = Nodo(estado, None, '', getDistanciaManhattan(estado))
    explorados = set()
    fronteira = PriorityQueue()
    nodos = expande(nodoInicial)
    iterator = count()

    for nodo in nodos:
        fronteira.put(((nodo.custo + getDistanciaManhattan(estado), next(iterator)),  nodo))

    while not fronteira.empty():
        nodoExpandivel = fronteira.get()[1]

        if nodoExpandivel.estado == '12345678_':
            return pegarCaminho(nodoExpandivel)

        if nodoExpandivel.estado not in explorados:
            explorados.add(nodoExpandivel.estado)
            nodos = expande(nodoExpandivel)
            for nodo in nodos:
                fronteira.put(((nodo.custo + getDistanciaManhattan(estado), next(iterator)), nodo))

    return None


