create table if not exists viviendas (
    ciudad varchar(100) not null,
    barrio varchar(100) not null,
    direccion varchar(200) not null,
    identificacion_propietario varchar(20) not null,
    valor decimal(15,2) not null,
    primary key (direccion),
    foreign key (identificacion_propietario) references solicitantes(identificacion)
);