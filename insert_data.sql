USE negozio;

-- Dati per Fornitori
INSERT INTO fornitori (nome_fornitore, indirizzo, telefono, email) VALUES
('TechWorld', 'Via Roma 1, Milano', '3331234567', 'techworld@email.com'),
('Moda SRL', 'Via Verdi 10, Roma', '3459876543', 'moda@email.com'),
('Elettra SPA', 'Via Dante 5, Torino', '3204567890', 'elettra@email.com');

-- Dati per Categorie
INSERT INTO categorie (nome_categoria, descrizione) VALUES
('Elettronica', 'Dispositivi tecnologici e accessori'),
('Abbigliamento', 'Vestiti e accessori di moda'),
('Casa', 'Arredamento e utensili domestici');

-- Dati per Prodotti
INSERT INTO prodotti (nome_prodotto, id_categoria, id_fornitore, prezzo, quantita_stock, data_aggiunta) VALUES
('Smartphone XYZ', 1, 1, 299.99, 50, '2025-01-15'),
('T-Shirt Casual', 2, 2, 19.99, 100, '2025-02-01'),
('Cuffie Wireless', 1, 1, 49.99, 30, '2025-03-10'),
('Lampada LED', 3, 3, 25.00, 20, '2025-04-01'),
('Jeans Slim', 2, 2, 39.99, 80, '2025-02-15');

-- Dati per Clienti
INSERT INTO clienti (nome, cognome, email, telefono) VALUES
('Anna', 'Verdi', 'anna.verdi@email.com', '3334567890'),
('Luca', 'Bianchi', 'luca.bianchi@email.com', '3456789012'),
('Maria', 'Rossi', 'maria.rossi@email.com', '3201234567');

-- Dati per Ordini
INSERT INTO ordini (id_cliente, data_ordine, stato_ordine, totale) VALUES
(1, '2025-04-10 10:30:00', 'Completato', 319.98),
(2, '2025-04-11 15:00:00', 'In Attesa', 49.99),
(3, '2025-04-12 09:15:00', 'Spedito', 64.99);

-- Dati per Dettagli_Ordini
INSERT INTO dettagli_ordini (id_ordine, id_prodotto, quantita, prezzo_unitario) VALUES
(1, 1, 1, 299.99), -- Smartphone
(1, 2, 1, 19.99),  -- T-Shirt
(2, 3, 1, 49.99),  -- Cuffie
(3, 4, 1, 25.00),  -- Lampada
(3, 5, 1, 39.99);  -- Jeans

-- Dati per Pagamenti
INSERT INTO pagamenti (id_ordine, importo, data_pagamento, metodo_pagamento) VALUES
(1, 319.98, '2025-04-10 11:00:00', 'Carta di Credito'),
(3, 64.99, '2025-04-12 10:00:00', 'PayPal');