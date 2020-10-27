create table expense(
    id serial primary key,
    author varchar,
    created_at datetime default current_timestamp,
    amount money not null,
    category varchar not null,
    comment text,
)