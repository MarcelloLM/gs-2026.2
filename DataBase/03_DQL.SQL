-- VarreSP | Três perguntas operacionais sobre a carga de demonstração.

-- 1. Quantos pedidos cada distrito registrou na semana de 22 de dezembro?
SELECT d.nome AS distrito, s.semana, s.pedidos
FROM demanda_semanal s
INNER JOIN distrito d ON d.id_distrito = s.id_distrito
WHERE s.semana = DATE '2025-12-22'
ORDER BY s.pedidos DESC, d.nome;

-- 2. Qual foi o total, a média semanal e o maior volume de cada distrito?
SELECT d.nome AS distrito,
       COUNT(*) AS semanas_observadas,
       SUM(s.pedidos) AS total_pedidos,
       ROUND(AVG(CAST(s.pedidos AS DECIMAL(12,4))), 2) AS media_semanal,
       MAX(s.pedidos) AS pico_semanal
FROM distrito d
INNER JOIN demanda_semanal s ON s.id_distrito = d.id_distrito
GROUP BY d.nome
ORDER BY total_pedidos DESC, d.nome;

-- 3. Quais distritos iniciados por L tinham previsão em 22/12?
-- O período pertence ao ON para manter o distrito sem previsão na amostra.
SELECT d.nome AS distrito,
       p.volume_previsto,
       p.prob_alta,
       CASE WHEN p.id_distrito IS NULL THEN 'SEM PREVISAO'
            ELSE 'DISPONIVEL' END AS cobertura
FROM distrito d
LEFT OUTER JOIN previsao_semanal p
    ON p.id_distrito = d.id_distrito AND p.semana = DATE '2025-12-22'
WHERE d.nome LIKE 'L%'
ORDER BY d.nome;
