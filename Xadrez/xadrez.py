# =============================================================
#  XADREZ - Jogo completo para terminal
#  Sem bibliotecas externas
# =============================================================

# ---------- Constantes (str) ----------
VAZIO = '.'
BRANCO = 'branco'
PRETO = 'preto'

# Valor das peças em float (para pontuação de material)
VALOR_PECA = {
    'P': 1.0, 'N': 3.0, 'B': 3.5,
    'R': 5.0, 'Q': 9.0, 'K': 0.0
}

# Símbolos Unicode para exibição
SIMBOLOS = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
    '.': '·'
}


# =============================================================
#  1. CRIAR E EXIBIR TABULEIRO
# =============================================================

def criar_tabuleiro() -> list:
    """
    Retorna lista de listas 8x8 com peças na posição inicial.
    Peças brancas: letras maiúsculas (K Q R B N P)
    Peças pretas:  letras minúsculas (k q r b n p)
    """
    tabuleiro = []

    fileira_pretas = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
    fileira_brancas = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

    tabuleiro.append(fileira_pretas)       # linha 0: peças pretas
    tabuleiro.append(['p'] * 8)            # linha 1: peões pretos
    for _ in range(4):                     # linhas 2-5: vazias
        tabuleiro.append([VAZIO] * 8)
    tabuleiro.append(['P'] * 8)            # linha 6: peões brancos
    tabuleiro.append(fileira_brancas)      # linha 7: peças brancas

    return tabuleiro


def exibir_tabuleiro(tabuleiro: list, capturadas_brancas: list, capturadas_pretas: list) -> None:
    """
    Imprime o tabuleiro com coordenadas, peças capturadas e pontuação.
    Demonstra: f-strings, for, .join(), .upper()
    """
    colunas = '    a  b  c  d  e  f  g  h'
    separador = '   +--+--+--+--+--+--+--+--+'

    print()
    print(colunas)
    print(separador)

    for i, linha in enumerate(tabuleiro):
        numero = 8 - i  # int: converte índice de lista em número de rank
        celulas = '|'.join(SIMBOLOS[peca] for peca in linha)
        print(f' {numero} |{celulas}| {numero}')
        print(separador)

    print(colunas)

    # Exibe peças capturadas com pontuação float
    pontos_b = sum(VALOR_PECA.get(p.upper(), 0.0) for p in capturadas_brancas)
    pontos_p = sum(VALOR_PECA.get(p.upper(), 0.0) for p in capturadas_pretas)

    caps_b = ' '.join(SIMBOLOS[p] for p in capturadas_brancas) if capturadas_brancas else '-'
    caps_p = ' '.join(SIMBOLOS[p] for p in capturadas_pretas)  if capturadas_pretas  else '-'

    print(f'\n  Brancas capturadas: {caps_b}  ({pontos_b:.1f} pts)')
    print(f'  Pretas capturadas:  {caps_p}  ({pontos_p:.1f} pts)')
    print()


# =============================================================
#  2. CONVERSÃO E VALIDAÇÃO DE ENTRADA
# =============================================================

def converter_posicao(pos: str) -> tuple:
    """
    Converte notação algébrica ('e4') em (linha, coluna) inteiros.
    Demonstra: fatiamento de string, int(), .lower(), .strip()
    """
    pos = pos.strip().lower()           # .strip() e .lower()
    coluna_letra = pos[0]               # fatiamento: pega a letra
    linha_numero = pos[1]               # fatiamento: pega o dígito

    colunas = 'abcdefgh'
    col = colunas.index(coluna_letra)   # busca em string
    lin = 8 - int(linha_numero)         # int(): converte str → int

    return lin, col                     # retorna tupla


def validar_entrada(entrada: str) -> bool:
    """
    Valida se a string digitada é um lance válido (ex: 'e2 e4').
    Demonstra: .split(), len(), and, or, not, in, condicionais
    """
    partes = entrada.strip().split()    # .split() → lista de partes

    if len(partes) != 2:                # len() de lista
        return False

    colunas_validas = 'abcdefgh'

    for pos in partes:
        valida = (
            len(pos) == 2
            and pos[0] in colunas_validas           # in em string
            and pos[1].isdigit()
            and 1 <= int(pos[1]) <= 8               # int() para comparar
        )
        if not valida:                              # not
            return False

    origem = partes[0]
    destino = partes[1]

    if origem == destino:               # não pode mover para a mesma casa
        return False

    return True


# =============================================================
#  3. VALIDAÇÕES DE MOVIMENTO POR PEÇA
# =============================================================

def caminho_livre(tabuleiro: list, lo: int, co: int, ld: int, cd: int) -> bool:
    """
    Verifica se não há peças entre origem e destino (para torre, bispo, rainha).
    Demonstra: while, int, operadores lógicos
    """
    dl = 0 if ld == lo else (1 if ld > lo else -1)   # int: direção linha
    dc = 0 if cd == co else (1 if cd > co else -1)   # int: direção coluna

    lin, col = lo + dl, co + dc

    while lin != ld or col != cd:
        if tabuleiro[lin][col] != VAZIO:
            return False
        lin += dl
        col += dc

    return True


def destino_valido(tabuleiro: list, ld: int, cd: int, branca: bool) -> bool:
    """
    Verifica se o destino está vazio ou tem peça adversária.
    Demonstra: bool, .isupper(), condicionais
    """
    peca_destino = tabuleiro[ld][cd]

    if peca_destino == VAZIO:
        return True

    # Não pode capturar peça da mesma cor
    destino_branca = peca_destino.isupper()   # bool

    return branca != destino_branca           # True se cores diferentes


def validar_peao(tabuleiro: list, lo: int, co: int, ld: int, cd: int, branca: bool) -> bool:
    """Valida movimento de peão. Demonstra: int, bool, condicionais."""
    direcao = -1 if branca else 1             # int: -1 sobe, +1 desce
    linha_inicial = 6 if branca else 1        # int: linha de início

    # Avanço simples
    if cd == co and ld == lo + direcao and tabuleiro[ld][cd] == VAZIO:
        return True

    # Avanço duplo na posição inicial
    if (cd == co
            and lo == linha_inicial
            and ld == lo + 2 * direcao
            and tabuleiro[lo + direcao][co] == VAZIO
            and tabuleiro[ld][cd] == VAZIO):
        return True

    # Captura diagonal
    if (abs(cd - co) == 1
            and ld == lo + direcao
            and tabuleiro[ld][cd] != VAZIO
            and destino_valido(tabuleiro, ld, cd, branca)):
        return True

    return False


def validar_torre(tabuleiro: list, lo: int, co: int, ld: int, cd: int, branca: bool) -> bool:
    """Valida movimento de torre (linha ou coluna reta)."""
    if lo != ld and co != cd:                 # deve ser linha ou coluna
        return False
    if not caminho_livre(tabuleiro, lo, co, ld, cd):
        return False
    return destino_valido(tabuleiro, ld, cd, branca)


def validar_bispo(tabuleiro: list, lo: int, co: int, ld: int, cd: int, branca: bool) -> bool:
    """Valida movimento de bispo (diagonal)."""
    if abs(ld - lo) != abs(cd - co):          # deve ser diagonal
        return False
    if not caminho_livre(tabuleiro, lo, co, ld, cd):
        return False
    return destino_valido(tabuleiro, ld, cd, branca)


def validar_cavalo(tabuleiro: list, lo: int, co: int, ld: int, cd: int, branca: bool) -> bool:
    """Valida movimento de cavalo (L). Cavalo pula peças."""
    dl = abs(ld - lo)                         # int: diferença de linhas
    dc = abs(cd - co)                         # int: diferença de colunas
    movimento_l = (dl == 2 and dc == 1) or (dl == 1 and dc == 2)
    return movimento_l and destino_valido(tabuleiro, ld, cd, branca)


def validar_rainha(tabuleiro: list, lo: int, co: int, ld: int, cd: int, branca: bool) -> bool:
    """Rainha = torre + bispo."""
    reta = (lo == ld or co == cd)
    diagonal = (abs(ld - lo) == abs(cd - co))
    if not (reta or diagonal):
        return False
    if not caminho_livre(tabuleiro, lo, co, ld, cd):
        return False
    return destino_valido(tabuleiro, ld, cd, branca)


def validar_rei(tabuleiro: list, lo: int, co: int, ld: int, cd: int, branca: bool) -> bool:
    """Rei move uma casa em qualquer direção."""
    dl = abs(ld - lo)
    dc = abs(cd - co)
    if dl > 1 or dc > 1:
        return False
    return destino_valido(tabuleiro, ld, cd, branca)


# =============================================================
#  4. MOVER PEÇA
# =============================================================

def mover_peca(tabuleiro: list, origem: tuple, destino: tuple,
               turno: str, capturadas: list) -> bool:
    """
    Tenta executar um lance. Retorna True se válido.
    Demonstra: if/elif/else, .upper(), .isupper(), append(), bool
    """
    lo, co = origem
    ld, cd = destino
    peca = tabuleiro[lo][co]

    # Célula de origem vazia
    if peca == VAZIO:
        print('  ✗ Não há peça nessa posição.')
        return False

    e_branca: bool = peca.isupper()   # bool

    # Verifica se é a peça correta do jogador
    if turno == BRANCO and not e_branca:
        print('  ✗ É a vez das brancas.')
        return False
    elif turno == PRETO and e_branca:
        print('  ✗ É a vez das pretas.')
        return False

    # Despacha validação por tipo (if/elif/else)
    tipo = peca.upper()               # .upper()
    if tipo == 'P':
        ok = validar_peao(tabuleiro, lo, co, ld, cd, e_branca)
    elif tipo == 'R':
        ok = validar_torre(tabuleiro, lo, co, ld, cd, e_branca)
    elif tipo == 'N':
        ok = validar_cavalo(tabuleiro, lo, co, ld, cd, e_branca)
    elif tipo == 'B':
        ok = validar_bispo(tabuleiro, lo, co, ld, cd, e_branca)
    elif tipo == 'Q':
        ok = validar_rainha(tabuleiro, lo, co, ld, cd, e_branca)
    elif tipo == 'K':
        ok = validar_rei(tabuleiro, lo, co, ld, cd, e_branca)
    else:
        ok = False

    if not ok:
        print('  ✗ Movimento inválido para essa peça.')
        return False

    # Captura peça adversária
    peca_destino = tabuleiro[ld][cd]
    if peca_destino != VAZIO:
        capturadas.append(peca_destino)    # append() à lista de capturadas

    # Executa o movimento
    tabuleiro[ld][cd] = peca
    tabuleiro[lo][co] = VAZIO

    # Promoção de peão
    if tipo == 'P' and (ld == 0 or ld == 7):
        tabuleiro[ld][cd] = 'Q' if e_branca else 'q'
        print('  ★ Peão promovido a Rainha!')

    return True


# =============================================================
#  5. VERIFICAR XEQUE
# =============================================================

def encontrar_rei(tabuleiro: list, branca: bool) -> tuple:
    """Retorna posição do rei. Demonstra: for com range, in."""
    rei = 'K' if branca else 'k'
    for lin in range(8):               # for com range
        for col in range(8):
            if tabuleiro[lin][col] == rei:
                return lin, col
    return -1, -1


def verificar_xeque(tabuleiro: list, turno: str) -> bool:
    """
    Verifica se o rei do jogador atual está em xeque.
    Demonstra: for com range, operadores lógicos, in
    """
    branca = (turno == BRANCO)         # bool
    lin_rei, col_rei = encontrar_rei(tabuleiro, branca)

    if lin_rei == -1:
        return False

    # Percorre todas as peças adversárias
    for lin in range(8):               # for com range
        for col in range(8):
            peca = tabuleiro[lin][col]
            if peca == VAZIO:
                continue

            adversaria = (branca and not peca.isupper()) or (not branca and peca.isupper())

            if not adversaria:
                continue

            tipo = peca.upper()
            origem = (lin, col)
            destino = (lin_rei, col_rei)

            # Verifica se peça adversária pode atacar o rei
            if tipo == 'P':
                ameaca = validar_peao(tabuleiro, lin, col, lin_rei, col_rei, not branca)
            elif tipo == 'R':
                ameaca = validar_torre(tabuleiro, lin, col, lin_rei, col_rei, not branca)
            elif tipo == 'N':
                ameaca = validar_cavalo(tabuleiro, lin, col, lin_rei, col_rei, not branca)
            elif tipo == 'B':
                ameaca = validar_bispo(tabuleiro, lin, col, lin_rei, col_rei, not branca)
            elif tipo == 'Q':
                ameaca = validar_rainha(tabuleiro, lin, col, lin_rei, col_rei, not branca)
            elif tipo == 'K':
                ameaca = validar_rei(tabuleiro, lin, col, lin_rei, col_rei, not branca)
            else:
                ameaca = False

            if ameaca:
                return True

    return False


# =============================================================
#  6. EXIBIR REGRAS
# =============================================================

def exibir_regras() -> None:
    """Exibe regras básicas. Demonstra: f-strings, listas, for."""
    regras = [
        'Cada jogador digita o lance no formato: e2 e4',
        'Letras de coluna: a até h  |  Números de linha: 1 até 8',
        'Peão (P): avança 1 casa (ou 2 na posição inicial), captura na diagonal',
        'Torre (R): move em linha reta (linhas e colunas)',
        'Cavalo (N): move em L, pode pular peças',
        'Bispo (B): move na diagonal',
        'Rainha (Q): combina torre e bispo',
        'Rei (K): move uma casa em qualquer direção',
        'Peão que chega ao fim é promovido a Rainha automaticamente',
        'Digite "sair" durante a partida para encerrar',
    ]

    print('\n' + '=' * 50)
    print('  REGRAS DO JOGO')
    print('=' * 50)
    for i, regra in enumerate(regras, start=1):    # for com enumerate
        print(f'  {i}. {regra}')                   # f-string
    print('=' * 50 + '\n')


# =============================================================
#  7. LOOP DO JOGO
# =============================================================

def jogar() -> None:
    """
    Loop principal da partida.
    Demonstra: while, break, append(), len(), f-strings, listas
    """
    tabuleiro: list = criar_tabuleiro()
    turno: str = BRANCO
    historico: list = []                # lista de lances
    capturadas_brancas: list = []       # peças brancas capturadas
    capturadas_pretas: list = []        # peças pretas capturadas
    jogo_ativo: bool = True

    print('\n  Partida iniciada! Brancas começam.')

    while jogo_ativo:                   # while condicional
        exibir_tabuleiro(tabuleiro, capturadas_brancas, capturadas_pretas)

        jogada_num: int = len(historico) // 2 + 1   # int
        cor_display: str = turno.upper()             # .upper()
        print(f'  Jogada {jogada_num} — Vez das {cor_display}')

        entrada = input('  Lance (ex: e2 e4) ou "sair": ').strip().lower()  # .strip() .lower()

        # Comando para sair
        if entrada == 'sair':
            print('\n  Jogo encerrado pelo jogador.')
            break                       # break encerra o while

        # Comandos especiais
        if entrada == 'historico':
            print('\n  Histórico de lances:')
            for idx, lance in enumerate(historico, start=1):   # for sobre lista
                print(f'    {idx}. {lance}')
            print()
            continue

        # Valida formato da entrada
        if not validar_entrada(entrada):
            print('  ✗ Entrada inválida. Use o formato: e2 e4\n')
            continue

        partes = entrada.split()        # .split() → lista
        origem = converter_posicao(partes[0])
        destino = converter_posicao(partes[1])

        # Lista de capturadas do turno atual
        capturadas_turno = capturadas_brancas if turno == PRETO else capturadas_pretas

        if mover_peca(tabuleiro, origem, destino, turno, capturadas_turno):
            historico.append(entrada)   # append() ao histórico

            # Verifica xeque após o lance
            proximo = PRETO if turno == BRANCO else BRANCO
            if verificar_xeque(tabuleiro, proximo):
                print(f'  ♚ XEQUE! Rei das {proximo.upper()} está em xeque.')

            # Troca de turno
            turno = proximo
        else:
            print()

    # Exibe resumo ao fim da partida
    total: int = len(historico)
    print(f'\n  Total de lances jogados: {total}')
    if historico:                       # in implícito: verifica se lista não vazia
        print(f'  Último lance: {historico[-1]}')


# =============================================================
#  8. MENU PRINCIPAL
# =============================================================

def menu_principal() -> None:
    """
    Menu do jogo com while e break.
    Demonstra: while, if/elif/else, break, input, .strip()
    """
    print('\n' + '=' * 50)
    print('        ♔  XADREZ  ♚')
    print('     Jogo para dois jogadores')
    print('=' * 50)

    while True:                          # loop do menu
        print('\n  1. Nova partida')
        print('  2. Ver regras')
        print('  3. Sair')

        opcao = input('\n  Escolha uma opção: ').strip()   # .strip()

        if opcao == '1':
            jogar()
        elif opcao == '2':
            exibir_regras()
        elif opcao == '3':
            print('\n  Até logo! ♟\n')
            break                        # break sai do while
        else:
            print('  ✗ Opção inválida. Digite 1, 2 ou 3.')


# =============================================================
#  PONTO DE ENTRADA
# =============================================================

if __name__ == '__main__':
    menu_principal()