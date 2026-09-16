-- Cartas do Modo Bibi, com login.
-- Correr uma vez no Supabase: SQL Editor -> New query -> colar -> Run.
--
-- Só as contas criadas em Authentication -> Users (com o registo de contas
-- novas desligado) conseguem ler e escrever. Quem não tem sessão não vê nada.

-- a versão anterior (frase secreta) deixa de ser usada
drop table if exists public.recados cascade;
drop function if exists public.recados_limite();

create table if not exists public.cartas (
  id bigint generated always as identity primary key,
  criado timestamptz not null default now(),
  autor uuid not null default auth.uid() references auth.users(id) on delete cascade,
  nome text not null default split_part(coalesce(auth.jwt() ->> 'email', ''), '@', 1),
  tipo text not null check (tipo in ('carta', 'abraco')),
  texto text check (texto is null or char_length(texto) between 1 and 240),
  selo text check (selo is null or selo in ('swan', 'cherry', 'heart', 'flower')),
  constraint carta_tem_texto check (tipo <> 'carta' or texto is not null)
);

alter table public.cartas enable row level security;

revoke all on public.cartas from anon, authenticated;
grant select on public.cartas to authenticated;
-- autor, nome e data vêm sempre do servidor: não dá para escrever em nome do outro
grant insert (tipo, texto, selo) on public.cartas to authenticated;

drop policy if exists "ler cartas" on public.cartas;
create policy "ler cartas" on public.cartas
  for select to authenticated using (true);

drop policy if exists "escrever cartas" on public.cartas;
create policy "escrever cartas" on public.cartas
  for insert to authenticated with check (autor = (select auth.uid()));

-- trava contra enganos: no máximo 30 cartas ou abraços em 10 minutos por conta
create or replace function public.cartas_limite()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if (select count(*) from public.cartas where autor = new.autor and criado > now() - interval '10 minutes') >= 30 then
    raise exception 'Demasiadas cartas seguidas. Tenta daqui a pouco.';
  end if;
  return new;
end;
$$;

drop trigger if exists cartas_limite on public.cartas;
create trigger cartas_limite
  before insert on public.cartas
  for each row execute function public.cartas_limite();

-- ---------------------------------------------------------------------------
-- Canal da sala (o tempo real entre os dois), fechado a estranhos.
--
-- Sem isto o canal é aberto: a chave publicável está no HTML, como tem de
-- estar em qualquer site, e quem a tirar de lá entra no canal, ouve o que
-- passa e também consegue escrever lá dentro com um nome à escolha.
-- Com isto, o Realtime passa a exigir o token de uma das duas contas.
--
-- ORDEM: correr este SQL PRIMEIRO. Só depois ligar o `private: true` no
-- java-bancada.html (está assinalado com «@CANAL-PRIVADO»). Ao contrário,
-- o tempo real deixa de funcionar até a política existir.

alter table realtime.messages enable row level security;

drop policy if exists "sala: ouvir" on realtime.messages;
create policy "sala: ouvir" on realtime.messages
  for select to authenticated
  using (realtime.topic() in ('sala', 'lago-presenca') and extension in ('broadcast', 'presence'));

drop policy if exists "sala: falar" on realtime.messages;
create policy "sala: falar" on realtime.messages
  for insert to authenticated
  with check (realtime.topic() in ('sala', 'lago-presenca') and extension in ('broadcast', 'presence'));
