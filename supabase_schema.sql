create table if not exists public.sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  date date not null,
  kind text not null,
  minutes int not null check (minutes between 1 and 300),
  effort int not null check (effort between 1 and 10),
  rating int check (rating between 1 and 5),
  notes text,
  created_at timestamptz default now()
);
alter table public.sessions enable row level security;
create policy "own select" on public.sessions for select using (auth.uid() = user_id);
create policy "own insert" on public.sessions for insert with check (auth.uid() = user_id);
create policy "own update" on public.sessions for update using (auth.uid() = user_id);
create policy "own delete" on public.sessions for delete using (auth.uid() = user_id);
