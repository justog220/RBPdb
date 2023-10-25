-- Plantear al menos 3 consultas en las que se utilicen
-- operaciones avanzadas (Join, exist, in, etc.)
-- 1)

-- 2)

-- 3)

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