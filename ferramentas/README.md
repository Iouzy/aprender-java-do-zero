# ferramentas/ — a automatização

O objetivo: **nunca pedir nada a ninguém para o estado ficar guardado**.
Tu programas; os ficheiros escrevem-se sozinhos.

## Instalar (uma vez)

```bash
cd ~/aprender-java-do-zero
./ferramentas/instalar.sh
```

Isso põe o `jc` no PATH, passa-te para o ramo `bruto` e mete o cron de 10 em
10 minutos. Abre um terminal novo depois.

## As três camadas

| Camada | Onde corre | Quando | O que faz |
|---|---|---|---|
| `jc` | tua máquina | a cada compilação | grava a versão, cola o erro do compilador no log, corre o programa |
| `guardar.sh` (cron) | tua máquina | de 10 em 10 min | `git push` do trabalho para o ramo `bruto` |
| Routine | cloud | 1×/dia | lê o `bruto`, faz *squash merge* dele para o `main`, conta, julga, escreve os documentos, e fecha tudo num commit |

A tua máquina só precisa de estar ligada enquanto estudas. A Routine corre com
o PC desligado — mas só vê o que o cron já empurrou.

## `jc` — usa isto em vez do javac

```bash
jc MediaArray.java
```

- Cada tentativa diferente vai para `versoes/MediaArray/v1.java`, `v2.java`, …
  Recompilar sem mudar nada não inventa uma versão nova.
- Cada compilação escreve em `sessoes/erros-bruto.log`:

```
== 2026-09-17T21:14:03+01:00 MediaArray v3 exit=1
MediaArray.java:7: error: incompatible types: possible lossy conversion from double to int
```

  Uma linha `==` por compilação (data ISO, classe, versão, código de saída), e
  por baixo o erro do compilador **em bruto**. É o formato que a Routine lê.
- Se compilou, corre o programa. Se não, mostra o erro e devolve 1.

## O ramo `bruto`

Trabalhas sempre no `bruto`. Os commits de 10 em 10 minutos são fita de
gravação — não são commits de ideia, e por isso não vão assim para o `main`.

À noite a Routine faz `git merge --squash origin/bruto` e fecha o dia num
único commit no `main`, junto com os documentos. Resultado: o `main` fica
com o código **e** o dossier, um commit por dia de estudo, com mensagem
sobre o porquê. O `bruto` fica atrás de propósito — é a cassete, não o
dossier, e ninguém o lê.

Tu não fazes merges nem pulls. Nunca faças `git checkout main` na tua
máquina: lê o `main` no GitHub. Se um dia quiseres o dossier em casa,
`git fetch origin && git show origin/main:ESTADO.md`.

## O que é automático e o que não é

Automático, sem tu saberes que acontece:
- versões de código até compilar, e o erro exato de cada uma
- hora de cada compilação → duração da sessão e gap desde a última
- tempo entre o início e a primeira versão gravada → padrão de adiamento
- que exercício e que fase, a partir dos ficheiros mexidos

Automático, mas é juízo do modelo (a Routine decide, não conta):
- qual das 6 fraquezas do ROADMAP causou cada erro
- se a dúvida era de conceito ou de sintaxe

Não deixa rasto no disco, logo ninguém o pode automatizar:
- o que te passou pela cabeça e nunca escreveste

Se quiseres apanhar essa parte, acrescenta uma linha a `sessoes/notas-hoje.md`
quando te apetecer. A Routine consome-o e apaga-o. Vazio também serve — o log
de erros sozinho dá quase tudo.

## Desfazer

```bash
crontab -l | grep -v guardar-java.sh | crontab -   # desliga o cron
rm ~/bin/jc ~/bin/guardar-java.sh                  # tira as ferramentas
```
