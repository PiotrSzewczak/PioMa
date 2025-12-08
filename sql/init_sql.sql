create schema  pioma_proj

create table pioma_proj.apartments 
(
id serial primary key ,
street text,
house_nr text,
city text,
full_address text,
longitude float,
latitude float
)


INSERT INTO pioma_proj.apartments (
    street,
    house_nr,
    city,
    full_address,
    longitude,
    latitude
) VALUES (
    'Marszałkowska',
    '12A',
    'Warszawa',
    'Marszałkowska 12A, Warszawa',
    21.0122287,
    52.2296756
);
