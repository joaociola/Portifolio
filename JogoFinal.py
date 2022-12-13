# Aluno: João Lucas Ciola
# Análise e desenvolvimento de sistemas
# Projeto final para matéria de Raciocínio computacional

from random import shuffle, choice
import time
from collections import namedtuple

print("-"*100, "\n \033[1;32m                                    BEM VINDO AO ZOMBIE DICE \033[m\n", "-"*100)
print("\033[4;35mO JOGO CONSISTE EM TENTAR A SORTE NOS DADOS, O ZUMBI QUE CONSEGUIR DEVORAR 13 CÉREBROS PRIMEIRO VENCE O JOGO!! "
      "\nLEVANDO 3 TIROS OS MAIS NA RODADA O ZUMBI FICA MUITO FERIDO, PERDE OS CÉREBROS DA RODADA E PRECISA TENTAR DE NOVO NA PRÓXIMA!!"
      "\nDADOS DE DIFERENTES CORES POSSUEM DIFERENTES QUANTIDADES DE PASSOS, CÉREBROS E TIROS."
      "\nO DADO VERMELHO POSSUI MAIS TIROS, O AMARELO POSSUI A MESMA QUANTIDADE DE PASSOS E CÉREBROS E APENAS UM TIRO"
      "\nO DADO VERDE É O QUE POSSUI MAIS CÉREBROS EM SEUS LADOS!!"
      "\nSE O SEU DADO VIRAR PARA A FACE INDICANDO PASSOS, SIGNIFICA QUE A SUA VÍTIMA FUGIU."
      "\nQUE VENÇA O MELHOR!!\033[m")
input("\n--> PRESSIONE ENTER PARA JOGAR")

# criando dados com tupla
def Dado():
    Dado = namedtuple("Dado", ['cor', 'lados'])
    verde = Dado('\033[32mVERDE\033[m', ['CEREBRO', 'CEREBRO', 'CEREBRO', 'PASSO', 'PASSO', 'TIRO'])
    vermelho = Dado('\033[31mVERMELHO\033[m', ['CEREBRO', 'PASSO', 'PASSO', 'TIRO', 'TIRO', 'TIRO'])
    amarelo = Dado('\033[33mAMARELO\033[m', ['CEREBRO', 'CEREBRO', 'PASSO', 'PASSO', 'TIRO', 'TIRO'])

    # adicionando os dados ao tubo
    tubo = []
    for i in range(6):
        tubo.append(verde)
    for i in range(3):
        tubo.append(vermelho)
    for i in range(4):
        tubo.append(amarelo)

    #embaralha os dados
    shuffle(tubo)
    return tubo #retorna os dados embaralhados

# criando jogadores usando classe definida
def listaJogadores ():
    global nome
    jogadores = []

    while True:
        try:
            totalJogadores = int(input("\n--> EM QUANTOS ZUMBIS ESTAMOS JOGANDO HOJE?? "))
            if totalJogadores > 1:
                break
            else:
                print("***CONVOQUE MAIS ZUMBIS PARA CAÇAR!!!!***")
        except ValueError:
            print("***QUANTIDADE DE JOGADORES INVÁLIDA!!***")

    for jogador in range(0, totalJogadores):
        nome = input(f"--> INSIRA O NOME DO {jogador+1}º ZUMBI: ").upper()
        jogador = {'nome': nome, 'score': 0} # dicionário com o nome como chave e score de valor
        jogadores.append(jogador) #adicionar a entrada do jogador à lista de jogadores
    #embaralhar os jogadores para jogar
    shuffle(jogadores)

    #imprimir a ordem embaralhada dos jogadores
    print("\n---\033[1mORDEM DO JOGO\033[m---\n")
    contador = 1
    for jogador in jogadores:
        print(f"-->{contador}. ZUMBI {jogador['nome']}")

    return jogadores

 #adicionando função da rodada para os jogadores
def rodada(jogador):
    global ladoSorteado, dado
    print(f"\n\n***ZUMBI {jogador['nome']}!! SUA VEZ DE CAÇAR!!***")
    time.sleep(0.4)

    tubo = Dado()
    scoreRodada = {'CEREBROS': 0, 'TIROS': 0}
    dadosAtuais = []

    while True:
        print("\n")
        # verificando os 3 dados para poder jogar:
        while len(dadosAtuais) < 3:
            dadosAtuais.append(tubo.pop())  # função pop tira o dado do tubo para o jogador

        contador = 1
        for dado in reversed(dadosAtuais):
            time.sleep(0.3)
            print(f"***JOGANDO DADO {contador}***")
            contador += 1

            cor = dado.cor
            shuffle(dado.lados) #embaralhando os lados do dado
            ladoSorteado = choice(dado.lados) #escolhendo um lado do dado já embaralhado

            print(f'-->COR: {cor}\n-->LADO:{ladoSorteado}')

            if ladoSorteado == 'CEREBRO':
                scoreRodada['CEREBROS'] = scoreRodada['CEREBROS'] + 1
                tubo.append(dadosAtuais.pop(dadosAtuais.index(dado)))
            elif ladoSorteado == 'TIRO':
                scoreRodada['TIROS'] = scoreRodada['TIROS'] + 1
                tubo.append(dadosAtuais.pop(dadosAtuais.index(dado)))

        shuffle(tubo)  # embaralha novamente o tubo quando devolve os dados
        print(f"\n--> CÉREBROS ATUAIS: {scoreRodada['CEREBROS']}\n--> TIROS ATUAIS: {scoreRodada['TIROS']}")
        # não é necessário fazer nenhuma ação para caso o dado tenha o lado sorteado para PASSOS,
        # pois nenhum ponto é somado e também o dado não volta para o tubo
        # caso o jogador não tenha levado 3 tiros ele pode jogar novamente os dados

        if scoreRodada['TIROS'] < 3:
            repetir = input("--> DESEJA ARRISCAR NOS DADOS NOVAMENTE? (S/N): ").strip().upper()
            if repetir == 'N':
                print(f"***VOCÊ CONSEGUIU {scoreRodada['CEREBROS']} CÉREBROS")
                jogador['score'] += scoreRodada['CEREBROS']
                break
        else:  # para 3 ou mais tiros
            print("***VOCÊ MORREU! TENTE DE NOVO NA PRÓXIMA RODADA!!!***")
            break

def pontuacao(jogadores):
    print("\n\033[7m***SCORE ATUAL***\033[m")
    for jogador in jogadores:
        print(f"{jogador['nome']}: {jogador['score']} CÉREBROS DEVORADOS")

jogadores = listaJogadores()

fimdeJogo = False
while not fimdeJogo:
    for jogador in jogadores:
        rodada(jogador)
        if jogador['score'] >= 13:
            vencedor = jogador['nome']
            fimdeJogo = True
        if not fimdeJogo:
            pontuacao(jogadores)
        else:
            print(f"\n\033[1;4;35m***FIM DE JOGO***\nZUMBI VENCEDOR: {vencedor}\033[m")

