USE negozio;

-- 1. Elenco prodotti per categoria con fornitore
SELECT 
    c.nome_categoria,
    p.nome_prodotto,
    p.prezzo,
    p.quantita_stock,
    f.nome_fornitore
FROM prodotti p
JOIN categorie c ON p.id_categoria = c.id_categoria
JOIN fornitori f ON p.id_fornitore = f.id_fornitore
ORDER BY c.nome_categoria, p.nome_prodotto;

-- 2. Totale vendite per categoria con numero ordini
SELECT 
    c.nome_categoria,
    COUNT(DISTINCT o.id_ordine) AS numero_ordini,
    SUM(d.quantita * d.prezzo_unitario) AS totale_vendite
FROM categorie c
JOIN prodotti p ON c.id_categoria = p.id_categoria
JOIN dettagli_ordini d ON p.id_prodotto = d.id_prodotto
JOIN ordini o ON d.id_ordine = o.id_ordine
GROUP BY c.nome_categoria
HAVING totale_vendite > 50;

-- 3. Clienti con ordini non pagati
SELECT 
    CONCAT(cl.nome, ' ', cl.cognome) AS cliente,
    o.id_ordine,
    o.data_ordine,
    o.totale
FROM clienti cl
JOIN ordini o ON cl.id_cliente = o.id_cliente
LEFT JOIN pagamenti p ON o.id_ordine = p.id_ordine
WHERE p.id_pagamento IS NULL;

-- 4. Prodotti con stock basso (<10) e fornitore
SELECT 
    p.nome_prodotto,
    p.quantita_stock,
    f.nome_fornitore,
    f.telefono
FROM prodotti p
JOIN fornitori f ON p.id_fornitore = f.id_fornitore
WHERE p.quantita_stock < 10;

-- 5. Media prezzo prodotti per categoria
SELECT 
    c.nome_categoria,
    AVG(p.prezzo) AS prezzo_medio,
    COUNT(p.id_prodotto) AS numero_prodotti
FROM categorie c
LEFT JOIN prodotti p ON c.id_categoria = p.id_categoria
GROUP BY c.nome_categoria;

-- 6. Sottoquery: Clienti che hanno speso più della media
SELECT 
    CONCAT(c.nome, ' ', c.cognome) AS cliente,
    SUM(o.totale) AS spesa_totale
FROM clienti c
JOIN ordini o ON c.id_cliente = o.id_cliente
GROUP BY c.id_cliente, c.nome, c.cognome
HAVING SUM(o.totale) > (SELECT AVG(totale) FROM ordini WHERE totale IS NOT NULL);

-- 7. Sottoquery: Prodotti più venduti per categoria
SELECT 
    c.nome_categoria,
    p.nome_prodotto,
    SUM(d.quantita) AS quantita_venduta
FROM categorie c
JOIN prodotti p ON c.id_categoria = p.id_categoria
JOIN dettagli_ordini d ON p.id_prodotto = d.id_prodotto
WHERE p.id_prodotto IN (
    SELECT d2.id_prodotto
    FROM dettagli_ordini d2
    GROUP BY d2.id_prodotto
    ORDER BY SUM(d2.quantita) DESC
    LIMIT 5
)
GROUP BY c.nome_categoria, p.nome_prodotto;

-- 8. Sottoquery annidata: Ordini con importo superiore al massimo pagamento del mese precedente
SELECT 
    o.id_ordine,
    o.data_ordine,
    o.totale
FROM ordini o
WHERE o.totale > (
    SELECT MAX(p.importo)
    FROM pagamenti p
    WHERE DATE_FORMAT(p.data_pagamento, '%Y-%m') = DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m')
);

-- 9. Query con CASE: Stato stock prodotti
SELECT 
    p.nome_prodotto,
    p.quantita_stock,
    CASE 
        WHEN p.quantita_stock > 50 THEN 'Alto'
        WHEN p.quantita_stock BETWEEN 10 AND 50 THEN 'Medio'
        ELSE 'Basso'
    END AS stato_stock
FROM prodotti p
ORDER BY p.quantita_stock DESC;

-- 10. Vista: Riepilogo ordini con stato pagamento
CREATE VIEW riepilogo_ordini AS
SELECT 
    o.id_ordre,
    CONCAT(c.nome, ' ', c.cognome) AS cliente,
    SUM(d.quantita * d.prezzo_unitario) AS totale_calcolato,
    p.importo AS totale_pagato,
    CASE 
        WHEN p.id_pagamento IS NOT NULL THEN 'Pagato'
        ELSE 'Non Pagato'
    END AS stato_pagamento
FROM ordini o
JOIN clienti c ON o.id_cliente = c.id_cliente
JOIN dettagli_ordini d ON o.id_ordine = d.id_ordine
LEFT JOIN pagamenti p ON o.id_ordine = p.id_ordine
GROUP BY o.id_ordine, c.nome, c.cognome, p.importo;