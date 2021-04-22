-- https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING
-- https://www.postgresql.org/docs/current/indexes-expressional.html
-- https://www.postgresql.org/docs/13/functions-json.html
-- https://www.postgresql.org/docs/12/functions-json.html

create temp table target(data jsonb);
copy target from '/playground/data.json';

select * from target;

-- Index
create index idx_gin_target on target using gin (data jsonb_ops);
create index idx_gin_path_target on target using gin (data jsonb_path_ops);

-- Nested index
create index idx_gin_path_target_cars on target using gin ((data -> 'cars') jsonb_ops);

-- After indexing, the queries 'where' will be faster
select count(*) from target where data @@ '$.age[0] > 50';
select * from target where data ->> 'name' = 'Riddle Mercado';

-- Selection
select data -> 'age' from target;
select data #> '{cars, 0}' from target;

-- Queries by jsonpath (must evaluate to boolean)
select data @@ '$.age[0] > 50' from target;
select data @@ '$.age[*] > 50' from target;

-- jsonpath existence
select data @? '$.cars[2]' from target;

-- Exists
select data ? 'age' from target;
select data ?& '{age, nonexisting}' from target;
select data ?| '{age, nonexisting}' from target;
select data @> '{"age": 40}' from target;

-- Deletion operator (jsonb object without the column)
select data - 'age' from target;

-- Select of an updated jsonb entry (does not change the database)
-- arguments of jsonb_set must be strings
select jsonb_set(data, '{age}', '50') from target where data ->> 'name' = 'Riddle Mercado';

-- Insert simple (invalid in out DB)
insert into target values('{age: 50}'::jsonb );

-- Delete from database
delete from target where data @@ '$.age[0] > 80';

-- Update of an entry
update target set data = jsonb_set(data, '{age}', '50') where data ->> 'name' = 'Riddle Mercado';
