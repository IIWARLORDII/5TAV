import random
import time
import csv
from collections import Counter

# Estatísticas
def exibir_conhecimento_ia():
    conhecimento_ia.sort()
    for vetor in enumerate(conhecimento_ia):
        print(f"{vetor}")

def exibir_jogadas(jogadas):
    for jogada in jogadas[-tabuleiro[0]:]:
        print(f"Partida: {tabuleiro[10]}")
        exibir_tabuleiro(jogada)

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

    # for vetor in enumerate(resultados):
    #     print(f"{vetor}")
    gerar_relatorio()
    zerar_tabuleiro()

def gerar_relatorio():
    # Nome do arquivo CSV
    nome_arquivo = "relatorio.csv"

    # Definindo os nomes das colunas
    colunas = ["Jogadas", "Tabuleiro", "Partida", "Resultado", "Vitorias J1", "Velhas", "Vitorias J2"]

    # Criando o arquivo CSV e escrevendo os dados
    with open(nome_arquivo, mode="w", newline="") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv, delimiter=";")

        # Escrever cabeçalho
        escritor_csv.writerow(colunas)

        # Escrever cada vetor na lista como uma linha no CSV
        for resultado in resultados:
            linha = [
                resultado[0],                      # Jogadas
                ",".join(map(str, resultado[1:10])),  # Tabuleiro (posição 1 até 9, separados por vírgula)
                resultado[10],                     # Partida
                resultado[11],                     # Resultado
                resultado[12],                     # Vitorias J1
                resultado[13],                     # Velhas
                resultado[14]                      # Vitorias J2
            ]
            escritor_csv.writerow(linha)

    print(f"Arquivo '{nome_arquivo}' criado com sucesso!")

    # # Transformar a lista em um DataFrame, criando colunas com os valores correspondentes
    # df = pd.DataFrame({
    #     "Jogadas": [resultado[0] for resultado in resultados],
    #     "Tabuleiro": [",".join(map(str, resultado[1:10])) for resultado in resultados],  # Combina posições 1 a 9 em uma string
    #     "Partida": [resultado[10] for resultado in resultados],
    #     "Resultado": [resultado[11] for resultado in resultados],
    #     "Vitorias J1": [resultado[12] for resultado in resultados],
    #     "Velhas": [resultado[13] for resultado in resultados],
    #     "Vitorias J2": [resultado[14] for resultado in resultados]
    # })

    # # Salvar no arquivo CSV
    # nome_arquivo = "realtorio.csv"
    # df.to_csv(nome_arquivo, index=False, sep=";")

    # print(f"Arquivo '{nome_arquivo}' criado com sucesso!")

# Tabuleiro
def zerar_tabuleiro():
    for i in range(15):
        tabuleiro[i] = 0

def jogada_valida(posicao):
    return 1 <= posicao <= 9 and tabuleiro[posicao] == 0

def verificar_posicoes(jogador): # <====================
    posicoes = []
    for pos in range(1,10):
        if jogador == converter_valor(tabuleiro[pos]):
            posicoes.append(pos)
    return posicoes

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

def exibir_tabuleiro(tabuleiro):
    print("\n")
    print(f" {converter_valor(tabuleiro[1])} | {converter_valor(tabuleiro[2])} | {converter_valor(tabuleiro[3])} ")
    print("---+---+---")
    print(f" {converter_valor(tabuleiro[4])} | {converter_valor(tabuleiro[5])} | {converter_valor(tabuleiro[6])} ")
    print("---+---+---")
    print(f" {converter_valor(tabuleiro[7])} | {converter_valor(tabuleiro[8])} | {converter_valor(tabuleiro[9])} ")
    print("\n")

# Jogadas
def jogada_humano(jogador):
    posicao_humano = None
    while not posicao_humano:
        try:
            posicao_humano = int(input("Escolha uma posição (1-9) para jogar: "))
            if not jogada_valida(posicao_humano):
                print("Posição inválida! Tente novamente.")
                continue
            marcar_posicao(posicao_humano, jogador)
            return posicao_humano
        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 9.")
            continue

def jogada_aleatorio(jogador):
    posicao_aleatorio = random.randint(1, 9)
    while not jogada_valida(posicao_aleatorio):
        posicao_aleatorio = random.randint(1, 9)
    marcar_posicao(posicao_aleatorio, jogador)
    
    return posicao_aleatorio

def jogada_campeao(jogador):
    quinas = [1, 3, 7, 9]
    meio = 5
    adversario = "O" if jogador == "X" else "X"

    # print(f"\nJogadas: {tabuleiro[0]}\nJogador: {jogador} Adversário: {adversario}") # =======================
    # exibir_tabuleiro(tabuleiro) # ===========================

    if tabuleiro[0] == 0:
        posicao_campeao = 1
    elif tabuleiro[0] == 1:
        if verificar_posicoes(adversario)[0] == meio:
            posicao_campeao = 1
        else:
            posicao_campeao = meio
    elif tabuleiro[0] == 2:
        if verificar_posicoes(adversario)[0] == meio:
            posicao_campeao = 9
        elif verificar_posicoes(adversario)[0] in [4, 7]:
            posicao_campeao = 3
        else:
            posicao_campeao = 7
    elif tabuleiro[0] == 3:
        if verificar_posicoes(jogador)[0] == 1:
            if verificar_vitoria_bloqueio_campeao(jogador):
                posicao_campeao = verificar_vitoria_bloqueio_campeao(jogador)
            else:
                posicao_campeao = 3
        else:
            if verificar_vitoria_bloqueio_campeao(jogador):
                posicao_campeao = verificar_vitoria_bloqueio_campeao(jogador)
            else:
                posicoes_adversario = verificar_posicoes(adversario)
                if any(pos in quinas for pos in posicoes_adversario):
                    if all(pos in quinas for pos in posicoes_adversario):
                        posicao_campeao = 4
                    else:
                        if posicoes_adversario in [[1,6],[1,8]]:
                            posicao_campeao = 9
                        elif posicoes_adversario in [[3,4],[3,8]]:
                            posicao_campeao = 7
                        elif posicoes_adversario in [[2,7],[6,7]]:
                            posicao_campeao = 3
                        else:
                            posicao_campeao = 1
                else:
                    if posicoes_adversario in [[4,8],[6,8]]:
                        posicao_campeao = 7
                    else:
                        posicao_campeao = 1            
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
    # input("Continua?") # =========================
    # print(f"Jogador {jogador} jogou na posição: {posicao_campeao}") # ======================
    return posicao_campeao

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

def antecipar_vitoria_bloqueio_campeao(jogador):
    combinacoes_vitoria = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],    # Linhas
        [1, 4, 7], [2, 5, 8], [3, 6, 9],    # Colunas
        [1, 5, 9], [3, 5, 7]                # Diagonais
    ]
    posicoes_ataque = []
    posicoes_defesa = []
    sequencia = 1 if jogador == "X" else -1
    sequencia_adversario = sequencia * -1
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
    defesa_mais_comum = [[0]]
    # defesa_mais_comum = Counter(posicoes_defesa).most_common(1)
    if ataque_mais_comum and defesa_mais_comum:
        if ataque_mais_comum[0][0] >= defesa_mais_comum[0][0]:
            pos = ataque_mais_comum[0][0]
        else:
            pos = defesa_mais_comum[0][0]
        return pos
    return None 

def jogada_inteligente(jogador):
    maior_pontuacao = -2**31 # float('inf') ou -2**31
    jogadas_validas = []
    jogada_ia = None
    # posicao_inteligente = None

    jogadas_jogador = jogadas_inteligentes if jogador == "X" else jogadas_inteligentes2
    for jogada in conhecimento_ia:
        if jogada[:10] == tabuleiro[:10]:
            if jogada[11] > maior_pontuacao:
                # print(f"Maior rank achado em: {jogada}")
                maior_pontuacao = jogada[11]
                jogadas_validas.clear()
                jogadas_validas.append(jogada)
            elif jogada[11] == maior_pontuacao:
                # print(f"Mais um rank alto achado em: {jogada}")
                jogadas_validas.append(jogada)
    if jogadas_validas:
        # print(f"Tem na base")
        if maior_pontuacao >= 0:
            # print(f"Maior rank >= 0")
            jogada_ia = random.choice(jogadas_validas)
        else:
            # print(f"Maior rank < 0")
            posicoes_validas = [pos[10] for pos in conhecimento_ia if pos[:10] == tabuleiro[:10]]
            jogadas_possiveis = []
            for i in range(1,10):
                if jogada_valida(i) and i not in posicoes_validas:
                    jogada_ia = tabuleiro[:12]
                    jogada_ia[10] = i
                    jogada_ia[11] = 0
                    jogadas_possiveis.append(jogada_ia[:])
            if jogadas_possiveis:
                # print(f"Tem mais jogadas pra base")
                jogada_ia = random.choice(jogadas_possiveis)
                conhecimento_ia.append(jogada_ia[:])
            else:
                # print(f"Não tem mais jogadas pra base")
                jogada_ia = random.choice(jogadas_validas)
        posicao_inteligente = jogada_ia[10]
        marcar_posicao(posicao_inteligente,jogador)
    else:
        # print(f"Não tem na base")
        jogada_ia = tabuleiro[:12]
        posicao_inteligente = jogada_ia[10] = jogada_aleatorio(jogador)
        jogada_ia[11] = 0
        conhecimento_ia.append(jogada_ia[:])
        # exibir_conhecimento_ia()
    jogadas_jogador.append(jogada_ia[:])
    return posicao_inteligente

def pontuar_jogada_inteligente(jogador, ponto):
    jogadas_jogador = jogadas_inteligentes if jogador == "X" else jogadas_inteligentes2
    for jogada in jogadas_jogador:
        for base in conhecimento_ia:
            if jogada[:11] == base[:11]:
                base[11] += ponto
                break
    jogadas_jogador.clear()

# Modos de jogo
def jogo_humano_vs_aleatorio():
    zerar_tabuleiro()

    print("Quem começa primeiro Humano ou Aleatório")
    escolha = input("1 - Humano ou 2 - Aleatório: ")
    while escolha not in ["1", "2"]:
        print("Opção inválida! Escolha novamente:")
        escolha = input("1 - Humano ou 2 - Aleatório: ")
    # jogador1 = "Humano" if escolha == 1 else "Aleatório"
    # jogador2 = "Aleatório" if escolha == 1 else "Humano"

    exibir_tabuleiro(tabuleiro)
    while tabuleiro[0] < 9:
        
        jogador = "X" if tabuleiro[0] % 2 == 0 else "O"
        if (escolha == "1" and jogador == "X") or (escolha == "2" and jogador == "O"):
            jogada_humano(jogador)
        else:
            posicao_aleatorio = jogada_aleatorio(jogador)
            print(f"Jogador Aleatório jogou na posição {posicao_aleatorio}")
        exibir_tabuleiro(tabuleiro)
        vencedor = verificar_vitoria()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1
            if vencedor == "X":
                tabuleiro[12] += 1
                print(f"Vitória do Jogador 1!")
            else:
                tabuleiro[14] += 1
                print(f"Vitória do Jogador 2!")
            resultados.append(tabuleiro[:])
            return perguntar_reiniciar()
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    exibir_tabuleiro(tabuleiro)
    print("Empate! Deu velha!")
    resultados.append(tabuleiro[:])
    perguntar_reiniciar()

def jogo_humano_vs_campeao():
    zerar_tabuleiro()

    print("Quem começa primeiro Humano ou Campeão")
    escolha = input("1 - Humano ou 2 - Campeão: ")
    while escolha not in ["1", "2"]:
        print("Opção inválida! Escolha novamente:")
        escolha = input("1 - Humano ou 2 - Campeão: ")

    exibir_tabuleiro(tabuleiro)
    while tabuleiro[0] < 9:
        
        jogador = "X" if tabuleiro[0] % 2 == 0 else "O"
        if (escolha == "1" and jogador == "X") or (escolha == "2" and jogador == "O"):
            jogada_humano(jogador)
        else:
            posicao_campeao = jogada_campeao(jogador)
            print(f"Jogador Campeão jogou na posição {posicao_campeao}")
        exibir_tabuleiro(tabuleiro)
        vencedor = verificar_vitoria()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1
            if vencedor == "X":
                tabuleiro[12] += 1
                print(f"Vitória do Jogador 1!")
            else:
                tabuleiro[14] += 1
                print(f"Vitória do Jogador 2!")
            resultados.append(tabuleiro[:])
            return perguntar_reiniciar()
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    exibir_tabuleiro(tabuleiro)
    print("Empate! Deu velha!")
    resultados.append(tabuleiro[:])
    perguntar_reiniciar()

def jogo_humano_vs_inteligente():
    ponto = 0
    zerar_tabuleiro()

    print("Quem começa primeiro Humano ou Inteligente")
    escolha = input("1 - Humano ou 2 - Inteligente: ")
    while escolha not in ["1", "2"]:
        print("Opção inválida! Escolha novamente:")
        escolha = input("1 - Humano ou 2 - Inteligente: ")

    exibir_tabuleiro(tabuleiro)
    while tabuleiro[0] < 9:
        # input("Continua?")
        jogador = "X" if tabuleiro[0] % 2 == 0 else "O"
        if (escolha == "1" and jogador == "X") or (escolha == "2" and jogador == "O"):
            jogada_humano(jogador)
        else:
            posicao_inteligente = jogada_inteligente(jogador, jogadas_inteligentes)
            print(f"Jogador Inteligente jogou na posição {posicao_inteligente}")
        exibir_tabuleiro(tabuleiro)
        vencedor = verificar_vitoria()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1
            if (vencedor == "X" and escolha == "1") or (vencedor == "O" and escolha == "2"):
                tabuleiro[12] += 1
                ponto = -1
                print(f"Vitória do Jogador 1!")
            else:
                tabuleiro[14] += 1
                ponto = 1
                print(f"Vitória do Jogador 2!")
            resultados.append(tabuleiro[:])
            # exibir_jogadas_inteligentes()
            pontuar_jogada_inteligente(ponto, jogadas_inteligentes)
            # exibir_jogadas_inteligentes()
            return perguntar_reiniciar()
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    exibir_tabuleiro(tabuleiro)
    print("Empate! Deu velha!")
    pontuar_jogada_inteligente(ponto, jogadas_inteligentes)
    resultados.append(tabuleiro[:])
    perguntar_reiniciar()

def jogo_aleatorio_vs_aleatorio():
    global total_jogadas
    reiniciar_tabuleiro()

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
            resultados.append(tabuleiro[:])
            total_jogadas += tabuleiro[0]
            return
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    resultados.append(tabuleiro[:])
    total_jogadas += tabuleiro[0]

def jogo_inteligente_vs_inteligente():
    reiniciar_tabuleiro()
    global total_jogadas, jogadas_inteligentes2
    jogadas_inteligentes2 = []
    ponto = 0
    ponto2 = 0

    while tabuleiro[0] < 9:
        jogador = "X" if tabuleiro[0] % 2 == 0 else "O"
        jogada_inteligente(jogador)
        vencedor = verificar_vitoria()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1
            if vencedor == "X":
                tabuleiro[12] += 1
                ponto = 1
                ponto2 = -1
            else:
                tabuleiro[14] += 1
                ponto = -1
                ponto2 = 1
            resultados.append(tabuleiro[:])
            total_jogadas += tabuleiro[0]
            pontuar_jogada_inteligente("X", ponto)
            pontuar_jogada_inteligente("O", ponto2)
            return
    pontuar_jogada_inteligente("X", ponto)
    pontuar_jogada_inteligente("O", ponto2)
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    resultados.append(tabuleiro[:])
    total_jogadas += tabuleiro[0]

def jogo_campeao_vs_aleatorio():
    reiniciar_tabuleiro()
    global total_jogadas

    while tabuleiro[0] < 9:
        jogador = "X" if tabuleiro[0] % 2 == 0 else "O"
        if (escolha == "1" and jogador == "X") or (escolha == "2" and jogador == "O"):
            jogada_campeao(jogador)
        else:
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

def jogo_inteligente_vs_aleatorio():
    reiniciar_tabuleiro()
    global total_jogadas, escolha
    jogadas = [] # =============
    ponto = 0

    while tabuleiro[0] < 9:
        jogador = "X" if tabuleiro[0] % 2 == 0 else "O"
        if (escolha == "1" and jogador == "X") or (escolha == "2" and jogador == "O"):
            jogada_inteligente(jogador, jogadas_inteligentes)
        else:
            jogada_aleatorio(jogador)
        # jogadas.append(tabuleiro[:10])
        vencedor = verificar_vitoria()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1
            if (vencedor == "X" and escolha == "1") or (vencedor == "O" and escolha == "2"):
                tabuleiro[12] += 1
                ponto = 1
            else:
                tabuleiro[14] += 1
                ponto = -1
                # exibir_jogadas(jogadas) # ===========
                # input("Continuar?")
            resultados.append(tabuleiro[:])
            total_jogadas += tabuleiro[0]
            return pontuar_jogada_inteligente(ponto, jogadas_inteligentes)
    pontuar_jogada_inteligente(ponto, jogadas_inteligentes)
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    resultados.append(tabuleiro[:])
    total_jogadas += tabuleiro[0]

def jogo_inteligente_vs_campeao():
    reiniciar_tabuleiro()
    global total_jogadas, escolha
    jogadas = [] # =============
    ponto = 0

    while tabuleiro[0] < 9:
        jogador = "X" if tabuleiro[0] % 2 == 0 else "O"
        if (escolha == "1" and jogador == "X") or (escolha == "2" and jogador == "O"):
            jogada_inteligente(jogador, jogadas_inteligentes)
        else:
            jogada_campeao(jogador)
        # jogadas.append(tabuleiro[:10])
        vencedor = verificar_vitoria()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1
            if (vencedor == "X" and escolha == "1") or (vencedor == "O" and escolha == "2"):
                tabuleiro[12] += 1
                ponto = 1
            else:
                tabuleiro[14] += 1
                ponto = -1
                # exibir_jogadas(jogadas) # ===========
                # input("Continuar?")
            resultados.append(tabuleiro[:])
            total_jogadas += tabuleiro[0]
            return pontuar_jogada_inteligente(ponto, jogadas_inteligentes)
    pontuar_jogada_inteligente(ponto, jogadas_inteligentes)
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    resultados.append(tabuleiro[:])
    total_jogadas += tabuleiro[0]

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
    escolha = None

    if not modo_jogo == jogo_aleatorio_vs_aleatorio and not modo_jogo == jogo_campeao_vs_campeao and not modo_jogo == jogo_inteligente_vs_inteligente:
        print(f"Quem começa primeiro {jogadores[0]} ou {jogadores[1]}?")
        escolha = input(f"1 - {jogadores[0]} ou 2 - {jogadores[1]}: ")
        while escolha not in ["1", "2"]:
            print("Opção inválida! Escolha novamente:")
            escolha = input(f"1 - {jogadores[0]} ou 2 - {jogadores[1]}: ")

    for _ in range(num_partidas):
        modo_jogo()
    exibir_estatisticas_finais()
    perguntar_reiniciar()

def menu_principal():
    global jogadores

    print("\nEscolha uma opção:")
    print("1 - Jogador Humano vs Jogador Aleatório")
    print("2 - Jogador Humano vs Jogador Campeão")
    print("3 - Jogador Humano vs Jogador Inteligente")
    print("4 - Jogador Aleatório vs Jogador Aleatório (múltiplas partidas)")
    print("5 - Jogador Campeão vs Jogador Campeão (múltiplas partidas)")
    print("6 - Jogador Inteligente vs Jogador Inteligente (múltiplas partidas)")
    print("7 - Jogador Campeão vs Jogador Aleatório (múltiplas partidas)")
    print("8 - Jogador Inteligente vs Jogador Aleatório (múltiplas partidas)")
    print("9 - Jogador Inteligente vs Jogador Campeão (múltiplas partidas)")
    print("0 - Exibir base de conhecimento IA")
    print("(Escolha qualquer outro número para encerrar o jogo)")

    escolha = input("Escolha: ")

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
    elif escolha == "6":
        num_partidas = int(input("Quantas partidas deseja jogar? "))
        jogar_multiplas_partidas(jogo_inteligente_vs_inteligente, num_partidas)
    elif escolha == "7":
        jogadores = ["Campeão", "Aleatório"]
        num_partidas = int(input("Quantas partidas deseja jogar? "))
        jogar_multiplas_partidas(jogo_campeao_vs_aleatorio, num_partidas)
    elif escolha == "8":
        jogadores = ["Inteligente", "Aleatório"]
        num_partidas = int(input("Quantas partidas deseja jogar? "))
        jogar_multiplas_partidas(jogo_inteligente_vs_aleatorio, num_partidas)
    elif escolha == "9":
        jogadores = ["Inteligente", "Campeão"]
        num_partidas = int(input("Quantas partidas deseja jogar? "))
        jogar_multiplas_partidas(jogo_inteligente_vs_campeao, num_partidas)
    elif escolha == "0":
        exibir_conhecimento_ia()
    else:
        print("Encerrando o jogo.")
        exit()

def iniciar_jogo():
    global tabuleiro, resultados, total_jogadas, jogadas_inteligentes, conhecimento_ia, jogadores
    tabuleiro = [0] * 15
    resultados = []
    total_jogadas = 0
    jogadores = []
    jogadas_inteligentes = []
    conhecimento_ia = []
    
    while True:
        menu_principal()

# Inicia o jogo
iniciar_jogo()
