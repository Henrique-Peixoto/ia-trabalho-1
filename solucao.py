from queue import Queue, LifoQueue

def determinarProximoEstado(acao, estado):
    posicaoEspacoVazio = estado.find('_')
    peca = ''

    if acao == 'esquerda':
        peca = estado[posicaoEspacoVazio-1:posicaoEspacoVazio]
    elif acao == 'direita':
        peca = estado[posicaoEspacoVazio+1:posicaoEspacoVazio+2]
    elif acao == 'acima':
        peca = estado[posicaoEspacoVazio-3:posicaoEspacoVazio-2]
    elif acao == 'abaixo':
        peca = estado[posicaoEspacoVazio+3:posicaoEspacoVazio+4]

    posicaoPeca = estado.find(peca)
    novoEstado = estado.replace('_', peca)
    novoEstado = novoEstado[:posicaoPeca] + '_' + novoEstado[posicaoPeca+1:]

    return acao, novoEstado


def sucessor(estado):
    posicaoEspacoVazio = estado.find('_')
    estadosPossiveis = []

    # Dois movimentos possíveis
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
    # Três movimentos possíveis
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
    # Quatro movimentos possíveis
    else:
        estadosPossiveis.append(determinarProximoEstado('acima', estado))
        estadosPossiveis.append(determinarProximoEstado('esquerda', estado))
        estadosPossiveis.append(determinarProximoEstado('direita', estado))
        estadosPossiveis.append(determinarProximoEstado('abaixo', estado))

    return estadosPossiveis

class Nodo:
    def __init__(self, pai, estado, acao, custo):
        self.pai = pai
        self.estado = estado
        self.acao = acao
        self.custo = custo

    def __str__(self):
        return f'Nodo ->' \
               f'\nPai: {self.pai}, ' \
               f'\nEstado: {self.estado}, ' \
               f'\nAção: {self.acao},' \
               f'\nCusto: {self.custo}' \
               f'\n'


def expande(nodo):
    estadosPossiveis = sucessor(nodo.estado)
    nodos = []

    for tupla in estadosPossiveis:
        acao = tupla[0]
        estado = tupla[1]
        novoNodo = Nodo(nodo, estado, acao, nodo.custo+1)
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

    nodoInicial = Nodo(None, estado, '', 0)
    explorados = set()
    fronteira = LifoQueue(0)
    nodos = expande(nodoInicial)

    for nodo in nodos:
        fronteira.put(nodo)

    while fronteira.qsize() > 0:
        nodoExpandivel = fronteira.get()

        if (nodoExpandivel.estado == '12345678_'):
            return pegarCaminho(nodoExpandivel)

        if nodoExpandivel not in explorados:
            explorados.add(nodoExpandivel)
            nodos = expande(nodoExpandivel)
            for nodo in nodos:
                fronteira.put(nodo)

    return None


def bfs(estado):
    if estado == '12345678_':
        return []

    nodoInicial = Nodo(None, estado, '', 0)
    explorados = set()
    fronteira = Queue(0)
    nodos = expande(nodoInicial)

    for nodo in nodos:
        fronteira.put(nodo)

    while fronteira.qsize() > 0:
        nodoExpandivel = fronteira.get()

        if nodoExpandivel.estado == '12345678_':
            return pegarCaminho(nodoExpandivel)

        if nodoExpandivel not in explorados:
            explorados.add(nodoExpandivel)
            nodos = expande(nodoExpandivel)
            for nodo in nodos:
                fronteira.put(nodo)

    return None


print(dfs('123456_78'))
print(bfs('123456_78'))
