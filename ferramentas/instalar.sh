#!/usr/bin/env bash
# instalar.sh — corre isto UMA vez, de dentro do repo, onde ele estiver:
#   cd <pasta-do-repo> && ./ferramentas/instalar.sh
# Depois nunca mais pedes nada a ninguém.
set -euo pipefail

# O repo é onde este script está, não um caminho adivinhado.
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"
[ -d .git ] || { echo "Isto não é o repo: $REPO"; exit 1; }

# 1. as ferramentas no PATH, e o caminho do repo gravado para elas
mkdir -p "$HOME/bin"
install -m 755 ferramentas/jc "$HOME/bin/jc"
install -m 755 ferramentas/guardar.sh "$HOME/bin/guardar-java.sh"
printf '%s\n' "$REPO" > "$HOME/.jc-repo"

# O PATH vai para a consola que tu usas — zsh não lê o .bashrc.
for RC in "$HOME/.zshrc" "$HOME/.bashrc"; do
  [ -e "$RC" ] || continue
  # Uma linha comentada não põe nada no PATH: só conta export activo.
  grep -qE '^[[:space:]]*export[[:space:]]+PATH=.*HOME/bin' "$RC" \
    || echo 'export PATH="$HOME/bin:$PATH"' >> "$RC"
done
if [ ! -e "$HOME/.zshrc" ] && [ ! -e "$HOME/.bashrc" ]; then
  echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.profile"
fi

# 2. passas a trabalhar no ramo `bruto` — o main é da Routine
git rev-parse --verify --quiet bruto >/dev/null || git branch bruto
git checkout bruto
git push -u origin bruto || true

# 3. o cron de 10 em 10 minutos.
# Num ficheiro à parte: com `set -e`, um `crontab -l` a falhar (ainda não há
# crontab) matava o subshell antes de a linha ser acrescentada.
command -v crontab >/dev/null || { echo "Falta o cron: sudo apt install cron"; exit 1; }
LINHA="*/10 * * * * $HOME/bin/guardar-java.sh >/dev/null 2>&1"
TMP="$(mktemp)"
crontab -l 2>/dev/null | grep -v 'guardar-java.sh' > "$TMP" || true
echo "$LINHA" >> "$TMP"
crontab "$TMP"
rm -f "$TMP"

echo
echo "Feito. Repo: $REPO"
echo "Abre uma consola nova e a partir de agora:"
echo "  jc MediaArray.java     em vez de javac + java"
echo "Estás no ramo 'bruto'. Não mudes para o main — ele é escrito na cloud."
