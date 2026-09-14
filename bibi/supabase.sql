-- Recadinhos encriptados do Modo Bibi.
-- Correr uma vez no Supabase: SQL Editor -> New query -> colar -> Run.
--
-- A página encripta cada recado no navegador (AES-GCM, chave derivada da
-- frase secreta com PBKDF2) antes de o enviar. Aqui só chega texto ilegível.
-- Qualquer pessoa pode ler e enviar texto encriptado; ninguém pode editar
-- nem apagar pelo site.

create table if not exists public.recados (
  id bigint generated always as identity primary key,
  criado timestamptz not null default now(),
  dados text not null
);

-- o Postgres não aceita repetições acima de 255 numa expressão regular: o tamanho vai à parte
alter table public.recados drop constraint if exists recados_dados_check;
alter table public.recados add constraint recados_dados_check
  check (length(dados) between 60 and 6100 and dados ~ '^v1\.[A-Za-z0-9+/]{16}\.[A-Za-z0-9+/=]+$');

alter table public.recados enable row level security;

revoke all on public.recados from anon, authenticated;
grant select (id, criado, dados) on public.recados to anon;
grant insert (dados) on public.recados to anon;

drop policy if exists "ler recados encriptados" on public.recados;
create policy "ler recados encriptados" on public.recados
  for select to anon using (true);

drop policy if exists "enviar recados encriptados" on public.recados;
create policy "enviar recados encriptados" on public.recados
  for insert to anon with check (true);

-- Trava contra spam: no máximo 30 recados em 10 minutos.
create or replace function public.recados_limite()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if (select count(*) from public.recados where criado > now() - interval '10 minutes') >= 30 then
    raise exception 'Demasiados recados seguidos. Tenta daqui a pouco.';
  end if;
  return new;
end;
$$;

drop trigger if exists recados_limite on public.recados;
create trigger recados_limite
  before insert on public.recados
  for each row execute function public.recados_limite();
