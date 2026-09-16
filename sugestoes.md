# Sugestões — 2026-09-16

Rascunho de coisas que valeria a pena mudar. Nada disto foi feito — é para
decidires amanhã o que faz sentido.

## 1. Fechar o canal da sala aos estranhos (segurança, prioridade alta)

Já está meio feito: o `bibi/supabase.sql` tem a política pronta e o
`java-bancada.html` tem o sítio exato marcado com `@CANAL-PRIVADO` (perto da
linha 2498) para ligar `private:true` nos canais `sala` e `lago-presenca`.
Falta só:

1. Correr a secção "Canal da sala" do `bibi/supabase.sql` no SQL Editor do
   Supabase (a parte de cima, das cartas, já deve estar corrida).
2. Só depois, acrescentar `private:true` ao `config` dos dois `client.channel(...)`
   marcados no HTML.

Não fiz isto sozinho porque a ordem importa — ligar `private:true` antes de
a política existir parte o tempo real todo, e eu não tenho como confirmar
daqui se o SQL já correu no teu projeto. Enquanto isto não acontece, quem tirar
a chave publicável do HTML (é preciso estar visível, isso é normal) consegue
ligar-se ao canal `sala` e ao `lago-presenca` e escrever lá dentro com um nome
à escolha — não injeta HTML (isso já está tapado), mas consegue fingir ser o
Bibi ou o Louzy, mandar gestos falsos ("torcida", "desafio", convites de
música) e ver em tempo real o que cada um está a fazer no site. Depois do
`private:true`, só entra quem tiver sessão numa das duas contas.

## 2. Placar do Swanrejas preso no primeiro recorde do dia (bug, causa provável identificada)

Reportado: o recorde no placar do Swanrejas ficou parado em 317 e não sobe,
mesmo depois de jogos com pontuação maior.

O que encontrei no código (`java-bancada.html`, `Placar.registar`, à volta da
linha 2714): cada partida de Swanrejas é gravada na tabela `partidas` do
Supabase sem indicar o campo `dia` — só o Swandoku manda esse campo de
propósito (é o que lhe permite um só tabuleiro por dia). Para o resumo
semanal do Swanrejas funcionar (`resumo()`, linha ~2725, filtra por
`r.dia >= semana` em todos os jogos, não só no Swandoku), a coluna `dia` tem
de vir preenchida sozinha pelo servidor com a data de hoje.

A função `registar()` já sabe lidar com "repetida" — quando a base de dados
recusa a gravação por duplicado, mas isso está pensado só para o Swandoku
("o Swandoku do dia já estava registado", diz o próprio comentário no
código). Se o índice/constraint que impede duplicados no Supabase for
único por (conta, jogo, nível, dia) sem excluir o Swanrejas, a base de dados
está a recusar em silêncio qualquer segunda partida de Swanrejas no mesmo
dia — o pedido falha, o `catch` interpreta como "repetida", e a pontuação
nova nunca chega a gravar-se nem a aparecer no placar. Achas 317 porque foi
a primeira pontuação do dia a entrar; tudo o que jogaste depois, no mesmo
dia, foi silenciosamente ignorado. (O jogo "Adivinha a música" tem
exatamente o mesmo problema, pela mesma razão — vale a pena reparar se
notaste o mesmo lá.)

Não consigo confirmar isto com certeza nem corrigi-lo sozinho: o SQL dessa
tabela vive em `bibi/placar.sql`, que está no `.gitignore` de propósito —
não faz parte deste repositório e eu não tenho acesso ao teu projeto
Supabase. Para confirmar e corrigir, no SQL Editor do Supabase:

```sql
-- confirmar o nome do índice/constraint responsável
select conname, pg_get_constraintdef(oid)
from pg_constraint
where conrelid = 'public.partidas'::regclass and contype in ('u', 'p');
-- ou, se for um índice em vez de constraint:
select indexname, indexdef from pg_indexes where tablename = 'partidas';
```

Se aparecer algo como `unique (autor, jogo, nivel, dia)` sem filtro por jogo,
o arranjo é trocá-lo por um índice parcial só para o Swandoku:

```sql
alter table public.partidas drop constraint nome_encontrado_acima;
create unique index partidas_swandoku_dia_unico on public.partidas (autor, jogo, nivel, dia)
  where jogo = 'swandoku';
```

Isto mantém o Swandoku a um tabuleiro por dia e deixa o Swanrejas e o
Adivinha a música gravarem quantas partidas quiseres no mesmo dia.

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
