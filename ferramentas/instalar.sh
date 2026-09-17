#!/usr/bin/env bash
# instalar.sh — corre isto UMA vez. Depois nunca mais pedes nada a ninguém.
set -euo pipefail

REPO="${REPO_JAVA:-$HOME/aprender-java-do-zero}"
cd "$REPO"

# 1. o jc fica no PATH
mkdir -p "$HOME/bin"
install -m 755 ferramentas/jc "$HOME/bin/jc"
install -m 755 ferramentas/guardar.sh "$HOME/bin/guardar-java.sh"
grep -q 'HOME/bin' "$HOME/.bashrc" || echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"

# 2. passas a trabalhar no ramo `bruto` — o main é da Routine
git rev-parse --verify --quiet bruto >/dev/null || git branch bruto
git checkout bruto
git push -u origin bruto || true

# 3. o cron de 10 em 10 minutos
LINHA="*/10 * * * * $HOME/bin/guardar-java.sh >/dev/null 2>&1"
( crontab -l 2>/dev/null | grep -v 'guardar-java.sh'; echo "$LINHA" ) | crontab -

echo
echo "Feito. Abre um terminal novo e a partir de agora:"
echo "  jc MediaArray.java     em vez de javac + java"
echo "Estás no ramo 'bruto'. Não mudes para o main — ele é escrito na cloud."
