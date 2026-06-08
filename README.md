# Jogo de Xadrez em Python

Projeto da disciplina de Programação de Computadores desenvolvido em Python puro, sem uso de bibliotecas externas. O jogo roda no terminal, imprime o tabuleiro na tela e permite jogar uma partida de xadrez em uma versão simplificada.

## Objetivo do projeto

O objetivo do projeto é implementar um jogo de xadrez jogável no terminal, usando apenas recursos nativos da linguagem Python. A proposta inclui organizar a lógica do tabuleiro, validar movimentos, controlar turnos, registrar o resultado da partida e manter o código legível em um único arquivo principal.

## Tecnologias e estrutura

- Linguagem: Python
- Bibliotecas externas: nenhuma
- Arquivo principal: `xadrez.py`
- Arquivo de apoio gerado pelo programa: `placar.txt`

## Requisitos mínimos

- Python 3 instalado
- Terminal capaz de executar scripts Python
- Suporte a UTF-8 ou fonte compatível com os símbolos das peças (`♔`, `♛`, `♟`, etc.)

## Como executar

No diretório do projeto, execute:

```bash
python3 xadrez.py
```

Depois disso, o menu principal será exibido no terminal.

## Funcionalidades implementadas

- criação e exibição do tabuleiro no terminal
- identificação de cor e tipo das peças
- leitura e validação de coordenadas no formato `origem destino`, como `e2 e4`
- controle de turnos entre brancas e pretas
- validação de movimento para peão, torre, bispo, dama, cavalo e rei
- verificação de caminho livre para peças lineares
- execução de jogadas e captura de peças
- identificação de xeque e aviso durante a partida
- histórico das jogadas realizadas
- finalização por captura do rei
- finalização por desistência, empate ou saída manual
- salvamento do resultado da partida em `placar.txt`
- leitura e exibição do placar salvo no menu principal

## Regras básicas de uso

- As brancas começam a partida.
- Cada jogador deve informar uma jogada no formato `origem destino`.
- Exemplos de entrada: `e2 e4`, `g8 f6`, `a7 a5`.
- Durante a partida, também é possível digitar:
  - `desistir` para encerrar a partida e dar vitória ao oponente
  - `empate` para terminar a partida empatada
  - `sair` para encerrar a partida manualmente e voltar ao fluxo final daquela sessão
- O programa rejeita movimentos inválidos e mantém o turno do jogador até uma jogada válida ser informada.

## Como a partida termina

A partida pode terminar das seguintes formas:

- captura do rei adversário
- desistência de um dos jogadores
- empate informado pelos jogadores
- saída manual com o comando `sair`

## Xeque e xeque-mate

- O jogo identifica situações de xeque e exibe avisos no terminal.
- Nesta versão, a partida termina quando um rei é capturado.
- A lógica completa de xeque-mate não está implementada.

## Autores

- Mayra Amaral (@mayraamaral)
- Marlon Andrade (@Marlon1109)
- Pietro Toledo (@pietrotoledo)
- Rodrigo Gadelha (@rodrigogadelhadev)
