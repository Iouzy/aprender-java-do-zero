# Sugestões — 2026-09-19

Pediste para repor as datas dos exercícios (estavam todas a aparecer em 14 de
setembro 22:26), conferir se mais alguém consegue mexer no site sem
permissão, e corrigir bugs. Fica aqui o que encontrei, o que já corrigi, e o
que fica para decidires — nada dos pontos "a decidir" foi feito.

## Datas dos exercícios: já estavam certas no `main` — encontrei outra coisa a mais

Fui ver o `java-bancada.html` que está no `main` (commit `314a0e0`, o mesmo
que o GitHub Pages serve) e as datas embutidas em `COMMITS` já vão de 7 a 16
de setembro, sem colapso nenhum — o guarda-costas contra o clone raso que
ficou no `bibi-atualizar.py` (ver a secção de 16/09 mais abaixo) está a
funcionar: tentei mesmo correr o script aqui, num ambiente com clone raso, e
ele recusou-se a mexer no ficheiro, como devia.

Ou seja: o código e os dados já estão corretos desde 16/09. Se ainda vês
14/09 22:26 no ecrã, o mais provável é a página estar aberta numa aba antiga
(as datas só são lidas uma vez, quando a página carrega) ou uma cópia em
cache do browser/GitHub Pages — experimenta fechar a aba de vez e abrir o
site outra vez (ou Ctrl+Shift+R). Se depois disso ainda aparecer errado,
avisa que há aqui um bug novo por encontrar.

**O que encontrei a mais, e já corrigi:** o `notaFinal.java` (o exercício de
switch+do-while de 16/09) tinha commit próprio no histórico mas nunca tinha
sido acrescentado às listas `EXERCISES` e `CUTE` do `java-bancada.html`. Não
aparecia sequer como opção na bancada (contava sempre "16" exercícios, nunca
os 17 reais), e o Modo Bibi já o contava por baixo dos panos — por isso o
total de "cerejas" no Modo Bibi e o "x/16" da bancada nunca batiam certo, e o
dia 16/09 no calendário/diário mostrava o nome cru do ficheiro em vez de uma
descrição em português. Já corrigido: entrou nas duas listas.

## Marcar tudo como concluído: só tu consegues, num clique

O "feito"/"não feito" de cada exercício vive no `localStorage` do teu
próprio aparelho, não no repositório — por isso não há como eu marcar isso
por ti a partir daqui (a mesma limitação já registada a 16/09, ver secção de
baixo, ponto 5). O menu já tem o botão certo para isto: **"Repor marcações
do Git"** marca como feito qualquer exercício com commit no histórico
(agora os 17, incluindo o notaFinal.java) nas datas certas, e desmarca os
que não têm. Um clique nesse botão faz exatamente o que pediste.

## Bugs que corrigi

- **Adivinha a música mostrava o recorde errado** — o mesmo bug que já
  tinha sido corrigido no Swanrejas (ver 16/09, ponto 2): o "recorde" da
  caixa inicial e o aviso de "novo recorde" vinham de `localStorage`
  (`java-musica-v1`), que é do aparelho, não da conta. Num aparelho
  partilhado pelos dois, um via como seu o recorde que o outro tinha feito.
  Corrigido para usar primeiro `Placar.recordes("musica", 0)` — o recorde
  partilhado da conta — tal como o Swanrejas já fazia, só caindo para o
  valor local quando não há sessão ou o Supabase está em baixo.
- **`notaFinal.java` em falta na bancada** — descrito acima.
- **Valor do placar sem escape ao entrar no `innerHTML`** — ver a secção de
  segurança a seguir.

## Segurança: quem consegue mexer no site sem ser um dos dois

Pedi uma auditoria de tudo o que o `java-bancada.html` manda para o
Supabase (mensagens, cartas, presença, jogos, o canal em tempo real) à
procura de alguma forma de outra pessoa mandar mensagens, comandos ou
código sem ser uma das duas contas. Resumo:

- **Nada encontrado que um estranho na internet consiga explorar hoje.** A
  tabela `cartas` e o canal em tempo real (`sala`, `lago-presenca`) — os
  dois sítios com o SQL completo aqui no repositório — estão bem fechados:
  RLS ligado, só para contas autenticadas, e o autor de cada carta vem
  sempre do servidor (`auth.uid()`), nunca do que o browser manda, por isso
  ninguém consegue escrever a fingir ser o outro.
- **Ponto cego real: `bibi/placar.sql`** (as tabelas dos jogos e placares)
  está no `.gitignore` e nunca chegou a este repositório — não há como eu
  confirmar que tem as mesmas proteções da `cartas` (RLS só para contas
  autenticadas, autor preenchido pelo servidor). Pelo que o site manda,
  parece seguir o mesmo padrão seguro, mas isto precisa de ser confirmado
  a olhar para o SQL real no painel do Supabase — ou, melhor ainda,
  versionar uma cópia desse ficheiro (já sem segredos, é só estrutura de
  tabela) para deixar de ser um ponto cego.
- **A verificação mais importante de todas não dá para fazer por código:**
  no painel do Supabase, em Authentication, confirma que "permitir novas
  contas" continua desligado. Enquanto isso estiver desligado, só as duas
  contas de sempre entram. Se algum dia for ligado sem querer, a política
  de leitura da `cartas` (`for select to authenticated using (true)`) deixa
  qualquer conta nova ler tudo — por isso este interruptor é o que separa
  "fechado aos dois" de "aberto a quem se registar".
- Corrigido de qualquer forma, por segurança extra: o valor de cada jogador
  na tabela do placar (`Placar.render`, `java-bancada.html` à volta da linha
  2861) ia direto para `innerHTML` sem passar pelo `esc()` que o resto da
  página usa. Hoje em dia o valor chega sempre como número, então não dá
  para explorar isto através do próprio site — mas se a tabela do placar
  não tiver a coluna bem tipada (o tal ponto cego de cima), uma das duas
  contas podia mandar uma string feita à medida direto para a API e pôr
  código a correr no ecrã da outra. Sem custo nenhum corrigir já, por isso
  corrigi.

## A confirmares tu, quando decidires (nada disto foi feito)

1. Confirmar no painel do Supabase que o registo de contas novas continua
   desligado (o ponto mais importante da lista acima).
2. Ver o SQL real de `bibi/placar.sql` no Supabase e confirmar que segue o
   mesmo padrão da `cartas` — e considerar versionar uma cópia sem segredos
   dele aqui, para deixar de ser um ponto cego em auditorias futuras.
3. Não encontrei nenhuma tabela `swandoku` a ser chamada pelo site (o nome
   só aparece como valor dentro das linhas de `partidas`) — vale a pena
   confirmares se essa tabela ainda existe mesmo no Supabase ou se é sobra
   de uma versão antiga.
4. Uma ideia para o `notaFinal.java` não se repetir: um exercício novo só
   aparece na bancada quando alguém se lembra de o acrescentar a duas
   listas (`EXERCISES` e `CUTE`) à mão. Dava para a bancada avisar sozinha
   quando um ficheiro em `exercicios/*.java` tem commit mas não está em
   nenhuma das duas listas — pequeno, mas evita que isto volte a acontecer
   caladinho.

---

# Sugestões — 2026-09-16

Rascunho de coisas que valeria a pena mudar. Nada disto foi feito — é para
decidires amanhã o que faz sentido.

## 1. Fechar o canal da sala aos estranhos (segurança) — feito

A política em `realtime.messages` foi corrida no SQL Editor do Supabase
(sem a linha `alter table ... enable row level security`, que dá erro de
posse do lado do Supabase — a tabela já vem com RLS ligado de origem, só
faltavam as políticas). Depois disso, `private:true` foi acrescentado ao
`config` dos dois `client.channel(...)` (`sala` e `lago-presenca`,
`java-bancada.html`). A partir de agora só entra no canal quem tiver
sessão numa das duas contas — antes, quem tirasse a chave publicável do
HTML conseguia ligar-se e escrever lá dentro com um nome à escolha.

## 2. Recorde do Swanrejas a mostrar o número errado (bug, já corrigido)

Reportado: a caixa "Pronto?" do Swanrejas dizia "O teu recorde é 317", mas
esse número nunca subia nem batia certo com o cartão do placar ao lado
(que mostrava 170, certinho com a base de dados).

Descartei primeiro a hipótese de ser a base de dados (não há constraint nem
índice a bloquear partidas repetidas do Swanrejas no mesmo dia — só existe
o `partidas_swandoku_uma_vez`, e esse já vem com condição própria, só para
o Swandoku). A tabela `partidas` só tinha 19 linhas ao todo, e o valor mais
alto lá registado em cerejas era 221 (Bibi) e 170 (Louzy) — o 317 não
existia em lado nenhum da base de dados.

A causa real: o "317" vinha do `data.best`, guardado em `localStorage` sob
uma chave única (`BIBI_KEY = "java-bibi-v1"`, `java-bancada.html:2408`) que
**não distingue quem está autenticado** — é do aparelho, não da conta. Um
número desse aparelho, de outra sessão (provavelmente da Bibi, ou de antes
de existir login por conta), ficava a aparecer como "o teu recorde" a quem
quer que estivesse com sessão aberta nesse browser, e como estava sempre
acima do que a conta realmente tinha feito, nunca "subia" — parecia preso.

Corrigido: a caixa "Pronto?" e a deteção de "novo recorde" no fim do jogo
passam a usar primeiro o recorde da conta que já vem certo do placar
partilhado (`Placar.recordes`), só caindo para o valor local do aparelho
quando não há sessão ou o Supabase está em baixo. O `data.best` continua a
existir só como retrocesso para esse caso.

## 3. Reforçar quem pode dizer que é quem, dentro do canal já privado

Mesmo depois do `private:true`, o campo `nome` de cada mensagem continua a vir
do que quem envia decidir mandar — o código só confere que é "bibi" ou "louzy"
e que não é o teu próprio nome (`Live.on("gesto"...)`, `Sala` em
`java-bancada.html`). Ou seja, a conta do Bibi consegue tecnicamente mandar um
gesto a dizer que é o Louzy. Como são só duas contas de confiança mútua, o
risco é baixo — mas dava para fechar de vez amarrando o `nome` à sessão
(`Conta.user().nome`) em vez de confiar no campo que vem no payload.

## 4. Impedir que o `bibi-atualizar.py` volte a partir-se com um clone raso

Já corrigido o guarda-costas no próprio script (aborta se
`git rev-parse --is-shallow-repository` for `true`), que foi a causa das datas
dos exercícios teres aparecido todas em 14/09 22:26. Fica como nota para não
esquecer: se algum dia isto correr outra vez num ambiente com clone raso
(sandboxes, CI, etc.), o script agora avisa em vez de corromper as datas em
silêncio. Vale a pena, no entanto, pensar num hook `post-commit` (o próprio
cabeçalho do script já sugere isto) para deixar de depender de correr o
script à mão.

## 5. "Repor marcações do Git" — comportamento a confirmar

Corrigi o botão do menu "Repor marcações do Git": antes apagava todas as
marcações (`state.done = {}`), ao contrário do que o próprio texto do
`confirm()` prometia. Agora marca como feito qualquer exercício que tenha
commit no histórico, e desmarca os que não têm. Isto também é o que preenche
os 16 exercícios como concluídos, nas datas corretas — mas só depois de
clicares nesse botão no teu browser (o estado de "feito" vive no
`localStorage` de cada aparelho, não no repositório, por isso não há como eu
fazer essa marcação por ti a partir daqui).

Vale a pena confirmares que é isto que queres como comportamento definitivo
do botão (marcar tudo o que tem commit, sem olhar às dez previsões certas no
simulador que a regra da bancada pede) — ou se preferes um botão separado só
para "marcar como feito os que já têm commit, mas nunca desmarcar os que já
tinhas marcado à mão".

## 6. Vídeo trocado no gira-discos (bug a confirmar, não corrigi sozinho)

No álbum "Norman Fucking Rockwell!" (`java-bancada.html`, à volta da linha
2879), o id de vídeo do YouTube `LrSX_OcpeJg` aparece duas vezes na mesma
lista: na faixa 4 ("Fuck it I love you") e na faixa 11 ("The greatest"). O
`TRACK` é um `Map()` indexado pelo id do vídeo, por isso a segunda entrada
substitui a primeira — sempre que esse vídeo está a tocar, o site identifica-o
como "The greatest", nunca como "Fuck it I love you" (afeta a letra em tempo
real e o jogo "Adivinha a música").

Não corrigi isto sozinho porque `LrSX_OcpeJg` é mesmo o vídeo oficial
duplo "Fuck it I love you / The greatest" — as duas faixas partilham o
mesmo vídeo de propósito, não foi copy-paste. Se quiseres separar as duas
faixas para a identificação ficar certa, precisas de escolher um vídeo (ou
áudio) só para "The greatest" — encontrei candidato em busca:
`https://www.youtube.com/watch?v=EqOwBkxhSZI` ("Lana Del Rey - The
greatest"), mas não confirmei que é o oficial que queres usar, por isso é
melhor confirmares tu antes de trocar o id.

## 7. Registo de novas contas no Supabase

O `bibi/supabase.sql` assume "registo de contas novas desligado" nas
definições de Authentication do projeto. Não dá para confirmar isso a partir
do código — vale a pena ires lá confirmar que a opção continua desligada,
até porque combina diretamente com o ponto 1 (sem isso, um estranho podia
simplesmente criar conta própria e entrar por essa porta, mesmo com o canal
privado).
