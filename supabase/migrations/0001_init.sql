-- ─────────────────────────────────────────────────────────────────────────────
-- S.T.A.N.D Mentorship — initial schema + Row-Level Security
-- Goal: parents manage their own children's enrollments & signed forms; staff/admin
-- (Coach D) manage programs, events, rosters, and form completion.
-- RLS is the authorization layer: queries run AS THE USER via supabase-js.
-- ─────────────────────────────────────────────────────────────────────────────

create extension if not exists pgcrypto;

-- Helper: is the current user staff/admin? SECURITY DEFINER avoids RLS recursion
-- when other tables' policies check the caller's role.
create or replace function public.is_staff()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.profiles
    where id = auth.uid() and role in ('admin', 'staff')
  );
$$;

-- Helper: keep updated_at fresh.
create or replace function public.set_updated_at()
returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end; $$;

-- ── profiles (1:1 with auth.users; role drives RLS) ──────────────────────────
create table public.profiles (
  id          uuid primary key references auth.users(id) on delete cascade,
  role        text not null default 'parent' check (role in ('parent', 'staff', 'admin')),
  full_name   text,
  phone       text,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
alter table public.profiles enable row level security;
create policy "profiles: self read"   on public.profiles for select using (id = auth.uid());
create policy "profiles: self update" on public.profiles for update using (id = auth.uid()) with check (id = auth.uid());
create policy "profiles: staff read"  on public.profiles for select using (public.is_staff());
create trigger profiles_updated before update on public.profiles for each row execute function public.set_updated_at();

-- Create a profile row automatically when an auth user signs up.
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, full_name)
  values (new.id, new.raw_user_meta_data ->> 'full_name');
  return new;
end; $$;
create trigger on_auth_user_created
  after insert on auth.users for each row execute function public.handle_new_user();

-- ── participants (a parent's child[ren]) ─────────────────────────────────────
create table public.participants (
  id          uuid primary key default gen_random_uuid(),
  parent_id   uuid not null references public.profiles(id) on delete cascade,
  full_name   text not null,
  dob         date,
  grade       text,
  school      text,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
alter table public.participants enable row level security;
create policy "participants: parent all" on public.participants
  for all using (parent_id = auth.uid()) with check (parent_id = auth.uid());
create policy "participants: staff read" on public.participants for select using (public.is_staff());
create trigger participants_updated before update on public.participants for each row execute function public.set_updated_at();

-- ── programs (the Leadership Academies) ──────────────────────────────────────
create table public.programs (
  id          uuid primary key default gen_random_uuid(),
  name        text not null,
  region      text check (region in ('baltimore', 'howard')),
  location    text,
  description text,
  schedule    text,
  capacity    int,
  status      text not null default 'draft' check (status in ('draft', 'open', 'closed', 'archived')),
  created_by  uuid references public.profiles(id),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
alter table public.programs enable row level security;
create policy "programs: authed read open" on public.programs
  for select using (auth.uid() is not null and (status in ('open', 'closed') or public.is_staff()));
create policy "programs: staff write" on public.programs for all using (public.is_staff()) with check (public.is_staff());
create trigger programs_updated before update on public.programs for each row execute function public.set_updated_at();

-- ── events ───────────────────────────────────────────────────────────────────
create table public.events (
  id          uuid primary key default gen_random_uuid(),
  program_id  uuid references public.programs(id) on delete set null,
  title       text not null,
  description text,
  location    text,
  address     text,
  starts_at   timestamptz,
  ends_at     timestamptz,
  capacity    int,
  status      text not null default 'draft' check (status in ('draft', 'published', 'canceled')),
  created_by  uuid references public.profiles(id),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
alter table public.events enable row level security;
create policy "events: authed read published" on public.events
  for select using (auth.uid() is not null and (status = 'published' or public.is_staff()));
create policy "events: staff write" on public.events for all using (public.is_staff()) with check (public.is_staff());
create trigger events_updated before update on public.events for each row execute function public.set_updated_at();

-- ── enrollments (participant ↔ program) ──────────────────────────────────────
create table public.enrollments (
  id              uuid primary key default gen_random_uuid(),
  participant_id  uuid not null references public.participants(id) on delete cascade,
  program_id      uuid not null references public.programs(id) on delete cascade,
  status          text not null default 'applied' check (status in ('applied', 'enrolled', 'waitlist', 'withdrawn')),
  created_at      timestamptz not null default now(),
  unique (participant_id, program_id)
);
alter table public.enrollments enable row level security;
-- A parent can see/insert/withdraw enrollments for THEIR children only.
create policy "enrollments: parent select" on public.enrollments for select
  using (exists (select 1 from public.participants p where p.id = participant_id and p.parent_id = auth.uid()));
create policy "enrollments: parent insert" on public.enrollments for insert
  with check (exists (select 1 from public.participants p where p.id = participant_id and p.parent_id = auth.uid()));
create policy "enrollments: staff all" on public.enrollments for all using (public.is_staff()) with check (public.is_staff());

-- ── event RSVPs ──────────────────────────────────────────────────────────────
create table public.event_rsvps (
  id              uuid primary key default gen_random_uuid(),
  event_id        uuid not null references public.events(id) on delete cascade,
  participant_id  uuid not null references public.participants(id) on delete cascade,
  status          text not null default 'going' check (status in ('going', 'maybe', 'declined')),
  created_at      timestamptz not null default now(),
  unique (event_id, participant_id)
);
alter table public.event_rsvps enable row level security;
create policy "rsvps: parent all" on public.event_rsvps for all
  using (exists (select 1 from public.participants p where p.id = participant_id and p.parent_id = auth.uid()))
  with check (exists (select 1 from public.participants p where p.id = participant_id and p.parent_id = auth.uid()));
create policy "rsvps: staff read" on public.event_rsvps for select using (public.is_staff());

-- ── form templates (consent, photo release, registration) ────────────────────
create table public.form_templates (
  id                 uuid primary key default gen_random_uuid(),
  key                text not null,
  title              text not null,
  version            int not null default 1,
  body               text,
  fields_json        jsonb not null default '{}'::jsonb,
  requires_signature boolean not null default true,
  active             boolean not null default true,
  created_at         timestamptz not null default now(),
  unique (key, version)
);
alter table public.form_templates enable row level security;
create policy "templates: authed read" on public.form_templates for select using (auth.uid() is not null);
create policy "templates: staff write" on public.form_templates for all using (public.is_staff()) with check (public.is_staff());

-- ── form submissions (the SIGNED, append-only record + audit trail) ──────────
create table public.form_submissions (
  id              uuid primary key default gen_random_uuid(),
  template_id     uuid not null references public.form_templates(id),
  template_version int not null,
  participant_id  uuid not null references public.participants(id) on delete cascade,
  submitted_by    uuid not null references public.profiles(id),
  data_json       jsonb not null default '{}'::jsonb,
  signer_name     text,
  signed_at       timestamptz not null default now(),
  signature_path  text,   -- Supabase Storage path (drawn signature image)
  pdf_path        text,   -- Supabase Storage path (generated signed PDF)
  ip              text,
  user_agent      text,
  content_hash    text,
  created_at      timestamptz not null default now()
);
alter table public.form_submissions enable row level security;
-- Insert + read own; NO update/delete policy → records are immutable.
create policy "submissions: parent insert" on public.form_submissions for insert
  with check (
    submitted_by = auth.uid()
    and exists (select 1 from public.participants p where p.id = participant_id and p.parent_id = auth.uid())
  );
create policy "submissions: parent read" on public.form_submissions for select
  using (exists (select 1 from public.participants p where p.id = participant_id and p.parent_id = auth.uid()));
create policy "submissions: staff read" on public.form_submissions for select using (public.is_staff());

-- ── announcements / updates ("where to go") ──────────────────────────────────
create table public.announcements (
  id          uuid primary key default gen_random_uuid(),
  scope       text not null default 'all' check (scope in ('all', 'program', 'event')),
  ref_id      uuid,
  title       text not null,
  body        text,
  created_by  uuid references public.profiles(id),
  created_at  timestamptz not null default now()
);
alter table public.announcements enable row level security;
create policy "announcements: authed read" on public.announcements for select using (auth.uid() is not null);
create policy "announcements: staff write" on public.announcements for all using (public.is_staff()) with check (public.is_staff());

-- ── keepalive (read by the scheduled keep-warm ping; prevents free-tier pause) ─
create table public.keepalive (
  id        int primary key default 1,
  pinged_at timestamptz not null default now()
);
insert into public.keepalive (id) values (1) on conflict do nothing;
alter table public.keepalive enable row level security;
create policy "keepalive: public read" on public.keepalive for select using (true);
