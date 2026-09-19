#!/usr/bin/env python3
"""Atualiza a lista de exercícios embutida no java-bancada.html.

A lista era escrita à mão, e por isso ficava para trás: o notaFinal.java
esteve commitado durante três dias sem nunca aparecer no separador
Exercícios. Isto lê a pasta `exercicios/` e escreve a lista a partir dela.

    python3 exercicios-atualizar.py

Correr depois de acrescentar (ou mexer em) um exercício. É idempotente:
correr duas vezes seguidas não muda nada na segunda.

O QUE ESTE SCRIPT DECIDE E O QUE NÃO DECIDE
O ficheiro e o código vêm do disco, sempre. A descrição não: essa fica
onde já estava, dentro do java-bancada.html, e este script só a transporta
de uma versão da lista para a seguinte. Um exercício novo entra sem
descrição e o script diz-te quais faltam — escreve-a no HTML, no campo "d",
e a partir daí ela sobrevive a todas as corridas seguintes.

O nome na lista também se preserva tal e qual (o `tipos.java` do disco está
na lista como "Tipos.java" desde sempre). É esse nome que marca o exercício
como feito no teu navegador: mudá-lo apagava-te as marcações.
"""
import base64
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "java-bancada.html"
EXDIR = ROOT / "exercicios"
MARK = re.compile(r"/\*@EXERCICIOS:START\*/.*?/\*@EXERCICIOS:END\*/", re.S)

texto = PAGE.read_text(encoding="utf-8")
achado = MARK.search(texto)
if not achado:
    raise SystemExit(
        "Marcador @EXERCICIOS não encontrado em java-bancada.html. A lista "
        "tem de estar entre /*@EXERCICIOS:START*/ e /*@EXERCICIOS:END*/."
    )

# o que já lá está: guarda o nome exato e a descrição de cada exercício
corpo = achado.group(0)
corpo = corpo[len("/*@EXERCICIOS:START*/"):-len("/*@EXERCICIOS:END*/")]
antigos = json.loads(corpo)
por_ficheiro = {e["n"].lower(): e for e in antigos}

ficheiros = sorted(EXDIR.rglob("*.java"), key=lambda p: (str(p.parent), p.name))
if not ficheiros:
    raise SystemExit(f"Nenhum .java em {EXDIR} — não vou apagar a lista toda.")

# a ordem que já lá estava manda; os novos entram a seguir, na ordem da pasta
por_nome = {p.name.lower(): p for p in ficheiros}
ordem = [e["n"].lower() for e in antigos if e["n"].lower() in por_nome]
ordem += [n for n in por_nome if n not in ordem]

lista, sem_descricao, sumidos = [], [], []
for chave in ordem:
    caminho = por_nome[chave]
    velho = por_ficheiro.get(chave, {})
    descricao = velho.get("d", "")
    if not descricao:
        sem_descricao.append(caminho.name)
    lista.append({
        "n": velho.get("n", caminho.name),   # nunca renomear: parte as marcações
        "d": descricao,
        "src": base64.b64encode(caminho.read_bytes()).decode("ascii"),
    })

for chave, velho in por_ficheiro.items():
    if chave not in por_nome:
        sumidos.append(velho["n"])

# "</" dentro do código fecharia o <script> da página
dados = json.dumps(lista, ensure_ascii=False).replace("</", "<\\/")
novo, n = MARK.subn(
    lambda _: "/*@EXERCICIOS:START*/" + dados + "/*@EXERCICIOS:END*/", texto)
if n != 1:
    raise SystemExit("Marcador @EXERCICIOS apareceu mais do que uma vez.")

mudou = novo != texto
if mudou:
    PAGE.write_text(novo, encoding="utf-8")
print(f"{len(lista)} exercícios em {PAGE.name}" + ("" if mudou else " (já estava certo)"))

if sumidos:
    print("saíram da lista, porque o ficheiro já não existe: " + ", ".join(sumidos))
if sem_descricao:
    print("sem descrição, escreve-a no campo \"d\" do java-bancada.html: "
          + ", ".join(sem_descricao))
    sys.exit(1)   # falha de propósito: uma lista com buracos não passa despercebida
