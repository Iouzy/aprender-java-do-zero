#!/usr/bin/env bash
# guardar.sh — de 10 em 10 minutos, empurra o trabalho em bruto para o ramo `bruto`.
#
# Corre no cron da tua máquina, enquanto estudas. Não toca no `main`:
# o `main` é escrito pela Routine noturna, na cloud, com commits de ideia.
# Se não mexeste em nada, não faz commit nenhum.
set -uo pipefail

# O caminho do repo fica em ~/.jc-repo, escrito pelo instalador.
REPO="${REPO_JAVA:-$(cat "$HOME/.jc-repo" 2>/dev/null || echo "$HOME/aprender-java-do-zero")}"
cd "$REPO" || exit 0

RAMO="$(git rev-parse --abbrev-ref HEAD)"
[ "$RAMO" = "bruto" ] || exit 0     # segurança: nunca commita fora do ramo bruto

git add exercicios sessoes versoes 2>/dev/null
git diff --cached --quiet && exit 0

git commit -q -m "bruto: $(date '+%F %H:%M')"
git push -q origin bruto || exit 0
