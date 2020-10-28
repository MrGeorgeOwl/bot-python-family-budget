create table expense(
    id serial primary key,
    author varchar,
    created_at timestamp default current_timestamp,
    amount numeric(10, 2) not null,
    category varchar not null,
    comment text
)