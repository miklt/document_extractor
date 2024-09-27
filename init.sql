create database temp_i
with
    owner user_temp;

create table
    public.prompts (
        id integer generated always as identity constraint prompts_pk primary key,
        prompt_recibo_acessorio text,
        prompt_recibo_principal text,
        data_alteracao timestamp default now () not null
    );

alter table public.prompts owner to user_temp;

create table
    public.documentos (
        id integer generated always as identity constraint documentos_pk primary key,
        representacao_json jsonb,
        cnpj text,
        data_hora_entrega text,
        hash_arquivo text,
        inscricao text,
        protocolo text,
        tipo_entrega text,
        validacao text
    );

alter table public.documentos owner to user_temp;