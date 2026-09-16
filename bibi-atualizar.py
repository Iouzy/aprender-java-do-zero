#!/usr/bin/env python3
"""Atualiza o histórico de commits embutido no java-bancada.html.

O Modo Bibi e o mapa de atividade leem estes dados. O registo em direto vai
buscar os commits ao GitHub sozinho, mas cai para esta lista quando não há
rede — por isso vale a pena mantê-la fresca. Corre depois de cada commit (ou
deixa um hook post-commit fazer isso):

    python3 bibi-atualizar.py
"""
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "java-bancada.html"
MARK = re.compile(r"/\*@COMMITS:START\*/.*?/\*@COMMITS:END\*/", re.S)

log = subprocess.run(
    ["git", "-C", str(ROOT), "log", "--reverse", "--format=%x1e%h%x1f%aI%x1f%s", "--name-only"],
    capture_output=True, text=True, check=True,
).stdout

commits = []
for record in log.split("\x1e")[1:]:
    head, _, files = record.partition("\n")
    h, t, s = head.split("\x1f")
    commits.append({"h": h, "t": t, "s": s, "f": [f for f in files.splitlines() if f.strip()]})

# "</" dentro de uma mensagem de commit fecharia o <script> da página
data = json.dumps(commits, ensure_ascii=False).replace("</", "<\\/")
text = PAGE.read_text(encoding="utf-8")
new, n = MARK.subn(lambda _: "/*@COMMITS:START*/" + data + "/*@COMMITS:END*/", text)
if n != 1:
    raise SystemExit("Marcador @COMMITS não encontrado em java-bancada.html")
PAGE.write_text(new, encoding="utf-8")
print(f"{len(commits)} commits embutidos em {PAGE.name}")
