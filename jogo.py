import random
import sqlite3

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect('jogo.db')  # Nome do banco de dados alterado
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
        partida_atual = resultado[0] + 1  # Incrementa o número da partida
        vitorias_j1 = resultado[4]
        empates = resultado[5]
        vitorias_j2 = resultado[6]
    else:
        partida_atual = 1  # Começa a partir da primeira partida
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
    tabuleiro = [0] * 15  # 15 posições para armazenar dados adicionais
    tabuleiro[10] = partida_atual  # Define o número da partida
    tabuleiro[12] = vitorias_j1     # Atualiza vitórias do jogador 1
    tabuleiro[13] = empates          # Atualiza empates
    tabuleiro[14] = vitorias_j2      # Atualiza vitórias do jogador 2
    tabuleiro[0] = 0  # Reinicia o contador de jogadas

def verificar_vitoria():
    combinacoes_vitoria = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],  # Linhas
        [1, 4, 7], [2, 5, 8], [3, 6, 9],  # Colunas
        [1, 5, 9], [3, 5, 7]              # Diagonais
    ]
    
    for combinacao in combinacoes_vitoria:
        soma = sum(tabuleiro[pos] for pos in combinacao)
        if soma == 3:   # Jogador 1 vence
            return "X"
        elif soma == -3:  # Jogador 2 vence
            return "O"
    return None  # Nenhum vencedor ainda

def marcar_posicao(posicao, jogador):
    tabuleiro[posicao] = 1 if jogador == "X" else -1  # 1 para X (Jogador 1), -1 para O (Jogador 2)
    tabuleiro[0] += 1  # Incrementa o contador de jogadas

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

def jogo_jogador_vs_maquina(conn):
    reiniciar_tabuleiro(conn)
    while tabuleiro[0] < 9:
        # Exibir o tabuleiro e permitir a jogada do jogador 1 (humano)
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
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar(conn)
        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 9.")
            continue
        
        # Máquina (Jogador 2)
        if tabuleiro[0] < 9:
            posicao_maquina = random.choice([pos for pos in range(1, 10) if jogada_valida(pos)])
            marcar_posicao(posicao_maquina, "O")
            print(f"A máquina jogou na posição {posicao_maquina}.")
            vencedor = verificar_vitoria()
            if vencedor:
                tabuleiro[11] = -1 if vencedor == "O" else 1
                tabuleiro[12] += 1 if vencedor == "X" else 0
                tabuleiro[14] += 1 if vencedor == "O" else 0
                armazenar_resultado(conn, tabuleiro)
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar(conn)

    # Se não houve vencedor, é empate
    tabuleiro[11] = 0  # Empate
    tabuleiro[13] += 1  # Incrementa o número de empates
    armazenar_resultado(conn, tabuleiro)
    print("Empate! Deu velha!")
    perguntar_reiniciar(conn)

def jogo_maquina_vs_maquina(conn):
    reiniciar_tabuleiro()
    while tabuleiro[0] < 9:
        # Máquina 1 joga
        posicao1 = random.choice([pos for pos in range(1, 10) if jogada_valida(pos)])
        marcar_posicao(posicao1, "X")
        print(f"Máquina 1 jogou na posição {posicao1}.")
        exibir_tabuleiro()
        vencedor = verificar_vitoria()
        if vencedor:
            tabuleiro[11] = 1 if vencedor == "X" else -1  # Define o resultado da partida
            tabuleiro[12] += 1 if vencedor == "X" else 0  # Incrementa vitórias do Jogador 1
            tabuleiro[14] += 1 if vencedor == "O" else 0  # Incrementa vitórias do Jogador 2
            armazenar_resultado(conn, tabuleiro)  # Armazena o resultado no banco de dados
            print(f"O jogador {vencedor} venceu!")
            return perguntar_reiniciar(conn)
        
        # Máquina 2 joga se ainda houver jogadas
        if tabuleiro[0] < 9:
            posicao2 = random.choice([pos for pos in range(1, 10) if jogada_valida(pos)])
            marcar_posicao(posicao2, "O")
            print(f"Máquina 2 jogou na posição {posicao2}.")
            exibir_tabuleiro()
            vencedor = verificar_vitoria()
            if vencedor:
                tabuleiro[11] = -1 if vencedor == "O" else 1  # Define o resultado da partida
                tabuleiro[12] += 1 if vencedor == "X" else 0  # Incrementa vitórias do Jogador 1
                tabuleiro[14] += 1 if vencedor == "O" else 0  # Incrementa vitórias do Jogador 2
                armazenar_resultado(conn, tabuleiro)  # Armazena o resultado no banco de dados
                print(f"O jogador {vencedor} venceu!")
                return perguntar_reiniciar(conn)

    print("Empate! Deu velha!")
    tabuleiro[11] = 0  # Empate
    tabuleiro[13] += 1  # Incrementa o número de empates
    armazenar_resultado(conn, tabuleiro)  # Armazena o resultado no banco de dados
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
        conn.close()  # Fecha a conexão do banco de dados
        exit()
    else:
        print("Opção inválida. Encerrando o jogo.")
        conn.close()  # Fecha a conexão do banco de dados
        exit()

def iniciar_jogo(conn):
    print("\nEscolha uma opção:")
    print("1 - Jogador vs Máquina")
    print("2 - Máquina vs Máquina")
    print("3 - Exibir Resultados")
    print("4 - Limpar Resultados")  # Nova opção para limpar a tabela

    escolha = input("Digite 1, 2, 3 ou 4: ")

    # Obtém estatísticas e define o número da partida e as estatísticas
    partida_atual, vitorias_j1, empates, vitorias_j2 = obter_estatisticas(conn)
    tabuleiro[10] = partida_atual  # Atualiza o número da partida
    tabuleiro[12] = vitorias_j1     # Atualiza vitórias do jogador 1
    tabuleiro[13] = empates          # Atualiza empates
    tabuleiro[14] = vitorias_j2      # Atualiza vitórias do jogador 2

    if escolha == "1":
        jogo_jogador_vs_maquina(conn)
    elif escolha == "2":
        jogo_maquina_vs_maquina(conn)
    elif escolha == "3":
        exibir_resultados(conn)
        perguntar_reiniciar(conn)  # Permite ao usuário decidir se quer jogar novamente ou encerrar
    elif escolha == "4":
        limpar_tabela(conn)  # Chama a função para limpar a tabela
        perguntar_reiniciar(conn)  # Pergunta ao usuário se deseja continuar
    else:
        print("Opção inválida. Encerrando o jogo.")
        conn.close()  # Fecha a conexão do banco de dados
        exit()

def menu_principal():
    global tabuleiro
    tabuleiro = [0] * 15  # Inicializa o tabuleiro
    tabuleiro[10] = 0  # Inicializa o número da partida
    conn = init_db()
    while True:
        iniciar_jogo(conn)

## Inicia o jogo
menu_principal()