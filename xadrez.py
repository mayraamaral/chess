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
# ==========================================
# 5. Função Principal
# ==========================================
def main():
    print("Iniciando o Jogo de Xadrez...")
    
    print("Peças Brancas:", " ".join(PECAS["brancas"].values()))
    print("Peças Pretas: ", " ".join(PECAS["pretas"].values()))
    
    # Testando as funções auxiliares
    print("Cor de ♔:", obter_cor_peca("♔"))
    print("Tipo de ♟:", obter_tipo_peca("♟"))
    print("Cor do Vazio:", obter_cor_peca(VAZIO))
    
    print("\nTabuleiro Inicial:")
    tabuleiro = criar_tabuleiro()
    imprimir_tabuleiro(tabuleiro)
    
    print("\nTestes de conversão de coordenadas:")
    print("e2 ->", coordenada_para_indice("e2"))
    print("a1 ->", coordenada_para_indice("a1"))
    print("h8 ->", coordenada_para_indice("h8"))
    print("z9 (inválido) ->", coordenada_para_indice("z9"))
    print("E2 (maiúscula) ->", coordenada_para_indice("E2"))
    
    # O loop principal do jogo será implementado aqui


if __name__ == "__main__":
    main()
