CREATE TABLE proteina (
    id_proteina SERIAL,
    PRIMARY KEY (id_proteina),
    uniProtID VARCHAR(15),
    descripcion VARCHAR(100),
    dominios VARCHAR(100),
    pI NUMERIC(5,3),
    pesoMol NUMERIC(10, 2),
    fraccionHelice NUMERIC(5,2),
    fraccionGiro NUMERIC(4,2),
    fraccionHoja NUMERIC(4,2),
    id_especie INT
);

CREATE TABLE secuencia (
    id_secuencia SERIAL,
    PRIMARY KEY (id_secuencia),
    secuencia TEXT NOT NULL,
    largo INT NOT NULL,
    id_proteina INT
);

ALTER TABLE secuencia ADD CONSTRAINT
    prot_sec_fk FOREIGN KEY
    (id_proteina) REFERENCES proteina
    (id_proteina);

CREATE TABLE especie (
    id_especie SERIAL,
    PRIMARY KEY (id_especie),
    taxId INT,
    nombre VARCHAR(30),
    id_proteina INT
);

ALTER TABLE especie ADD CONSTRAINT
    prot_especie_fk FOREIGN KEY
    (id_proteina) REFERENCES proteina
    (id_proteina);

CREATE TABLE gen (
    id_gen SERIAL,
    PRIMARY KEY (id_gen),
    nombre VARCHAR(25),
    id_proteina INT
);

ALTER TABLE gen ADD CONSTRAINT
    prot_gen_fk FOREIGN KEY
    (id_proteina) REFERENCES proteina
    (id_proteina);

CREATE TABLE referencia (
    id_referencia SERIAL,
    PRIMARY KEY (id_referencia),
    anio INT,
    titulo VARCHAR(200),
    id_proteina INT
);

ALTER TABLE referencia ADD CONSTRAINT
    prot_ref_fk FOREIGN KEY
    (id_proteina) REFERENCES proteina
    (id_proteina);

CREATE TABLE autor (
    id_autor SERIAL,
    PRIMARY KEY (id_autor),
    nombre VARCHAR(50)
);

CREATE TABLE ref_tiene_autor (
    id_autor INT,
    id_referencia INT
);

ALTER TABLE ref_tiene_autor ADD CONSTRAINT
    ref_tiene_autor_ref_fk FOREIGN KEY
    (id_referencia) REFERENCES referencia
    (id_referencia);

ALTER TABLE ref_tiene_autor ADD CONSTRAINT
    ref_tiene_autor_autor_fk FOREIGN KEY
    (id_autor) REFERENCES autor
    (id_autor);

-- TODO: definir los tamaños que tendra cada varchar