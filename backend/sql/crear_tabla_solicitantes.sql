create table if not exists solicitantes (
    nombre varchar(100) not null,
    identificacion varchar(20) primary key not null,
    fecha_nacimiento date not null,
    edad int not null
);