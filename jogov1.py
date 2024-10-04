import random

# Inicializa o tabuleiro com 10 posições: 0 para contador de jogadas, 1-9 para posições do tabuleiro
tabuleiro = [" "] * 10  # Inicia com espaços vazios para melhor visualização

def exibir_tabuleiro():
    """Exibe o tabuleiro na tela."""
    print("\n")
    print(f" {tabuleiro[1]} | {tabuleiro[2]} | {tabuleiro[3]} ")
    print("---+---+---")
    print(f" {tabuleiro[4]} | {tabuleiro[5]} | {tabuleiro[6]} ")
    print("---+---+---")
    print(f" {tabuleiro[7]} | {tabuleiro[8]} | {tabuleiro[9]} ")
    print("\n")

def jogada_valida(posicao):
    """Verifica se a jogada é válida (posição livre e dentro do range)."""
    return 1 <= posicao <= 9 and tabuleiro[posicao] == " "

def marcar_posicao(posicao, jogador):
    """Marca a posição no tabuleiro para o jogador."""
    tabuleiro[posicao] = jogador
    tabuleiro[0] = int(tabuleiro[0]) + 1  # Incrementa o contador de jogadas

def verificar_vitoria(jogador):
    """Verifica se o jogador venceu."""
    combinacoes_vitoria = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],  # Linhas
        [1, 4, 7], [2, 5, 8], [3, 6, 9],  # Colunas
        [1, 5, 9], [3, 5, 7]              # Diagonais
    ]
    for combinacao in combinacoes_vitoria:
        if all(tabuleiro[pos] == jogador for pos in combinacao):
            return True
    return False

def reiniciar_tabuleiro():
    """Reinicia o tabuleiro para um novo jogo."""
    global tabuleiro
    tabuleiro = [" "] * 10
    tabuleiro[0] = 0  # Reinicia o contador de jogadas

def jogo_jogador_vs_maquina():
    """Jogo entre jogador e máquina."""
    reiniciar_tabuleiro()
    while tabuleiro[0] < 9:
        exibir_tabuleiro()
        # Jogador 1 (humano)
        try:
            posicao = int(input("Escolha uma posição (1-9) para jogar: "))
            if not jogada_valida(posicao):
                print("Posição inválida! Tente novamente.")
                continue
            marcar_posicao(posicao, "X")
            if verificar_vitoria("X"):
                exibir_tabuleiro()
                print("Você venceu!")
                return perguntar_reiniciar()
        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 9.")
            continue
        
        # Máquina (Jogador 2)
        if tabuleiro[0] < 9:  # Verifica se ainda há jogadas
            posicao_maquina = random.choice([pos for pos in range(1, 10) if jogada_valida(pos)])
            marcar_posicao(posicao_maquina, "O")
            print(f"A máquina jogou na posição {posicao_maquina}.")
            if verificar_vitoria("O"):
                exibir_tabuleiro()
                print("A máquina venceu!")
                return perguntar_reiniciar()

    exibir_tabuleiro()
    print("Empate! Deu velha!")
    perguntar_reiniciar()

def jogo_maquina_vs_maquina():
    """Jogo entre duas máquinas jogando aleatoriamente."""
    reiniciar_tabuleiro()
    while tabuleiro[0] < 9:
        # Máquina 1 joga
        posicao1 = random.choice([pos for pos in range(1, 10) if jogada_valida(pos)])
        marcar_posicao(posicao1, "X")
        print(f"Máquina 1 jogou na posição {posicao1}.")
        exibir_tabuleiro()
        if verificar_vitoria("X"):
            print("Máquina 1 venceu!")
            return perguntar_reiniciar()
        
        # Máquina 2 joga se ainda houver jogadas
        if tabuleiro[0] < 9:
            posicao2 = random.choice([pos for pos in range(1, 10) if jogada_valida(pos)])
            marcar_posicao(posicao2, "O")
            print(f"Máquina 2 jogou na posição {posicao2}.")
            exibir_tabuleiro()
            if verificar_vitoria("O"):
                print("Máquina 2 venceu!")
                return perguntar_reiniciar()
    
    print("Empate! Deu velha!")
    perguntar_reiniciar()

def perguntar_reiniciar():
    """Pergunta ao jogador se deseja jogar novamente ou encerrar o jogo."""
    print("\nDeseja jogar novamente ou encerrar o jogo?")
    print("1 - Jogar novamente")
    print("2 - Encerrar")
    escolha = input("Escolha uma opção (1 ou 2): ")
    if escolha == "1":
        iniciar_jogo()
    elif escolha == "2":
        print("Jogo encerrado. Obrigado por jogar!")
        exit()
    else:
        print("Opção inválida. Encerrando o jogo.")
        exit()

def iniciar_jogo():
    """Inicia o jogo com base na escolha do usuário."""
    print("\nEscolha uma opção:")
    print("1 - Jogador vs Máquina")
    print("2 - Máquina vs Máquina")
    
    escolha = input("Digite 1 ou 2: ")
    if escolha == "1":
        jogo_jogador_vs_maquina()
    elif escolha == "2":
        jogo_maquina_vs_maquina()
    else:
        print("Opção inválida. Encerrando o jogo.")
        exit()

def menu_principal():
    """Menu principal do jogo."""
    print("Bem-vindo ao Jogo da Velha!")
    iniciar_jogo()

# Inicia o jogo
menu_principal()