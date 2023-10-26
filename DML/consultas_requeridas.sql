-- Plantear al menos 3 consultas en las que se utilicen
-- operaciones avanzadas (Join, exist, in, etc.)
-- 1) Número de proteína por especie.
SELECT COUNT(prot.*) AS cnt, esp.Nombre
 FROM proteina as prot
 JOIN especie as esp
	ON esp.id_especie = prot.id_especie
GROUP BY esp.Nombre
ORDER BY cnt DESC;

-- 2) Mostrar la proteína que esta en todas las especies.
SELECT DISTINCT prot.uniprotid
FROM proteina as prot
WHERE NOT EXISTS (
    SELECT esp.id_especie
    FROM especie as esp
    WHERE NOT EXISTS (SELECT *
        FROM proteina as prot2
        WHERE esp.id_especie = prot2.id_especie AND 
			  prot.uniprotid = prot2.uniprotid));
		
-- 3) Encontrar el titulo de la/s referencia/s que describe la única proteína 
-- que se tiene registro en Danio rerio
SELECT rf.titulo
FROM referencia as rf
JOIN (SELECT prot.uniprotid, prot.id_proteina
		FROM proteina as prot
		JOIN (SELECT esp.id_especie
				FROM especie as esp
				WHERE esp.Nombre = 'Danio rerio') as A
			ON prot.id_especie = A.id_especie) as B
	ON rf.id_proteina = B.id_proteina;

-- Crear una consulta que utilice tres tablas, contenga una condición
-- de igualdad y una condición de rango (>, >=, <, <=, between). Escribir
-- el árbol de ejecución de la consulta en álgebra relacional y luego
-- optimizarlo. Luego escribir la nueva consulta SQL optimizado

-- No optimizada:
SELECT prot.descripcion as Nombre, sec.secuencia as Secuencia
FROM proteina as prot
	JOIN secuencia as sec
		ON sec.id_proteina = prot.id_proteina
	JOIN especie as esp
		ON prot.id_especie = esp.id_especie
WHERE esp.taxId = 9606 AND prot.pi BETWEEN 6.4 AND 13.2;

-- Optimizada:
SELECT prot.descripcion as Nombre, sec.secuencia as Secuencia
FROM (
	SELECT esp.id_especie
	FROM especie as esp
	WHERE esp.taxid = 9606
) as A
JOIN (
	SELECT prot.descripcion, sec.secuencia, prot.id_especie
	FROM (
		SELECT prot.id_proteina, prot.descripcion, prot.id_especie
		FROM proteina as prot
		WHERE prot.pi BETWEEN 6.4 AND 13.2
	) as B
	JOIN (
		SELECT sec.secuencia, sec.id_proteina
		FROM secuencia as sec
	) as C
		ON C.id_proteina = B.id_proteina
) as D
ON A.id_especie = D.id_especie;