import random
import sqlite3

def init_db():
    conn = sqlite3.connect('jogo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultados (
            partida INTEGER,
            jogada INTEGER,
            posicoes TEXT,
            resultado INTEGER,
            vitoria_jogador1 INTEGER,
            empate INTEGER,
            vitoria_jogador2 INTEGER
        )
    ''')
    conn.commit()
    return conn

def jogada_valida(posicao):
    return 1 <= posicao <= 9 and tabuleiro[posicao] == 0

def armazenar_resultado(conn, tabuleiro):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO resultados (partida, jogada, posicoes, resultado, vitoria_jogador1, empate, vitoria_jogador2)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (tabuleiro[10], tabuleiro[0], ','.join(map(str, tabuleiro[1:10])), tabuleiro[11], tabuleiro[12], tabuleiro[13], tabuleiro[14]))
    conn.commit()

def exibir_resultados(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resultados')
    resultados = cursor.fetchall()

    if not resultados:
        print("Nenhum resultado encontrado.")
        return

    print("\nResultados das Partidas:")
    print("Partida | Jogada | Posições | Resultado | Vitórias J1 | Empates | Vitórias J2")
    print("-" * 70)
    for resultado in resultados:
        print(f"{resultado[0]:<7} | {resultado[1]:<6} | {resultado[2]:<9} | {resultado[3]:<9} | {resultado[4]:<13} | {resultado[5]:<7} | {resultado[6]:<13}")
    print("-" * 70)

def obter_estatisticas(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resultados ORDER BY partida DESC LIMIT 1;')
    resultado = cursor.fetchone()

    if resultado:
        partida_atual = resultado[0] + 1
        vitorias_j1 = resultado[4]
        empates = resultado[5]
        vitorias_j2 = resultado[6]
    else:
        partida_atual = 1
        vitorias_j1 = 0
        empates = 0
        vitorias_j2 = 0

    return partida_atual, vitorias_j1, empates, vitorias_j2

def limpar_tabela(conn):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM resultados')
    conn.commit()
    print("Tabela limpa com sucesso!")

def reiniciar_tabuleiro(conn):
    global tabuleiro
    partida_atual, vitorias_j1, empates, vitorias_j2 = obter_estatisticas(conn)
    tabuleiro = [0] * 15
    tabuleiro[10] = partida_atual
    tabuleiro[12] = vitorias_j1
    tabuleiro[13] = empates
    tabuleiro[14] = vitorias_j2
    tabuleiro[0] = 0

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

def exibir_tabuleiro():
    def converter_valor(valor):
        if valor == 1:
            return "X"
        elif valor == -1:
            return "O"
        else:
            return " "

    print("\n")
    print(f" {converter_valor(tabuleiro[1])} | {converter_valor(tabuleiro[2])} | {converter_valor(tabuleiro[3])} ")
    print("---+---+---")
    print(f" {converter_valor(tabuleiro[4])} | {converter_valor(tabuleiro[5])} | {converter_valor(tabuleiro[6])} ")
    print("---+---+---")
    print(f" {converter_valor(tabuleiro[7])} | {converter_valor(tabuleiro[8])} | {converter_valor(tabuleiro[9])} ")
    print("\n")

def minimax(profundidade, jogador):
    vencedor = verificar_vitoria()
    if vencedor == "X":
        return 1  # Vitória para X
    elif vencedor == "O":
        return -1  # Vitória para O
    elif tabuleiro[0] == 9:
        return 0  # Empate

    if jogador == "X":
        melhor_valor = -float('inf')
        for posicao in range(1, 10):
            if jogada_valida(posicao):
                marcar_posicao(posicao, "X")
                valor = minimax(profundidade + 1, "O")
                tabuleiro[posicao] = 0
                tabuleiro[0] -= 1
                melhor_valor = max(melhor_valor, valor)
        return melhor_valor
    else:
        melhor_valor = float('inf')
        for posicao in range(1, 10):
            if jogada_valida(posicao):
                marcar_posicao(posicao, "O")
                valor = minimax(profundidade + 1, "X")
                tabuleiro[posicao] = 0
                tabuleiro[0] -= 1
                melhor_valor = min(melhor_valor, valor)
        return melhor_valor

def melhor_jogada_campeao(jogador):
    melhor_valor = -float('inf') if jogador == "X" else float('inf')
    melhor_jogada = None
    for posicao in range(1, 10):
        if jogada_valida(posicao):
            marcar_posicao(posicao, jogador)
            valor = minimax(0, "O" if jogador == "X" else "X")
            tabuleiro[posicao] = 0
            tabuleiro[0] -= 1
            if (jogador == "X" and valor > melhor_valor) or (jogador == "O" and valor < melhor_valor):
                melhor_valor = valor
                melhor_jogada = posicao
    return melhor_jogada

# Modos de jogo
def jogo_jogador_vs_maquina(conn):
    reiniciar_tabuleiro(conn)
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
                armazenar_resultado(conn, tabuleiro)
                exibir_tabuleiro()
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar(conn)
        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 9.")
            continue

        if tabuleiro[0] < 9:
            posicao_maquina = random.randint(1, 9)
            while not jogada_valida(posicao_maquina):
                posicao_maquina = random.randint(1, 9)
            marcar_posicao(posicao_maquina, "O")
            print(f"A máquina jogou na posição {posicao_maquina}.")
            vencedor = verificar_vitoria()
            if vencedor:
                tabuleiro[11] = -1 if vencedor == "O" else 1
                tabuleiro[12] += 1 if vencedor == "X" else 0
                tabuleiro[14] += 1 if vencedor == "O" else 0
                armazenar_resultado(conn, tabuleiro)
                exibir_tabuleiro()
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar(conn)

    tabuleiro[11] = 0
    tabuleiro[13] += 1
    armazenar_resultado(conn, tabuleiro)
    exibir_tabuleiro()
    print("Empate! Deu velha!")
    perguntar_reiniciar(conn)

def jogo_maquina_vs_maquina(conn):
    reiniciar_tabuleiro(conn)
    while tabuleiro[0] < 9:
        posicao1 = random.randint(1, 9)
        while not jogada_valida(posicao1):
            posicao1 = random.randint(1, 9)
        marcar_posicao(posicao1, "X")
        print(f"Máquina 1 jogou na posição {posicao1}.")
        exibir_tabuleiro()
        vencedor = verificar_vitoria()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1
            tabuleiro[12] += 1 if vencedor == "X" else 0
            tabuleiro[14] += 1 if vencedor == "O" else 0
            armazenar_resultado(conn, tabuleiro)
            print(f"O jogador {vencedor} venceu!")
            return perguntar_reiniciar(conn)

        if tabuleiro[0] < 9:
            posicao2 = random.randint(1, 9)
            while not jogada_valida(posicao2):
                posicao2 = random.randint(1, 9)
            marcar_posicao(posicao2, "O")
            print(f"Máquina 2 jogou na posição {posicao2}.")
            exibir_tabuleiro()
            vencedor = verificar_vitoria()
            if vencedor:
                tabuleiro[11] = -1 if vencedor == "O" else 1
                tabuleiro[12] += 1 if vencedor == "X" else 0
                tabuleiro[14] += 1 if vencedor == "O" else 0
                armazenar_resultado(conn, tabuleiro)
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar(conn)

    print("Empate! Deu velha!")
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    armazenar_resultado(conn, tabuleiro)
    perguntar_reiniciar(conn)

def jogo_humano_vs_campeao(conn):
    reiniciar_tabuleiro(conn)
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
                armazenar_resultado(conn, tabuleiro)
                exibir_tabuleiro()
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar(conn)
        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 9.")
            continue

        if tabuleiro[0] < 9:
            posicao_campeao = melhor_jogada_campeao("O")
            marcar_posicao(posicao_campeao, "O")
            print(f"O Campeão jogou na posição {posicao_campeao}.")
            vencedor = verificar_vitoria()
            if vencedor:
                tabuleiro[11] = -1 if vencedor == "O" else 1
                tabuleiro[12] += 1 if vencedor == "X" else 0
                tabuleiro[14] += 1 if vencedor == "O" else 0
                armazenar_resultado(conn, tabuleiro)
                exibir_tabuleiro()
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar(conn)

    tabuleiro[11] = 0
    tabuleiro[13] += 1
    armazenar_resultado(conn, tabuleiro)
    exibir_tabuleiro()
    print("Empate! Deu velha!")
    perguntar_reiniciar(conn)

def jogo_campeao_vs_campeao(conn):
    reiniciar_tabuleiro(conn)
    while tabuleiro[0] < 9:
        posicao_campeao1 = melhor_jogada_campeao("X")
        marcar_posicao(posicao_campeao1, "X")
        print(f"Campeão 1 jogou na posição {posicao_campeao1}.")
        exibir_tabuleiro()
        vencedor = verificar_vitoria()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1
            tabuleiro[12] += 1 if vencedor == "X" else 0
            tabuleiro[14] += 1 if vencedor == "O" else 0
            armazenar_resultado(conn, tabuleiro)
            print(f"O jogador {vencedor} venceu!")
            return perguntar_reiniciar(conn)

        if tabuleiro[0] < 9:
            posicao_campeao2 = melhor_jogada_campeao("O")
            marcar_posicao(posicao_campeao2, "O")
            print(f"Campeão 2 jogou na posição {posicao_campeao2}.")
            exibir_tabuleiro()
            vencedor = verificar_vitoria()
            if vencedor:
                tabuleiro[11] = -1 if vencedor == "O" else 1
                tabuleiro[12] += 1 if vencedor == "X" else 0
                tabuleiro[14] += 1 if vencedor == "O" else 0
                armazenar_resultado(conn, tabuleiro)
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar(conn)

    print("Empate! Deu velha!")
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    armazenar_resultado(conn, tabuleiro)
    perguntar_reiniciar(conn)

def jogo_campeao_vs_maquina(conn):
    reiniciar_tabuleiro(conn)
    while tabuleiro[0] < 9:
        posicao_campeao = melhor_jogada_campeao("X")
        marcar_posicao(posicao_campeao, "X")
        print(f"O Campeão jogou na posição {posicao_campeao}.")
        exibir_tabuleiro()
        vencedor = verificar_vitoria()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1
            tabuleiro[12] += 1 if vencedor == "X" else 0
            tabuleiro[14] += 1 if vencedor == "O" else 0
            armazenar_resultado(conn, tabuleiro)
            print(f"O jogador {vencedor} venceu!")
            return perguntar_reiniciar(conn)

        if tabuleiro[0] < 9:
            posicao_maquina = random.randint(1, 9)
            while not jogada_valida(posicao_maquina):
                posicao_maquina = random.randint(1, 9)
            marcar_posicao(posicao_maquina, "O")
            print(f"A máquina jogou na posição {posicao_maquina}.")
            exibir_tabuleiro()
            vencedor = verificar_vitoria()
            if vencedor:
                tabuleiro[11] = -1 if vencedor == "O" else 1
                tabuleiro[12] += 1 if vencedor == "X" else 0
                tabuleiro[14] += 1 if vencedor == "O" else 0
                armazenar_resultado(conn, tabuleiro)
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar(conn)

    print("Empate! Deu velha!")
    tabuleiro[11] = 0
    tabuleiro[13] += 1
    armazenar_resultado(conn, tabuleiro)
    perguntar_reiniciar(conn)

def perguntar_reiniciar(conn):
    print("\nDeseja jogar novamente ou encerrar o jogo?")
    print("1 - Jogar novamente")
    print("2 - Encerrar")
    escolha = input("Escolha uma opção (1 ou 2): ")
    if escolha == "1":
        iniciar_jogo(conn)
    elif escolha == "2":
        print("Jogo encerrado. Obrigado por jogar!")
        conn.close()
        exit()
    else:
        print("Opção inválida. Encerrando o jogo.")
        conn.close()
        exit()

# Atualização do menu com as novas opções
def iniciar_jogo(conn):
    print("\nEscolha uma opção:")
    print("1 - Jogador Humano vs Jogador Aleatório")
    print("2 - Jogador Humano vs Jogador Campeão")
    print("3 - Jogador Aleatório vs Jogador Aleatório")
    print("4 - Jogador Campeão vs Jogador Campeão")
    print("5 - Jogador Campeão vs Jogador Aleatório")
    print("6 - Exibir Resultados")
    print("7 - Limpar Resultados")

    escolha = input("Digite 1, 2, 3, 4, 5, 6 ou 7: ")

    partida_atual, vitorias_j1, empates, vitorias_j2 = obter_estatisticas(conn)
    tabuleiro[10] = partida_atual
    tabuleiro[12] = vitorias_j1
    tabuleiro[13] = empates
    tabuleiro[14] = vitorias_j2

    if escolha == "1":
        jogo_jogador_vs_maquina(conn)
    elif escolha == "2":
        jogo_humano_vs_campeao(conn)
    elif escolha == "3":
        jogo_maquina_vs_maquina(conn)
    elif escolha == "4":
        jogo_campeao_vs_campeao(conn)
    elif escolha == "5":
        jogo_campeao_vs_maquina(conn)
    elif escolha == "6":
        exibir_resultados(conn)
        perguntar_reiniciar(conn)
    elif escolha == "7":
        limpar_tabela(conn)
        perguntar_reiniciar(conn)
    else:
        print("Opção inválida. Encerrando o jogo.")
        conn.close()
        exit()

# Menu principal com reinicialização do jogo
def menu_principal():
    global tabuleiro
    tabuleiro = [0] * 15
    tabuleiro[10] = 0
    conn = init_db()
    while True:
        iniciar_jogo(conn)

# Inicia o jogo
menu_principal()
