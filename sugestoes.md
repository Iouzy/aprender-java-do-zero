# Sugestões — 2026-09-17

Rascunho de coisas que valeria a pena mudar. Nada disto foi feito — é para
decidires amanhã o que faz sentido. (As sugestões de 16/09 já resolvidas
ou já decididas saíram daqui; ver histórico do ficheiro no git se precisares
de as reler.)

## 1. Verificação de hoje: datas, acesso e bugs

Pediste para verificar as datas dos exercícios, se algum estranho consegue
mandar mensagens/comandos/código no site, e para corrigir bugs. O que
encontrei e já corrigi (não é sugestão, já está feito e vai no mesmo commit):

- **`notaFinal.java` não aparecia na bancada.** Foi criado na sessão de
  16/09 mas nunca foi adicionado à lista `EXERCISES` do `java-bancada.html`
  — por isso não tinha simulador, não contava para o total de exercícios
  (ficava em 16, devia ser 17) e não tinha como ser marcado como feito.
  Acrescentei a entrada; a data resolve-se sozinha a partir do commit
  `745e92b` (16 de setembro, a hora certa), sem precisar de correção manual.
- **Lista de commits embutida estava um commit atrasada** (`java-bancada.html`,
  bloco `@COMMITS`): tinha o hash antigo do último commit da sessão de 16/09,
  de antes de um amend/reescrita. Corri o `bibi-atualizar.py` (já fora de
  clone raso — tinha de fazer `git fetch --unshallow` primeiro) e ficou
  atualizada. As datas dos 16 exercícios anteriores continuavam todas certas,
  nenhuma tinha voltado a colapsar em 14/09 22:26.
- **As datas que reportaste erradas não estavam erradas no repositório.**
  Conferi os dados guardados (`EXERCISES`/`FEITO_EM`/`@COMMITS`) e todos os
  17 exercícios resolvem para a data real de quando foram escritos, não para
  14/09 22:26. Se ainda estás a ver essa data errada no browser, é quase de
  certeza o `localStorage` desse aparelho com uma cópia antiga por trás de
  cache — experimenta recarregar a página a limpar a cache (Ctrl+Shift+R) e,
  se persistir, diz-me o aparelho/browser para eu tentar reproduzir.
- **"Marcar como concluídos" não dá para fazer eu sozinho.** O estado de
  "feito" de cada exercício vive no `localStorage` do teu aparelho, não no
  repositório — não há ficheiro nem base de dados que eu possa editar a
  partir daqui para isso acontecer. Continua a ser o botão "Repor marcações
  do Git" (menu ⋮ da bancada) que faz isso por ti, com as datas certas, a
  correr no teu próprio browser.
- **Acesso não autorizado:** revi o SQL (`bibi/supabase.sql`) e o código do
  canal em tempo real (`java-bancada.html`). RLS está ligado, as políticas
  só deixam contas autenticadas ler/escrever nos tópicos certos, os inserts
  em `cartas` só aceitam `tipo`/`texto`/`selo` (autor e nome vêm sempre do
  servidor) e todo o texto de mensagens é escapado antes de ir para o HTML
  (`esc()`), por isso não há injeção de HTML/script pelas cartas. Não
  encontrei forma de um estranho mandar mensagens, comandos ou código sem
  sessão numa das duas contas. Duas coisas que o código sozinho não
  confirma, porque vivem só nas definições do Supabase, não no
  repositório — vale a pena ires confirmar lá:
  - Authentication → registo de contas novas continua desligado?
  - O SQL de `bibi/supabase.sql` está mesmo corrido tal como está agora no
    ficheiro (a versão das cartas, não só a versão antiga dos recados)?

## 2. Sistema de fecho de sessão — ainda por testar em condições reais

A sessão de 16/09 criou o `sessoes/_template.md`, `sessoes/HISTORICO.md` e
as instruções de fecho no `CLAUDE.md`, mas só correu uma vez, no fim dessa
mesma sessão que as criou — nunca foi posto à prova numa sessão normal, do
início ao fecho. Vale a pena veres se o `sessoes/2026-09-16.md` reflete bem
o que passou-se, e se as colunas do `HISTORICO.md` fazem sentido depois de
mais uma ou duas sessões — pode ser cedo para saber se o formato é o certo.

## 3. Nome da conta continua a não estar amarrado à sessão (baixo risco)

Registado desde 16/09, ainda por decidir: `Live.on("gesto"...)` confia no
campo `nome` que vem dentro do payload da mensagem, só confere que é
"bibi" ou "louzy" e que não é o teu próprio nome. Como o canal já exige
sessão de uma das duas contas, o único cenário é a conta do Bibi dizer que
é o Louzy (ou vice-versa) — as duas contas são de confiança mútua, por
isso o risco real é baixo. Dava para fechar de vez lendo o nome de
`Conta.user().nome` em vez do payload, se quiseres a coisa mais correta em
vez de suficiente.

## 4. Vídeo partilhado entre duas faixas no gira-discos (por confirmar)

Ainda por resolver desde 16/09: o id do YouTube `LrSX_OcpeJg` está em duas
faixas do álbum "Norman Fucking Rockwell!" de propósito (vídeo oficial
duplo), mas faz o `Map()` de identificação do "Adivinha a música" e da
letra em tempo real assumirem sempre a segunda faixa ("The greatest").
Encontrei candidato para separar (`EqOwBkxhSZI`, "Lana Del Rey - The
greatest") mas não confirmei que é o oficial — precisa da tua palavra
antes de trocar.
