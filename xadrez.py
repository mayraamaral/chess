# Disciplina: Programação de Computadores
# Professor: Leonardo Angelo Virginio De Souto
# Integrantes: Mayra Amaral, Marlon Andrade, Pietro Toledo e Rodrigo Gadelha
# Tema: Jogo de Xadrez em Python (Terminal)
# Descrição do Jogo:
# Um jogo de xadrez completo desenvolvido em Python puro, sem bibliotecas externas.
# O jogo será jogado via terminal, com o tabuleiro sendo impresso na tela.

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
PLACAR_ARQUIVO = "placar.txt"

COLUNAS_VALIDAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
LINHAS_VALIDAS = ['1', '2', '3', '4', '5', '6', '7', '8']

SIMBOLO_PARA_PECA = {
    simbolo: ("branco" if cor == "brancas" else "preto", tipo)
    for cor, pecas_cor in PECAS.items()
    for tipo, simbolo in pecas_cor.items()
}

LINHA_INICIAL_PRETAS = [
    PECAS["pretas"]["torre"], PECAS["pretas"]["cavalo"], PECAS["pretas"]["bispo"],
    PECAS["pretas"]["dama"], PECAS["pretas"]["rei"],
    PECAS["pretas"]["bispo"], PECAS["pretas"]["cavalo"], PECAS["pretas"]["torre"]
]
LINHA_INICIAL_BRANCAS = [
    PECAS["brancas"]["torre"], PECAS["brancas"]["cavalo"], PECAS["brancas"]["bispo"],
    PECAS["brancas"]["dama"], PECAS["brancas"]["rei"],
    PECAS["brancas"]["bispo"], PECAS["brancas"]["cavalo"], PECAS["brancas"]["torre"]
]


def criar_linha_vazia():
    return [VAZIO] * 8


def descrever_cor(cor):
    if cor == "branco":
        return "brancas"
    if cor == "preto":
        return "pretas"
    return None


def mover_turno(cor):
    return "preto" if cor == "branco" else "branco"

# ==========================================
# 2. Estruturas de Dados (Tabuleiro, Peças)
# ==========================================

def criar_tabuleiro():
    return [
        LINHA_INICIAL_PRETAS.copy(),
        [PECAS["pretas"]["peao"]] * 8,
        *(criar_linha_vazia() for _ in range(4)),
        [PECAS["brancas"]["peao"]] * 8,
        LINHA_INICIAL_BRANCAS.copy(),
    ]

# ==========================================
# 3. Funções de Lógica do Jogo (Movimentos)
# ==========================================

def obter_cor_peca(peca):
    if peca == VAZIO or not peca:
        return None
    dados_peca = SIMBOLO_PARA_PECA.get(peca)
    return None if dados_peca is None else dados_peca[0]

def obter_tipo_peca(peca):
    if peca == VAZIO or not peca:
        return None
    dados_peca = SIMBOLO_PARA_PECA.get(peca)
    return None if dados_peca is None else dados_peca[1]


def encontrar_rei(tabuleiro, cor):
    nome_cor = descrever_cor(cor)
    if nome_cor is None:
        return None

    rei_simbolo = PECAS[nome_cor]["rei"]

    for linha_idx, linha in enumerate(tabuleiro):
        for col_idx, valor in enumerate(linha):
            if valor == rei_simbolo:
                return linha_idx, col_idx

    return None


def obter_cor_oponente(cor):
    if cor not in {"branco", "preto"}:
        return None
    return mover_turno(cor)


def rei_existe(tabuleiro, simbolo_rei):
    for linha in tabuleiro:
        if simbolo_rei in linha:
            return True
    return False


def verificar_fim_de_jogo(tabuleiro):
    branco_existe = rei_existe(tabuleiro, PECAS["brancas"]["rei"])
    preto_existe = rei_existe(tabuleiro, PECAS["pretas"]["rei"])

    if not branco_existe and not preto_existe:
        return {'tipo': 'empate'}
    if not branco_existe:
        return {'tipo': 'vitoria', 'vencedor': 'preto', 'motivo': 'rei_branco_capturado'}
    if not preto_existe:
        return {'tipo': 'vitoria', 'vencedor': 'branco', 'motivo': 'rei_preto_capturado'}

    return None


def obter_status_xeque(tabuleiro):
    return {
        'branco': esta_em_xeque(tabuleiro, 'branco'),
        'preto': esta_em_xeque(tabuleiro, 'preto')
    }


def exibir_avisos_de_xeque(status_anterior, status_atual):
    for cor in ("branco", "preto"):
        if status_atual[cor]:
            print(f"Xeque no rei {cor}!")
        elif status_anterior[cor]:
            print(f"O rei {cor} não está mais em xeque.")


def formatar_vencedor_resultado(vencedor, tipo_finalizacao):
    if vencedor in {"branco", "preto"}:
        return descrever_cor(vencedor)
    if tipo_finalizacao == 'Empate':
        return 'empate'
    return 'sem vencedor'


def salvar_resultado(vencedor, quantidade_jogadas, tipo_finalizacao):
    vencedor_formatado = formatar_vencedor_resultado(vencedor, tipo_finalizacao)
    resultado = (
        f"Vencedor: {vencedor_formatado} | "
        f"Jogadas: {quantidade_jogadas} | "
        f"Finalização: {tipo_finalizacao}"
    )

    try:
        with open(PLACAR_ARQUIVO, 'a', encoding='utf-8') as arquivo:
            arquivo.write(resultado + '\n')
    except OSError as erro:
        print(f"Aviso: não foi possível salvar o resultado em {PLACAR_ARQUIVO}: {erro}")

    return resultado


def carregar_resultados():
    try:
        with open(PLACAR_ARQUIVO, 'r', encoding='utf-8') as arquivo:
            linhas = [linha.strip() for linha in arquivo if linha.strip()]
    except FileNotFoundError:
        return []
    except OSError as erro:
        print(f"Aviso: não foi possível ler o arquivo {PLACAR_ARQUIVO}: {erro}")
        return None

    if not linhas:
        return []

    resultados = []

    for linha in linhas:
        partes = linha.split(' | ')
        if len(partes) != 3:
            resultados.append({
                'vencedor': 'desconhecido',
                'quantidade_jogadas': 'desconhecida',
                'tipo_finalizacao': linha
            })
            continue

        vencedor = partes[0].replace('Vencedor: ', '', 1)
        quantidade_jogadas = partes[1].replace('Jogadas: ', '', 1)
        tipo_finalizacao = partes[2].replace('Finalização: ', '', 1)
        resultados.append({
            'vencedor': vencedor,
            'quantidade_jogadas': quantidade_jogadas,
            'tipo_finalizacao': tipo_finalizacao
        })

    return resultados


def obter_quantidade_jogadas(historico):
    return sum(1 for item in historico if 'origem' in item and 'destino' in item)


def registrar_resultado(historico, resultado):
    historico.append({'resultado': resultado})


def declarar_vencedor(cor_vencedora, motivo, quantidade_jogadas):
    mensagens_por_captura = {
        'rei_preto_capturado': 'Fim de jogo! O rei preto foi capturado.\nVitória das peças brancas.',
        'rei_branco_capturado': 'Fim de jogo! O rei branco foi capturado.\nVitória das peças pretas.',
    }
    mensagem = mensagens_por_captura.get(motivo)

    if mensagem is None:
        mensagem = f"Vitória das peças {descrever_cor(cor_vencedora)}."

    print(mensagem)
    salvar_resultado(cor_vencedora, quantidade_jogadas, 'Rei capturado')
    return mensagem


def finalizar_por_desistencia(turno_atual, quantidade_jogadas):
    vencedor = mover_turno(turno_atual)
    desistente_formatado = descrever_cor(turno_atual)
    vencedor_formatado = formatar_vencedor_resultado(vencedor, 'Desistência')
    mensagem = f'O jogador das peças {desistente_formatado} desistiu.\nVitória das peças {vencedor_formatado}.'
    print(mensagem)
    salvar_resultado(vencedor, quantidade_jogadas, 'Desistência')
    return mensagem


def finalizar_por_empate(quantidade_jogadas):
    mensagem = 'A partida terminou empatada.'
    print(mensagem)
    salvar_resultado(None, quantidade_jogadas, 'Empate')
    return mensagem


def finalizar_por_saida_manual(quantidade_jogadas):
    mensagem = 'A partida foi encerrada manualmente.'
    print(mensagem)
    salvar_resultado(None, quantidade_jogadas, 'Saída manual')
    return mensagem


def movimento_peao_valido(tabuleiro, origem, destino, cor):
    linha_orig, col_orig = origem
    linha_dest, col_dest = destino

    if origem == destino:
        return False

    linha_diff = linha_dest - linha_orig
    coluna_diff = col_dest - col_orig
    destino_peca = tabuleiro[linha_dest][col_dest]

    if cor == "branco":
        direcao = -1
        linha_inicial = 6
        cor_oponente = "preto"
    else:
        direcao = 1
        linha_inicial = 1
        cor_oponente = "branco"

    if coluna_diff == 0 and linha_diff == direcao:
        return destino_peca == VAZIO

    if coluna_diff == 0 and linha_diff == 2 * direcao:
        if linha_orig != linha_inicial:
            return False
        if destino_peca != VAZIO:
            return False
        linha_intermediaria = linha_orig + direcao
        return tabuleiro[linha_intermediaria][col_orig] == VAZIO

    if abs(coluna_diff) == 1 and linha_diff == direcao:
        return destino_peca != VAZIO and obter_cor_peca(destino_peca) == cor_oponente

    return False


def caminho_livre(tabuleiro, origem, destino):
    linha_orig, col_orig = origem
    linha_dest, col_dest = destino

    delta_linha = linha_dest - linha_orig
    delta_col = col_dest - col_orig

    passo_linha = 0 if delta_linha == 0 else (1 if delta_linha > 0 else -1)
    passo_col = 0 if delta_col == 0 else (1 if delta_col > 0 else -1)

    # Caminho deve ser horizontal, vertical ou diagonal
    if passo_linha != 0 and passo_col != 0 and abs(delta_linha) != abs(delta_col):
        return False

    linha = linha_orig + passo_linha
    col = col_orig + passo_col
    while (linha, col) != (linha_dest, col_dest):
        if tabuleiro[linha][col] != VAZIO:
            return False
        linha += passo_linha
        col += passo_col

    return True


def movimento_torre_valido(tabuleiro, origem, destino):
    linha_orig, col_orig = origem
    linha_dest, col_dest = destino

    if origem == destino:
        return False

    if linha_orig != linha_dest and col_orig != col_dest:
        return False

    return caminho_livre(tabuleiro, origem, destino)


def movimento_bispo_valido(tabuleiro, origem, destino):
    linha_orig, col_orig = origem
    linha_dest, col_dest = destino

    if origem == destino:
        return False

    if abs(linha_dest - linha_orig) != abs(col_dest - col_orig):
        return False

    return caminho_livre(tabuleiro, origem, destino)


def movimento_dama_valido(tabuleiro, origem, destino):
    linha_orig, col_orig = origem
    linha_dest, col_dest = destino

    if origem == destino:
        return False

    horizontal = linha_orig == linha_dest
    vertical = col_orig == col_dest
    diagonal = abs(linha_dest - linha_orig) == abs(col_dest - col_orig)

    if not (horizontal or vertical or diagonal):
        return False

    return caminho_livre(tabuleiro, origem, destino)


def movimento_cavalo_valido(tabuleiro, origem, destino):
    linha_orig, col_orig = origem
    linha_dest, col_dest = destino

    if origem == destino:
        return False

    linha_diff = abs(linha_dest - linha_orig)
    col_diff = abs(col_dest - col_orig)

    return (linha_diff == 2 and col_diff == 1) or (linha_diff == 1 and col_diff == 2)


def movimento_rei_valido(tabuleiro, origem, destino):
    linha_orig, col_orig = origem
    linha_dest, col_dest = destino

    if origem == destino:
        return False

    linha_diff = abs(linha_dest - linha_orig)
    col_diff = abs(col_dest - col_orig)

    return linha_diff <= 1 and col_diff <= 1


VALIDADORES_MOVIMENTO = {
    "torre": movimento_torre_valido,
    "bispo": movimento_bispo_valido,
    "dama": movimento_dama_valido,
    "cavalo": movimento_cavalo_valido,
    "rei": movimento_rei_valido,
}


def movimento_por_tipo_valido(tabuleiro, origem, destino, tipo_peca, cor=None):
    if tipo_peca == "peao":
        return movimento_peao_valido(tabuleiro, origem, destino, cor)

    validador = VALIDADORES_MOVIMENTO.get(tipo_peca)
    if validador is None:
        return False

    return validador(tabuleiro, origem, destino)


def peca_ataca_posicao(tabuleiro, origem, destino):
    linha_orig, col_orig = origem
    peca_origem = tabuleiro[linha_orig][col_orig]

    if peca_origem == VAZIO or not peca_origem:
        return False

    cor_peca = obter_cor_peca(peca_origem)
    tipo_peca = obter_tipo_peca(peca_origem)
    return movimento_por_tipo_valido(tabuleiro, origem, destino, tipo_peca, cor_peca)


def esta_em_xeque(tabuleiro, cor):
    posicao_rei = encontrar_rei(tabuleiro, cor)
    cor_oponente = obter_cor_oponente(cor)

    if posicao_rei is None or cor_oponente is None:
        return False

    for linha_idx, linha in enumerate(tabuleiro):
        for col_idx, peca in enumerate(linha):
            if obter_cor_peca(peca) != cor_oponente:
                continue

            if peca_ataca_posicao(tabuleiro, (linha_idx, col_idx), posicao_rei):
                return True

    return False


def movimento_valido(tabuleiro, origem, destino, turno_atual):
    linha_orig, col_orig = origem
    linha_dest, col_dest = destino

    peca_origem = tabuleiro[linha_orig][col_orig]
    if peca_origem == VAZIO or not peca_origem:
        return False

    if not peca_pertence_ao_turno(peca_origem, turno_atual):
        return False

    peca_destino = tabuleiro[linha_dest][col_dest]
    if peca_destino != VAZIO and obter_cor_peca(peca_destino) == obter_cor_peca(peca_origem):
        return False

    tipo_peca = obter_tipo_peca(peca_origem)
    return movimento_por_tipo_valido(tabuleiro, origem, destino, tipo_peca, turno_atual)


def executar_jogada(tabuleiro, origem, destino):
    linha_orig, col_orig = origem
    linha_dest, col_dest = destino

    peca_origem = tabuleiro[linha_orig][col_orig]
    peca_capturada = tabuleiro[linha_dest][col_dest]

    tabuleiro[linha_dest][col_dest] = peca_origem
    tabuleiro[linha_orig][col_orig] = VAZIO

    return peca_capturada if peca_capturada != VAZIO else None


def registrar_jogada(historico, turno, peca, origem, destino, capturada):
    tipo = obter_tipo_peca(peca) or peca
    entrada = {
        'turno': turno,
        'peca': tipo,
        'simbolo': peca,
        'origem': origem,
        'destino': destino,
        'capturada': capturada
    }
    historico.append(entrada)


def exibir_historico(historico):
    if not historico:
        print("Nenhuma jogada registrada nesta partida.")
        return

    print("\nHistórico de jogadas:")
    for i, item in enumerate(historico, start=1):
        if 'resultado' in item:
            print(f"Resultado final: {item['resultado']}")
            continue

        turno = item['turno'].capitalize()
        peca = item['peca'].capitalize() if isinstance(item['peca'], str) else item['peca']
        simbolo = item['simbolo']
        origem = item['origem']
        destino = item['destino']
        cap = item['capturada']

        linha = f"{i}. {turno} - {peca} ({simbolo}): {origem} -> {destino}"
        if cap:
            linha += f" (capturou {cap})"
        print(linha)


def peca_pertence_ao_turno(peca, turno_atual):
    if peca == VAZIO or not peca:
        return False
    return obter_cor_peca(peca) == turno_atual

def alternar_turno(turno_atual):
    return mover_turno(turno_atual)

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
    
    if coluna_str not in COLUNAS_VALIDAS or linha_str not in LINHAS_VALIDAS:
        return None

    coluna = COLUNAS_VALIDAS.index(coluna_str)
    linha = 7 - LINHAS_VALIDAS.index(linha_str)

    return linha, coluna

def validar_formato_jogada(entrada):
    partes = entrada.split()
    if len(partes) != 2:
        return False
        
    origem = partes[0]
    destino = partes[1]
    
    if coordenada_para_indice(origem) is None or coordenada_para_indice(destino) is None:
        return False

    return True

def ler_jogada():
    while True:
        entrada = input("Digite sua jogada (ex: e2 e4), 'desistir', 'empate' ou 'sair': ").strip().lower()

        if entrada in {"sair", "desistir", "empate"}:
            return entrada

        if validar_formato_jogada(entrada):
            origem, destino = entrada.split()
            return origem, destino
        else:
            print("Erro: Formato inválido! Use coordenadas entre a1 e h8, como 'e2 e4', ou digite 'desistir', 'empate' ou 'sair'.")


def exibir_menu():
    # Mostra o menu principal e devolve a ação escolhida.
    while True:
        print("\n" + "="*30)
        print("Menu Principal - Jogo de Xadrez")
        print("="*30)
        print("1. Iniciar partida")
        print("2. Ver regras")
        print("3. Ver placar salvo")
        print("sair. Sair")
        opcao = input("Escolha uma opção (1, 2, 3 ou sair): ").strip().lower()

        if opcao == "1":
            return "iniciar_partida"
        elif opcao == "2":
            return "ver_regras"
        elif opcao == "3":
            return "ver_placar"
        elif opcao == "sair":
            return "sair"
        else:
            print("Opção inválida! Digite 1, 2, 3 ou sair.")


def mostrar_regras():
    # Exibe as regras resumidas desta versão do jogo.
    print("\nRegras do Xadrez:")
    print("- O objetivo do jogo é dar xeque-mate no rei adversário, ou seja, atacar o rei de forma que ele não possa escapar.")
    print("- As brancas sempre começam a partida e os jogadores alternam turnos.")
    print("- Cada turno o jogador deve mover uma peça sua para uma casa válida, respeitando as regras de movimento.")
    print("- Um jogador não pode fazer um movimento que deixe ou mantenha seu próprio rei em xeque.")
    print("- As peças se movem assim:")
    print("  • Rei: uma casa em qualquer direção.")
    print("  • Dama: qualquer número de casas em linha reta, diagonal ou horizontal.")
    print("  • Torre: qualquer número de casas na vertical ou horizontal.")
    print("  • Bispo: qualquer número de casas na diagonal.")
    print("  • Cavalo: em 'L', duas casas em uma direção e uma casa perpendicular; pode pular peças.")
    print("  • Peão: uma casa para frente, ou duas casas na primeira jogada; captura uma casa na diagonal.")
    print("- Quando um peão atinge a última linha do tabuleiro, ele pode ser promovido para uma dama, torre, bispo ou cavalo.")
    print("- Xeque é quando o rei está sendo atacado por uma peça adversária.")
    print("- Xeque-mate é quando o rei está em xeque e não há nenhum movimento legal para escapar.")
    print("- Empate pode ocorrer em situações como falta de material para dar xeque-mate, repetição de posição ou acordo mútuo.")
    print("- Nesta versão simplificada, você informa movimentos como 'origem destino', por exemplo: e2 e4.")
    print("- Digite 'sair' durante a partida para retornar ao menu principal.")
    input("\nPressione Enter para voltar ao menu...")


def mostrar_placar():
    # Mostra os resultados salvos no arquivo de placar.
    print("\nPlacar salvo:")

    resultados = carregar_resultados()
    if resultados is None:
        input("\nPressione Enter para voltar ao menu...")
        return

    if not resultados:
        print("Nenhum resultado salvo ainda.")
    else:
        for indice, resultado in enumerate(resultados, start=1):
            vencedor = resultado['vencedor']
            quantidade_jogadas = resultado['quantidade_jogadas']
            tipo_finalizacao = resultado['tipo_finalizacao']

            print(f"{indice}. Vencedor: {vencedor}")
            print(f"   Jogadas: {quantidade_jogadas}")
            print(f"   Finalização: {tipo_finalizacao}")

    input("\nPressione Enter para voltar ao menu...")


def iniciar_partida():
    # Executa o laço principal da partida até o jogo terminar.
    print("\nIniciando a partida...")
    tabuleiro = criar_tabuleiro()
    historico_jogadas = []
    turno_atual = "branco"
    status_xeque = obter_status_xeque(tabuleiro)

    print("\n" + "="*40)
    print("Tabuleiro Inicial:")
    print("="*40)
    imprimir_tabuleiro(tabuleiro)

    while True:
        print("\n" + "-"*40)
        cor_turno = "BRANCAS" if turno_atual == "branco" else "PRETAS"
        print(f"Turno: {cor_turno}")
        print("-"*40)

        jogada = ler_jogada()
        resultado = processar_comando_especial(jogada, turno_atual, historico_jogadas)
        if resultado is not None:
            registrar_resultado(historico_jogadas, resultado)
            exibir_historico(historico_jogadas)
            break

        origem, destino = jogada
        indice_origem = coordenada_para_indice(origem)
        indice_destino = coordenada_para_indice(destino)

        linha_orig, col_orig = indice_origem

        if not movimento_valido(tabuleiro, indice_origem, indice_destino, turno_atual):
            print("Erro: Movimento inválido! Verifique origem, destino e as regras da peça.")
            print("Tentando novamente no mesmo turno...\n")
            continue

        peca = tabuleiro[linha_orig][col_orig]

        peca_capturada = executar_jogada(tabuleiro, indice_origem, indice_destino)
        registrar_jogada(historico_jogadas, turno_atual, peca, origem, destino, peca_capturada)

        if peca_capturada:
            print(f"Peça capturada: {peca_capturada}")

        print(f"Jogada executada: {origem} -> {destino}")
        print("Tabuleiro após o movimento:")
        imprimir_tabuleiro(tabuleiro)

        fim = verificar_fim_de_jogo(tabuleiro)
        if fim is not None:
            quantidade_jogadas = obter_quantidade_jogadas(historico_jogadas)

            if fim['tipo'] == 'vitoria':
                resultado = declarar_vencedor(fim['vencedor'], fim['motivo'], quantidade_jogadas)
            else:
                resultado = finalizar_por_empate(quantidade_jogadas)

            registrar_resultado(historico_jogadas, resultado)
            exibir_historico(historico_jogadas)
            break

        novo_status_xeque = obter_status_xeque(tabuleiro)
        exibir_avisos_de_xeque(status_xeque, novo_status_xeque)
        status_xeque = novo_status_xeque

        turno_atual = alternar_turno(turno_atual)


def processar_comando_especial(jogada, turno_atual, historico_jogadas):
    # Trata os comandos de encerramento digitados durante a partida.
    quantidade_jogadas = obter_quantidade_jogadas(historico_jogadas)

    if jogada == "sair":
        return finalizar_por_saida_manual(quantidade_jogadas)
    if jogada == "desistir":
        return finalizar_por_desistencia(turno_atual, quantidade_jogadas)
    if jogada == "empate":
        return finalizar_por_empate(quantidade_jogadas)
    return None


def main():
    # Exibe o menu principal e direciona o fluxo do programa.
    print("Bem-vindo ao Jogo de Xadrez em Python!")

    while True:
        acao = exibir_menu()

        if acao == "iniciar_partida":
            iniciar_partida()
        elif acao == "ver_regras":
            mostrar_regras()
        elif acao == "ver_placar":
            mostrar_placar()
        elif acao == "sair":
            print("Saindo do programa. Até a próxima!")
            break


if __name__ == "__main__":
    main()
