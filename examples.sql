-- https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING
-- https://www.postgresql.org/docs/current/indexes-expressional.html
-- https://www.postgresql.org/docs/13/functions-json.html
-- https://www.postgresql.org/docs/12/functions-json.html

create temp table person(data jsonb);
copy person from '/playground/data.json';

select * from person;

-- Index
create index idx_gin_person on person using gin (data jsonb_ops);
create index idx_gin_path_person on person using gin (data jsonb_path_ops);

-- Nested index
create index idx_gin_path_person_cars on person using gin ((data -> 'cars') jsonb_ops);

-- After indexing, the queries 'where' will be faster
select count(*) from person where data @@ '$.age[0] > 50';
select * from person where data ->> 'name' = 'Riddle Mercado';

-- Selection
select data -> 'age' from person;
select data #> '{cars, 0}' from person;

-- Unnest arrays
select jsonb_array_elements(data -> 'cars') from person;

-- Name | Age | Car
select data ->> 'name' as name, data ->> 'age' as age, jsonb_array_elements(data -> 'cars') as car from person;
select data ->> 'name' as name, data ->> 'age' as age, jsonb_array_elements(data -> 'cars') -> 'license_plate' as license_plate from person;

-- Complex query using join
select * from (select
  person.data ->> 'name' as name,
  person.data ->> 'age' as age,
  jsonb_array_elements(person.data -> 'cars') -> 'license_plate' as license_plate
  from person
) as t -- t is a required alias, it is not used anywhere
inner join speed_violation on license_plate = speed_violation.data -> 'license_plate'
where (speed_violation.data -> 'actual_speed')::int > 100;

-- Queries by jsonpath (must evaluate to boolean)
select data @@ '$.age[0] > 50' from person;
select data @@ '$.age[*] > 50' from person;

-- jsonpath existence
select data @? '$.cars[2]' from person;

-- Exists
select data ? 'age' from person;
select data ?& '{age, nonexisting}' from person;
select data ?| '{age, nonexisting}' from person;
select data @> '{"age": 40}' from person;

-- Deletion operator (jsonb object without the column)
select data - 'age' from person;

-- Select of an updated jsonb entry (does not change the database)
-- arguments of jsonb_set must be strings
select jsonb_set(data, '{age}', '50') from person where data ->> 'name' = 'Riddle Mercado';

-- Insert simple (invalid in out DB)
insert into person values('{age: 50}'::jsonb);

-- Delete from database
delete from person where data @@ '$.age[0] > 80';

-- Update of an entry
update person set data = jsonb_set(data, '{age}', '50') where data ->> 'name' = 'Riddle Mercado';

-- Super complex "query", update nested attribute
create temp table t as
select id, jsonb_array_elements(data -> 'pets') as pets from person where data @@ '$.pets[*].age > 14';

update t set pets = jsonb_set(pets, '{age}', ((pets -> 'age')::int + 1)::text::jsonb)
where pets @@ '$.age > 14';

with new_pets as (
    select id, jsonb_agg(pets) as pets from t group by(id)
)

update person
set data = jsonb_set(person.data, '{pets}', new_pets.pets)
from person p inner join new_pets on p.id = new_pets.id
where person.id = new_pets.id;
--- end of super complex query
