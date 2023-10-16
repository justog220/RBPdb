CREATE VIEW vista_recuento_entradas AS
SELECT
    (SELECT COUNT(*) FROM proteina) AS proteina_count,
    (SELECT COUNT(*) FROM secuencia) AS secuencia_count,
    (SELECT COUNT(*) FROM especie) AS especie_count,
    (SELECT COUNT(*) FROM gen) AS gen_count,
    (SELECT COUNT(*) FROM referencia) AS referencia_count;
