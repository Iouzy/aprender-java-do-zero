# Sugestões — 2026-09-18

Pediste para ver as datas dos exercícios, confirmar que mais ninguém consegue
fazer coisas no site sem autorização, corrigir bugs, e deixar aqui um rascunho
do que falta — nada disto foi feito para além do que está marcado "já
corrigido"; o resto é para decidires amanhã.

## 1. As datas "todas em 14/09 22:26" — a causa já estava corrigida, o sintoma pode ainda estar no teu browser

Confirmei o histórico do Git (`main` e `bruto`, os dois atualizados) e os
dados de datas embutidos no `java-bancada.html`: não há nenhuma data
colapsada — cada exercício tem a data real do commit dele, espalhadas entre
7 e 17 de setembro. O `dc45cfd`…`f9882f4` só têm mesmo um commit genuíno às
14/09 22:26:29 ("Modo Bibi: legendas dos números mais legíveis sobre a
névoa") — não é o bug, é só um commit normal a essa hora.

A causa do bug em si (um clone raso a colapsar todas as datas antigas na do
commit mais recente disponível) já tinha sido corrigida a 16/09 com um
guarda no `bibi-atualizar.py`, que agora recusa a correr nesse caso em vez
de gravar datas erradas — confirmei que esse guarda continua no sítio.

O que a página mostra de cada exercício (`dateLabel` em `java-bancada.html`)
é sempre calculado ao vivo a partir desses dados, nunca guardado em cache no
`localStorage` — por isso, se ainda vês 14/09 22:26 em todos, o mais
provável é o browser ter uma cópia antiga da página em cache (do GitHub
Pages ou do próprio browser), de antes da correção de dia 16. **Experimenta
um refresh a sério (Ctrl+Shift+R / Cmd+Shift+R) e volta a olhar** — se
continuar errado depois disso, avisa-me com uma captura de ecrã, porque aí é
outra coisa que ainda não vi.

Não há nada mais para eu corrigir no repositório quanto a isto — os dados
já estão certos.

## 2. "Marcar todos como concluídos" — não consigo fazer isto por ti a partir daqui

O ficheiro `java-bancada.html` já tem o botão certo para isto (menu ⋮ →
"Repor marcações do Git"), que desde dia 16 marca como feito qualquer
exercício com commit, e desmarca os que não têm (ver ponto 5 do rascunho
anterior). Mas essa marcação ("feito"/"não feito") vive no `localStorage` do
teu aparelho, não no repositório — não há ficheiro nenhum que eu possa
editar aqui que mude o que aparece no teu browser. Depois do refresh do
ponto 1, clica nesse botão e os exercícios com commit ficam marcados, com a
data certa ao lado.

Nota à parte, já que pediste para marcar "todos": a própria bancada (e o
`ROADMAP.md`, secção 2) diz que um exercício só conta como sabido depois de
acertares dez previsões seguidas no simulador — ter commit não é saber. O
botão "Repor marcações do Git" ignora essa regra de propósito (marca por
commit, não por simulador) porque foi pensado para depois de um raio
apagar tudo, não para o dia a dia. Só chamo a atenção para não usares como
atalho a saltar o simulador.

## 3. Quem consegue fazer o quê no site sem autorização — revi tudo, está sólido

Verifiquei: as políticas de RLS em `bibi/supabase.sql`, os 47 sítios onde a
página escreve HTML a partir de dados (mensagens, notas, nomes), o canal em
tempo real (`sala`/`lago-presenca`) e quem tem acesso de escrita ao
repositório no GitHub.

- **GitHub**: só a tua conta (`Iouzy`) tem acesso de escrita ao repositório.
  Mais ninguém pode alterar código por aí.
- **Canal em tempo real e mensagens**: continuam fechados a quem não tiver
  sessão numa das duas contas (`private:true` + política em
  `realtime.messages`, confirmei que ainda lá está). Todo o texto que vem de
  fora (cartas, notas, nomes) passa por `esc(...)` antes de ir para o ecrã —
  não encontrei nenhum sítio por escapar.
- **Tabela `cartas`**: um utilizador autenticado não consegue escrever em
  nome do outro — `autor`, `nome` e `criado` vêm sempre do servidor, nunca
  do que o cliente manda.

Duas coisas que fica a valer a pena confirmares tu (não dá para ver por
código):

- **Registo de contas novas no Supabase** — continua a assumir-se desligado
  nas definições do projeto; se estiver ligado, um estranho podia criar
  conta própria e entrar por aí. Vale confirmar no painel do Supabase.
- **Tabelas `partidas` e `presenca` (o placar e "quem esteve cá") não têm
  políticas no `bibi/supabase.sql`** — só `cartas` e o canal da sala têm.
  O código do cliente nunca manda `nome`/`autor` nos pedidos a estas duas
  tabelas, o que só é seguro se a base de dados os preencher sozinha (como
  faz com `cartas`) — mas isso não está no SQL que temos guardado, por isso
  não consigo confirmar por aqui se está mesmo protegido do lado do
  Supabase, ou se falta esse SQL no repositório. Risco baixo (só há duas
  contas de confiança), mas se um dia quiseres fechar isto de vez, digo-te
  o que falta escrever.

## 4. Bugs — dois corrigidos agora, um encontrado mas deixado por decidir

### Corrigidos

- **"Adivinha a música": o recorde mostrado era o do aparelho, não o da
  conta** — o mesmo bug que já tinha sido corrigido no Swanrejas dia 16,
  mas ficou por corrigir aqui. Num aparelho partilhado pelos dois, o
  recorde e o "novo recorde!" deste jogo estavam a misturar as contas.
  Corrigido da mesma forma: passa a usar primeiro o recorde do placar
  partilhado (`Placar.recordes`), só caindo para o valor local quando não
  há sessão.
- **`Sala.gesto()` deixava o campo `nome` por cima de um `extra` que também
  tivesse essa chave** — nenhum sítio da página faz isso hoje, mas era um
  descuido: bastava um `extra` com `nome` para o gesto sair com o nome
  errado. Troquei a ordem para o nome verdadeiro vencer sempre.

### Por decidir (não corrigi sozinho)

- **Vídeo trocado no gira-discos** (já reportado a 16/09, continua por
  resolver): o `id` do YouTube `LrSX_OcpeJg` serve as duas faixas "Fuck it
  I love you" e "The greatest" do NFR, de propósito (é o vídeo oficial
  duplo) — mas isso faz o site identificar sempre a faixa a tocar como "The
  greatest". Precisas de escolher um vídeo/áudio só para "The greatest" se
  quiseres separar as duas.

## 5. Nada mais para além disto

Não encontrei outros bugs concretos (com linha e cenário de falha) na parte
de acompanhamento dos exercícios (marcação, datas, filtros) nem no
login/sessão — revi com cuidado e estava tudo a bater certo com o que já
tinha sido corrigido antes.
