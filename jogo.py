import random
import time
from collections import Counter

# Estatísticas
def exibir_conhecimento_ia():
    conhecimento_ia.sort()
    for vetor in enumerate(conhecimento_ia):
        print(f"{vetor}")

def exibir_jogadas_inteligentes():
    for vetor in enumerate(jogadas_inteligentes):
        print(f"{vetor}")

def exibir_estatisticas_finais(): # <======
    tempo_final = time.time()
    tempo_final -= tempo_inicio
    num_partidas = tabuleiro[10]
    media_jogadas = total_jogadas / num_partidas
    vitorias_j1 = tabuleiro[12]
    vitorias_j2 = tabuleiro[14]
    velhas = tabuleiro[13]

    print("\nEstatísticas Finais:")
    print(f"Número de partidas jogadas: {num_partidas}")
    print(f"Média de jogadas de todas as partidas: {media_jogadas:.2f}")
    print(f"Quantidade de vitórias do jogador 1: {vitorias_j1} ({((vitorias_j1 / num_partidas) * 100):.2f}%)")
    print(f"Quantidade de vitórias do jogador 2: {vitorias_j2} ({((vitorias_j2 / num_partidas) * 100):.2f}%)")
    print(f"Quantidade de empates: {velhas} ({((velhas / num_partidas) * 100):.2f}%)")
    print(f"Tempo para resultados finais: {tempo_final:.2f} segundos")

    zerar_tabuleiro(tabuleiro)

# Tabuleiro
def zerar_tabuleiro(tabuleiro):
    for i in range(15):
        tabuleiro[i] = 0

def jogada_valida(posicao):
    return 1 <= posicao <= 9 and tabuleiro[posicao] == 0

def verificar_posicao(jogador): # <====================
    for pos in range(1,10):
        if jogador == converter_valor(tabuleiro[pos]):
            return pos

def reiniciar_tabuleiro():
    for i in range(10):
        tabuleiro[i] = 0
    tabuleiro[10] += 1

def verificar_vitoria():
    combinacoes_vitoria = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],
        [1, 4, 7], [2, 5, 8], [3, 6, 9],
        [1, 5, 9], [3, 5, 7]
    ]

    for combinacao in combinacoes_vitoria:
        soma = sum(tabuleiro[pos] for pos in combinacao)
        if soma == 3:   # Jogador 1 vence
            return "X"
        elif soma == -3:  # Jogador 2 vence
            return "O"
    return None

def marcar_posicao(posicao, jogador):
    tabuleiro[posicao] = 1 if jogador == "X" else -1
    tabuleiro[0] += 1

def converter_valor(valor):
        if valor == 1:
            return "X"
        elif valor == -1:
            return "O"
        else:
            return " "

def exibir_tabuleiro():
    print("\n")
    print(f" {converter_valor(tabuleiro[1])} | {converter_valor(tabuleiro[2])} | {converter_valor(tabuleiro[3])} ")
    print("---+---+---")
    print(f" {converter_valor(tabuleiro[4])} | {converter_valor(tabuleiro[5])} | {converter_valor(tabuleiro[6])} ")
    print("---+---+---")
    print(f" {converter_valor(tabuleiro[7])} | {converter_valor(tabuleiro[8])} | {converter_valor(tabuleiro[9])} ")
    print("\n")

# Jogadas
def jogada_aleatorio(jogador):
    posicao_aleatorio = random.randint(1, 9)
    while not jogada_valida(posicao_aleatorio):
        posicao_aleatorio = random.randint(1, 9)
    marcar_posicao(posicao_aleatorio, jogador)
    
    return posicao_aleatorio

def jogada_campeao(jogador):
    posicao_campeao = ""
    quinas = [1, 3, 7, 9]
    bordas = [2, 4, 6, 8]
    meio = 5
    jogadas_validas_borda = [[1, 3, 5, 8], [1, 5, 6, 7], [3, 4, 5, 9], [2, 5, 7, 9]]
    adversario = "O" if jogador == "X" else "X"

    if tabuleiro[0] == 0:
        posicao_campeao = random.randint(1, 9)
    elif tabuleiro[0] == 1:
        if verificar_posicao(adversario) == meio:
            posicao_campeao = random.choice(quinas)
        else:
            posicao_campeao = meio
    elif tabuleiro[0] == 2:
        if verificar_posicao(jogador) in quinas and verificar_posicao(adversario) in quinas:
            posicao_campeao = random.choice(quinas)
            while not jogada_valida(posicao_campeao):
                posicao_campeao = random.choice(quinas)
        elif verificar_posicao(jogador) in quinas:
            if not verificar_posicao(adversario) == meio:
                posicao_campeao = meio
            else:
                posicao_campeao = random.choice(verificar_jogada_campeao(jogador))
        elif verificar_posicao(jogador) == meio and verificar_posicao(adversario) in bordas:
            if verificar_posicao(adversario) == 4 or verificar_posicao(adversario) == 6:
                posicao_campeao = verificar_posicao(adversario) - 3
            elif verificar_posicao(adversario) == 2 or verificar_posicao(adversario) == 8:
                posicao_campeao = verificar_posicao(adversario) - 1
        elif verificar_posicao(jogador) == meio and verificar_posicao(adversario) in quinas:
            posicao_campeao = random.choice(verificar_jogada_campeao(jogador))
            while posicao_campeao not in quinas:
                posicao_campeao = random.choice(verificar_jogada_campeao(jogador))
        elif jogador == any(converter_valor(tabuleiro[i]) for i in bordas) and tabuleiro[verificar_posicao(adversario)] not in jogadas_validas_borda[verificar_posicao(jogador) / 2]:
            posicao_campeao = meio
        else:
            if jogada_valida(meio):
                posicao_campeao = meio
            elif verificar_jogada_campeao(jogador):
                posicao_campeao = random.choice(verificar_jogada_campeao(jogador))
            else:
                posicao_campeao = random.randint(1, 9)
                while not jogada_valida(posicao_campeao):
                    posicao_campeao = random.randint(1, 9)
    else:
        if verificar_vitoria_bloqueio_campeao(jogador):
            posicao_campeao = verificar_vitoria_bloqueio_campeao(jogador)
        elif antecipar_vitoria_bloqueio_campeao(jogador):
            posicao_campeao = antecipar_vitoria_bloqueio_campeao(jogador)
        else:
            posicao_campeao = random.randint(1, 9)
            while not jogada_valida(posicao_campeao):
                posicao_campeao = random.randint(1, 9)

    marcar_posicao(posicao_campeao,jogador)

def antecipar_vitoria_bloqueio_campeao(jogador):
    combinacoes_vitoria = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],    # Linhas
        [1, 4, 7], [2, 5, 8], [3, 6, 9],    # Colunas
        [1, 5, 9], [3, 5, 7]                # Diagonais
    ]
    posicoes_ataque = []
    posicoes_defesa = []
    sequencia = 1 if jogador == "X" else -1
    sequencia_adversario = -1 if jogador == "X" else 1
    for combinacao in combinacoes_vitoria:
        soma = sum(tabuleiro[pos] for pos in combinacao)
        if soma == sequencia:
            for pos in combinacao:
                if tabuleiro[pos] == 0:
                    posicoes_ataque.append(pos)
    for combinacao in combinacoes_vitoria:
        soma = sum(tabuleiro[pos] for pos in combinacao)
        if soma == sequencia_adversario:
            for pos in combinacao:
                if tabuleiro[pos] == 0:
                    posicoes_defesa.append(pos)
    ataque_mais_comum = Counter(posicoes_ataque).most_common(1)
    defesa_mais_comum = Counter(posicoes_defesa).most_common(1)
    if ataque_mais_comum and defesa_mais_comum:
        if ataque_mais_comum[0][0] >= defesa_mais_comum[0][0]:
            pos = ataque_mais_comum[0][0]
        else:
            pos = defesa_mais_comum[0][0]
        return pos
    return None  

def verificar_jogada_campeao(jogador):
    combinacoes_vitoria = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],    # Linhas
        [1, 4, 7], [2, 5, 8], [3, 6, 9],    # Colunas
        [1, 5, 9], [3, 5, 7]                # Diagonais
    ]
    posicoes_validas = []
    sequencia = 1 if jogador == "X" else -1
    for combinacao in combinacoes_vitoria:
        soma = sum(tabuleiro[pos] for pos in combinacao)
        if soma == sequencia:
            for pos in combinacao:
                if tabuleiro[pos] == 0:
                    posicoes_validas.append(pos)
    return posicoes_validas

def verificar_vitoria_bloqueio_campeao(jogador):
    combinacoes_vitoria = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],    # Linhas
        [1, 4, 7], [2, 5, 8], [3, 6, 9],    # Colunas
        [1, 5, 9], [3, 5, 7]                # Diagonais
    ]
    sequencia = 2 if jogador == "X" else -2
    sequencia_adversario = -2 if jogador == "X" else 2
    for combinacao in combinacoes_vitoria:
        soma = sum(tabuleiro[pos] for pos in combinacao)
        if soma == sequencia:
            for pos in combinacao:
                if tabuleiro[pos] == 0:
                    return pos
    for combinacao in combinacoes_vitoria:
        soma = sum(tabuleiro[pos] for pos in combinacao)
        if soma == sequencia_adversario:
            for pos in combinacao:
                if tabuleiro[pos] == 0:
                    return pos
    return None

def jogada_inteligente(jogador):
    maior_pontuacao = -float('inf')
    jogada_ia = None
    posicao_inteligente = None
    jogadas_validas = []

    for jogada in conhecimento_ia:
        if jogada[:10] == tabuleiro[:10]:
            if jogada[11] > maior_pontuacao:
                jogadas_validas.clear()
                maior_pontuacao = jogada[11]
                jogadas_validas.append(jogada)
            elif jogada[11] == maior_pontuacao:
                jogadas_validas.append(jogada)
    if jogadas_validas:
        if maior_pontuacao >= 0:
            jogada_ia = random.choice(jogadas_validas)
            posicao_inteligente = jogada_ia[10]
            marcar_posicao(posicao_inteligente,jogador)
        else:
            jogadas_validas.clear()
            for jogada in conhecimento_ia:
                if jogada[:10] == tabuleiro[:10]:
                    jogadas_validas.append(jogada[10])
            jogada_ia = tabuleiro[:12]
            jogada_ia[10] = jogada_aleatorio(jogador)
            while jogada_ia[10] in jogadas_validas:
                jogada_ia[10] = jogada_aleatorio(jogador)
            posicao_inteligente = jogada_ia[10]
            jogada_ia[11] = 0
            conhecimento_ia.append(jogada_ia) 
    else:
        jogada_ia = tabuleiro[:12]
        posicao_inteligente = jogada_ia[10] = jogada_aleatorio(jogador)
        jogada_ia[11] = 0
        conhecimento_ia.append(jogada_ia)
        
    jogadas_inteligentes.append(jogada_ia)
    return posicao_inteligente

def pontuar_jogada_inteligente(ponto):
    for jogada in jogadas_inteligentes:
        for base in conhecimento_ia:
            if jogada[:11] == base[:11]:
                base[11] += ponto
                break

    jogadas_inteligentes.clear()

# Modos de jogo
def jogo_humano_vs_aleatorio():
    reiniciar_tabuleiro()
    while tabuleiro[0] < 9:
        exibir_tabuleiro()
        try:
            posicao = int(input("Escolha uma posição (1-9) para jogar: "))
            if not jogada_valida(posicao):
                print("Posição inválida! Tente novamente.")
                continue
            marcar_posicao(posicao, "X")
            vencedor = verificar_vitoria()
            if vencedor:
                tabuleiro[11] = 1 if vencedor == "X" else -1
                tabuleiro[12] += 1 if vencedor == "X" else 0
                tabuleiro[14] += 1 if vencedor == "O" else 0
                exibir_tabuleiro()
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar()
        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 9.")
            continue

        if tabuleiro[0] < 9:
            posicao_aleatorio = random.randint(1, 9)
            while not jogada_valida(posicao_aleatorio):
                posicao_aleatorio = random.randint(1, 9)
            marcar_posicao(posicao_aleatorio, "O")
            print(f"A máquina jogou na posição {posicao_aleatorio}.")
            vencedor = verificar_vitoria()
            if vencedor:
                tabuleiro[11] = -1 if vencedor == "O" else 1
                tabuleiro[12] += 1 if vencedor == "X" else 0
                tabuleiro[14] += 1 if vencedor == "O" else 0
                exibir_tabuleiro()
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar()

    tabuleiro[11] = 0
    tabuleiro[13] += 1
    exibir_tabuleiro()
    print("Empate! Deu velha!")
    perguntar_reiniciar()

def jogo_humano_vs_campeao():
    reiniciar_tabuleiro()
    while tabuleiro[0] < 9:
        exibir_tabuleiro()
        try:
            posicao = int(input("Escolha uma posição (1-9) para jogar: "))
            if not jogada_valida(posicao):
                print("Posição inválida! Tente novamente.")
                continue
            marcar_posicao(posicao, "X")
            vencedor = verificar_vitoria()
            if vencedor:
                tabuleiro[11] = 1 if vencedor == "X" else -1
                tabuleiro[12] += 1 if vencedor == "X" else 0
                tabuleiro[14] += 1 if vencedor == "O" else 0
                exibir_tabuleiro()
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar()
        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 9.")
            continue

        if tabuleiro[0] < 9:
            posicao_campeao = melhor_jogada_campeao("O")
            marcar_posicao(posicao_campeao, "O")
            vencedor = verificar_vitoria()
            if vencedor:
                tabuleiro[11] = -1 if vencedor == "O" else 1
                tabuleiro[12] += 1 if vencedor == "X" else 0
                tabuleiro[14] += 1 if vencedor == "O" else 0
                exibir_tabuleiro()
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar()

    tabuleiro[11] = 0
    tabuleiro[13] += 1
    exibir_tabuleiro()
    print("Empate! Deu velha!")
    perguntar_reiniciar()

def jogo_humano_vs_inteligente():
    reiniciar_tabuleiro()
    while tabuleiro[0] < 9:
        exibir_tabuleiro()
        try:
            posicao = int(input("Escolha uma posição (1-9) para jogar: "))
            if not jogada_valida(posicao):
                print("Posição inválida! Tente novamente.")
                continue
            marcar_posicao(posicao, "X")
            vencedor = verificar_vitoria()
            if vencedor:
                tabuleiro[11] = 1 if vencedor == "X" else -1
                tabuleiro[12] += 1 if vencedor == "X" else 0
                tabuleiro[14] += 1 if vencedor == "O" else 0
                exibir_tabuleiro()
                print(f"O jogador {vencedor} venceu!")
                pontuar_jogada_inteligente(-1)
                return perguntar_reiniciar()
        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 9.")
            continue

        if tabuleiro[0] < 9:
            posicao_inteligente = jogada_inteligente("O")
            print(f"O Jogador Inteligente jogou na posição {posicao_inteligente}.")
            exibir_jogadas_inteligentes()
            vencedor = verificar_vitoria()
            if vencedor:
                tabuleiro[11] = -1 if vencedor == "O" else 1
                tabuleiro[12] += 1 if vencedor == "X" else 0
                tabuleiro[14] += 1 if vencedor == "O" else 0
                exibir_tabuleiro()
                print(f"O jogador {vencedor} venceu!")
                pontuar_jogada_inteligente(1)
                return perguntar_reiniciar()

    tabuleiro[11] = 0
    tabuleiro[13] += 1
    exibir_tabuleiro()
    print("Empate! Deu velha!")
    perguntar_reiniciar()

def jogo_aleatorio_vs_aleatorio():
    reiniciar_tabuleiro()
    global total_jogadas

    while tabuleiro[0] < 9:
        jogador = "X" if tabuleiro[0] % 2 == 0 else "O"
        jogada_aleatorio(jogador)
        vencedor = verificar_vitoria()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1
            if vencedor == "X":
                tabuleiro[12] += 1
            else:
                tabuleiro[14] += 1
            resultados.append(tabuleiro[:])
            total_jogadas += tabuleiro[0]
            return
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    resultados.append(tabuleiro[:])
    total_jogadas += tabuleiro[0]

def jogo_campeao_vs_campeao():
    reiniciar_tabuleiro()
    global total_jogadas

    while tabuleiro[0] < 9:
        jogador = "X" if tabuleiro[0] % 2 == 0 else "O"
        jogada_campeao(jogador)
        vencedor = verificar_vitoria()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1
            if vencedor == "X":
                tabuleiro[12] += 1
            else:
                tabuleiro[14] += 1
            resultados.append(tabuleiro)
            total_jogadas += tabuleiro[0]
            return
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    resultados.append(tabuleiro)
    total_jogadas += tabuleiro[0]

# def jogo_inteligente_vs_inteligente():

def jogo_campeao_vs_aleatorio():
    reiniciar_tabuleiro()
    global total_jogadas, escolha, test

    while tabuleiro[0] < 9:
        jogador = "X" if tabuleiro[0] % 2 == 0 else "O"
        if (escolha == "1" and jogador == "X") or (escolha == "2" and jogador == "O"):
            jogada_campeao(jogador)
        else:
            jogada_aleatorio(jogador)
        vencedor = verificar_vitoria()
        exibir_tabuleiro()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1
            if vencedor == "X":
                tabuleiro[12] += 1
                test = 1
            else:
                tabuleiro[14] += 1
            resultados.append(tabuleiro)
            total_jogadas += tabuleiro[0]
            return
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    resultados.append(tabuleiro)
    total_jogadas += tabuleiro[0]

def jogo_inteligente_vs_aleatorio():
    reiniciar_tabuleiro()
    global total_jogadas, escolha
    ponto = 0

    while tabuleiro[0] < 9:
        jogador = "X" if tabuleiro[0] % 2 == 0 else "O"
        if (escolha == "1" and jogador == "X") or (escolha == "2" and jogador == "O"):
            jogada_inteligente(jogador)
        else:
            jogada_aleatorio(jogador)
        vencedor = verificar_vitoria()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1
            if vencedor == "X":
                tabuleiro[12] += 1
                if escolha == "1":
                    ponto = 1
                else:
                    ponto = -1
                    # exibir_jogadas_inteligentes()
                    # exibir_tabuleiro()
            else:
                tabuleiro[14] += 1
                if escolha == "1":
                    ponto = -1
                    # exibir_jogadas_inteligentes()
                    # exibir_tabuleiro()
                else:
                    ponto = 1
            resultados.append(tabuleiro)
            total_jogadas += tabuleiro[0]
            pontuar_jogada_inteligente(ponto)
            return
    pontuar_jogada_inteligente(ponto)
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    resultados.append(tabuleiro)
    total_jogadas += tabuleiro[0]

# def jogo_inteligente_vs_campeao():

# Opções de Jogo
def perguntar_reiniciar():
    print("\nO que deseja fazer agora?")
    print("1 - Menu principal")
    print("2 - Encerrar")
    escolha = input("Escolha uma opção (1 ou 2): ")
    while escolha not in ["1", "2"]:
        print("\nOpção inválida.\nO que deseja fazer agora?")
        print("1 - Menu principal")
        print("2 - Encerrar")
        escolha = input("Escolha uma opção (1 ou 2): ")
    if escolha == "1":
        menu_principal()
    else:
        print("Jogo encerrado. Obrigado por jogar!")
        exit()

def jogar_multiplas_partidas(modo_jogo, num_partidas): # <====================
    global total_jogadas, tempo_inicio, escolha
    total_jogadas = 0
    tempo_inicio = time.time()

    if not modo_jogo == jogo_aleatorio_vs_aleatorio:
        print("Quem começa primeiro Campeão/Inteligente ou Aleatório?")
        escolha = input("1 - Campeão/Inteligente ou 2 - Aleatório: ")
        while escolha not in ["1", "2"]:
            escolha = input("Opção inválida: 1 - Campeão/Inteligente ou 2 - Aleatório: ")

    for _ in range(num_partidas):
        modo_jogo()
    exibir_estatisticas_finais()

def menu_principal():
    print("\nEscolha uma opção:")
    print("1 - Jogador Humano vs Jogador Aleatório")
    print("2 - Jogador Humano vs Jogador Campeão")
    print("3 - Jogador Humano vs Jogador Inteligente")
    print("4 - Jogador Aleatório vs Jogador Aleatório (múltiplas partidas)")
    print("5 - Jogador Campeão vs Jogador Campeão (múltiplas partidas)")
    # print("6 - Jogador Inteligente vs Jogador Inteligente (múltiplas partidas)")
    print("7 - Jogador Campeão vs Jogador Aleatório (múltiplas partidas)")
    print("8 - Jogador Inteligente vs Jogador Aleatório (múltiplas partidas)")
    # print("9 - Jogador Inteligente vs Jogador Campeão (múltiplas partidas)")
    print("0 - Exibir base de conhecimento IA")
    print("(Escolha qualquer outro número para encerrar o jogo)")

    escolha = input("Digite: ")

    if escolha == "1":
        jogo_humano_vs_aleatorio()
    elif escolha == "2":
        jogo_humano_vs_campeao()
    elif escolha == "3":
        jogo_humano_vs_inteligente()
    elif escolha == "4":
        num_partidas = int(input("Quantas partidas deseja jogar? "))
        jogar_multiplas_partidas(jogo_aleatorio_vs_aleatorio, num_partidas)
    elif escolha == "5":
        num_partidas = int(input("Quantas partidas deseja jogar? "))
        jogar_multiplas_partidas(jogo_campeao_vs_campeao, num_partidas)
    # elif escolha == "6":
    #     num_partidas = int(input("Quantas partidas deseja jogar? "))
    #     jogar_multiplas_partidas(jogo_inteligente_vs_inteligente, num_partidas)
    elif escolha == "7":
        num_partidas = int(input("Quantas partidas deseja jogar? "))
        jogar_multiplas_partidas(jogo_campeao_vs_aleatorio, num_partidas)
    elif escolha == "8":
        num_partidas = int(input("Quantas partidas deseja jogar? "))
        jogar_multiplas_partidas(jogo_inteligente_vs_aleatorio, num_partidas)
    # elif escolha == "9":
    #     num_partidas = int(input("Quantas partidas deseja jogar? "))
    #     jogar_multiplas_partidas(jogo_inteligente_vs_campeao, num_partidas)
    elif escolha == "0":
        exibir_conhecimento_ia()
    else:
        print("Encerrando o jogo.")
        exit()

def iniciar_jogo():
    global tabuleiro, resultados, total_jogadas, jogadas_inteligentes, conhecimento_ia
    tabuleiro = [0] * 15
    resultados = []
    total_jogadas = 0
    jogadas_inteligentes = []
    conhecimento_ia = []
    
    while True:
        menu_principal()

# Inicia o jogo
iniciar_jogo()
