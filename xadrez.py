"""
Disciplina: Programação de Computadores
Professor: Leonardo Angelo Virginio De Souto
Integrantes: Mayra Amaral, Marlon Andrade, Pietro Toledo e Rodrigo Gadelha
Tema: Jogo de Xadrez em Python (Terminal)
Descrição do Jogo:
Um jogo de xadrez completo desenvolvido em Python puro, sem bibliotecas externas.
O jogo será jogado via terminal, com o tabuleiro sendo impresso na tela.
"""

# ==========================================
# 1. Constantes e Configurações Iniciais
# ==========================================


PECAS = {
    "brancas": {
        "rei": "♔",
        "dama": "♕",
        "torre": "♖",
        "bispo": "♗",
        "cavalo": "♘",
        "peao": "♙"
    },
    "pretas": {
        "rei": "♚",
        "dama": "♛",
        "torre": "♜",
        "bispo": "♝",
        "cavalo": "♞",
        "peao": "♟"
    }
}

VAZIO = "."

COLUNAS_VALIDAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
LINHAS_VALIDAS = ['1', '2', '3', '4', '5', '6', '7', '8']

# ==========================================
# 2. Estruturas de Dados (Tabuleiro, Peças)
# ==========================================

def criar_tabuleiro():
    tabuleiro = []
    
    # Linha 0: Peças maiores pretas
    linha_0 = [
        PECAS["pretas"]["torre"], PECAS["pretas"]["cavalo"], PECAS["pretas"]["bispo"], 
        PECAS["pretas"]["dama"], PECAS["pretas"]["rei"], 
        PECAS["pretas"]["bispo"], PECAS["pretas"]["cavalo"], PECAS["pretas"]["torre"]
    ]
    tabuleiro.append(linha_0)
    
    # Linha 1: Peões pretos
    linha_1 = [PECAS["pretas"]["peao"]] * 8
    tabuleiro.append(linha_1)
    
    # Linhas 2 a 5: Vazias
    for _ in range(4):
        tabuleiro.append([VAZIO] * 8)
        
    # Linha 6: Peões brancos
    linha_6 = [PECAS["brancas"]["peao"]] * 8
    tabuleiro.append(linha_6)
    
    # Linha 7: Peças maiores brancas
    linha_7 = [
        PECAS["brancas"]["torre"], PECAS["brancas"]["cavalo"], PECAS["brancas"]["bispo"], 
        PECAS["brancas"]["dama"], PECAS["brancas"]["rei"], 
        PECAS["brancas"]["bispo"], PECAS["brancas"]["cavalo"], PECAS["brancas"]["torre"]
    ]
    tabuleiro.append(linha_7)
    
    return tabuleiro

# ==========================================
# 3. Funções de Lógica do Jogo (Movimentos)
# ==========================================

def obter_cor_peca(peca):
    if peca == VAZIO or not peca:
        return None
    if peca in PECAS["brancas"].values():
        return "branco"
    if peca in PECAS["pretas"].values():
        return "preto"
    return None

def obter_tipo_peca(peca):
    if peca == VAZIO or not peca:
        return None
    for tipo, simbolo in PECAS["brancas"].items():
        if simbolo == peca:
            return tipo
    for tipo, simbolo in PECAS["pretas"].items():
        if simbolo == peca:
            return tipo
    return None

def movimento_peao_valido(tabuleiro, origem, destino, cor):
    # Verifica se o movimento do peão é válido de acordo com as regras básicas do xadrez
    # Os peões brancos se movem para cima no tabuleiro (linha menor) e os pretos se movem para baixo (linha maior).
    linha_orig, col_orig = origem
    linha_dest, col_dest = destino

    # O peão não pode ficar parado na mesma casa, isso não é um movimento válido.
    if origem == destino:
        return False

    linha_diff = linha_dest - linha_orig
    coluna_diff = col_dest - col_orig
    destino_peca = tabuleiro[linha_dest][col_dest]

    if cor == "branco":
        # Peões brancos avançam na direção de índices de linha menores
        direcao = -1
        linha_inicial = 6
        cor_oponente = "preto"
    else:
        # Peões pretos avançam na direção de índices de linha maiores
        direcao = 1
        linha_inicial = 1
        cor_oponente = "branco"

    # Movimento simples para frente: uma casa adiante em mesma coluna, somente se estiver desocupada.
    if coluna_diff == 0 and linha_diff == direcao:
        return destino_peca == VAZIO

    # Avanço duplo: dois espaços à frente apenas da posição inicial e apenas se ambos os espaços estiverem livres.
    if coluna_diff == 0 and linha_diff == 2 * direcao:
        if linha_orig != linha_inicial:
            return False
        if destino_peca != VAZIO:
            return False
        linha_intermediaria = linha_orig + direcao
        return tabuleiro[linha_intermediaria][col_orig] == VAZIO

    # Captura diagonal: o peão só captura quando avança uma casa na diagonal e há peça adversária na casa de destino.
    if abs(coluna_diff) == 1 and linha_diff == direcao:
        return destino_peca != VAZIO and obter_cor_peca(destino_peca) == cor_oponente

    # Todo outro movimento, inclusive movimento lateral, para trás ou captura para frente, é inválido.
    return False

def peca_pertence_ao_turno(peca, turno_atual):
    # Verifica se a peça pertence ao jogador do turno atual
    if peca == VAZIO or not peca:
        return False
    
    cor_peca = obter_cor_peca(peca)
    
    if turno_atual == "branco":
        return cor_peca == "branco"
    elif turno_atual == "preto":
        return cor_peca == "preto"
    
    return False

def alternar_turno(turno_atual):
    # Alterna o turno entre branco e preto
    if turno_atual == "branco":
        return "preto"
    else:
        return "branco"

# ==========================================
# 4. Funções de Interface (Impressão no Terminal)
# ==========================================

def imprimir_tabuleiro(tabuleiro):
    print("  " + " ".join(COLUNAS_VALIDAS))
    for i, linha in enumerate(tabuleiro):
        numero_linha = LINHAS_VALIDAS[7 - i]
        print(f"{numero_linha} " + " ".join(linha))

def coordenada_para_indice(coordenada):
    if not isinstance(coordenada, str) or len(coordenada) != 2:
        return None
    
    coordenada = coordenada.lower()
    coluna_str = coordenada[0]
    linha_str = coordenada[1]
    
    # Se o que foi digitado não estiver nas listas, é inválido
    if coluna_str not in COLUNAS_VALIDAS or linha_str not in LINHAS_VALIDAS:
        return None
        
    # O index() nos diz a posição da letra na lista (a=0, b=1, etc)
    coluna = COLUNAS_VALIDAS.index(coluna_str)
    linha = 7 - LINHAS_VALIDAS.index(linha_str)
    
    return linha, coluna

def validar_formato_jogada(entrada):
    partes = entrada.split()
    if len(partes) != 2:
        return False
        
    origem = partes[0]
    destino = partes[1]
    
    # Se qualquer uma das coordenadas for None (inválida), rejeita a jogada
    if coordenada_para_indice(origem) is None or coordenada_para_indice(destino) is None:
        return False
        
    return True

def ler_jogada():
    while True:
        # Recebe a entrada do usuário e remove espaços
        entrada = input("Digite sua jogada (ex: e2 e4) ou 'sair': ").strip().lower()
        
        if entrada == "sair":
            return "sair"
            
        if validar_formato_jogada(entrada):
            origem, destino = entrada.split()
            return origem, destino
        else:
            print("Erro: Formato inválido! Use coordenadas entre a1 e h8, como 'e2 e4'.")

# ==========================================
# 5. Função Principal
# ==========================================
def main():
    print("Iniciando o Jogo de Xadrez...")
    print("Peças Brancas:", " ".join(PECAS["brancas"].values()))
    print("Peças Pretas: ", " ".join(PECAS["pretas"].values()))
    
    tabuleiro = criar_tabuleiro()
    turno_atual = "branco"  # Brancas começam
    
    print("\n" + "="*40)
    print("Tabuleiro Inicial:")
    print("="*40)
    imprimir_tabuleiro(tabuleiro)
    
    # Loop principal do jogo
    while True:
        print("\n" + "-"*40)
        
        # Exibir turno atual
        cor_turno = "BRANCAS" if turno_atual == "branco" else "PRETAS"
        print(f"Turno: {cor_turno}")
        print("-"*40)
        
        # Ler jogada do jogador
        jogada = ler_jogada()
        
        if jogada == "sair":
            print("Encerrando o jogo...")
            break
        
        origem, destino = jogada
        indice_origem = coordenada_para_indice(origem)
        indice_destino = coordenada_para_indice(destino)
        
        # Obter a peça na posição de origem
        linha_orig, col_orig = indice_origem
        peca = tabuleiro[linha_orig][col_orig]
        
        # Validar se a peça pertence ao turno atual
        if not peca_pertence_ao_turno(peca, turno_atual):
            print(f"Erro: Você não pode mover uma peça do adversário ou uma posição vazia!")
            print("Tentando novamente no mesmo turno...\n")
            continue

        tipo_peca = obter_tipo_peca(peca)

        # Validar movimento do peão quando a peça for um peão
        if tipo_peca == "peao":
            if not movimento_peao_valido(tabuleiro, indice_origem, indice_destino, turno_atual):
                print("Erro: Movimento de peão inválido!")
                print("Tentando novamente no mesmo turno...\n")
                continue

        # Se chegou aqui, a jogada é válida (no contexto atual)
        # Realizar o movimento
        linha_dest, col_dest = indice_destino
        tabuleiro[linha_dest][col_dest] = peca
        tabuleiro[linha_orig][col_orig] = VAZIO
        
        print(f"Jogada executada: {origem} -> {destino}")
        print("Tabuleiro após o movimento:")
        imprimir_tabuleiro(tabuleiro)
        
        # Alternar turno apenas após jogada válida
        turno_atual = alternar_turno(turno_atual)


if __name__ == "__main__":
    main()
