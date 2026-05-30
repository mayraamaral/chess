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

# ==========================================
# 2. Estruturas de Dados (Tabuleiro, Peças)
# ==========================================


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
    
    # O loop principal do jogo será implementado aqui


if __name__ == "__main__":
    main()
