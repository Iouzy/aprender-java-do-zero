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

## 2. Reforçar quem pode dizer que é quem, dentro do canal já privado

Mesmo depois do `private:true`, o campo `nome` de cada mensagem continua a vir
do que quem envia decidir mandar — o código só confere que é "bibi" ou "louzy"
e que não é o teu próprio nome (`Live.on("gesto"...)`, `Sala` em
`java-bancada.html`). Ou seja, a conta do Bibi consegue tecnicamente mandar um
gesto a dizer que é o Louzy. Como são só duas contas de confiança mútua, o
risco é baixo — mas dava para fechar de vez amarrando o `nome` à sessão
(`Conta.user().nome`) em vez de confiar no campo que vem no payload.

## 3. Impedir que o `bibi-atualizar.py` volte a partir-se com um clone raso

Já corrigido o guarda-costas no próprio script (aborta se
`git rev-parse --is-shallow-repository` for `true`), que foi a causa das datas
dos exercícios teres aparecido todas em 14/09 22:26. Fica como nota para não
esquecer: se algum dia isto correr outra vez num ambiente com clone raso
(sandboxes, CI, etc.), o script agora avisa em vez de corromper as datas em
silêncio. Vale a pena, no entanto, pensar num hook `post-commit` (o próprio
cabeçalho do script já sugere isto) para deixar de depender de correr o
script à mão.

## 4. "Repor marcações do Git" — comportamento a confirmar

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

## 5. Vídeo trocado no gira-discos (bug a confirmar, não corrigi sozinho)

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

## 6. Registo de novas contas no Supabase

O `bibi/supabase.sql` assume "registo de contas novas desligado" nas
definições de Authentication do projeto. Não dá para confirmar isso a partir
do código — vale a pena ires lá confirmar que a opção continua desligada,
até porque combina diretamente com o ponto 1 (sem isso, um estranho podia
simplesmente criar conta própria e entrar por essa porta, mesmo com o canal
privado).
