-- Creazione del database
CREATE DATABASE IF NOT EXISTS negozio;
USE negozio;

-- Tabella Fornitori
CREATE TABLE fornitori (
    id_fornitore INT PRIMARY KEY AUTO_INCREMENT,
    nome_fornitore VARCHAR(100) NOT NULL,
    indirizzo VARCHAR(150),
    telefono VARCHAR(15),
    email VARCHAR(100) UNIQUE
);

-- Tabella Categorie
CREATE TABLE categorie (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nome_categoria VARCHAR(50) NOT NULL,
    descrizione TEXT
);

-- Tabella Prodotti
CREATE TABLE prodotti (
    id_prodotto INT PRIMARY KEY AUTO_INCREMENT,
    nome_prodotto VARCHAR(100) NOT NULL,
    id_categoria INT,
    id_fornitore INT,
    prezzo DECIMAL(10, 2) NOT NULL,
    quantita_stock INT NOT NULL DEFAULT 0,
    data_aggiunta DATE,
    FOREIGN KEY (id_categoria) REFERENCES categorie(id_categoria),
    FOREIGN KEY (id_fornitore) REFERENCES fornitori(id_fornitore)
);

-- Tabella Clienti
CREATE TABLE clienti (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(15),
    data_registrazione DATE DEFAULT '2025-01-01'
);

-- Tabella Ordini
CREATE TABLE ordini (
    id_ordine INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    data_ordine DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    stato_ordine VARCHAR(20) DEFAULT 'In Attesa',
    totale DECIMAL(10, 2),
    FOREIGN KEY (id_cliente) REFERENCES clienti(id_cliente)
);

-- Tabella Dettagli_Ordini
CREATE TABLE dettagli_ordini (
    id_dettaglio INT PRIMARY KEY AUTO_INCREMENT,
    id_ordine INT,
    id_prodotto INT,
    quantita INT NOT NULL,
    prezzo_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_ordine) REFERENCES ordini(id_ordine),
    FOREIGN KEY (id_prodotto) REFERENCES prodotti(id_prodotto)
);

-- Tabella Pagamenti
CREATE TABLE pagamenti (
    id_pagamento INT PRIMARY KEY AUTO_INCREMENT,
    id_ordine INT,
    importo DECIMAL(10, 2) NOT NULL,
    data_pagamento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metodo_pagamento VARCHAR(30),
    FOREIGN KEY (id_ordine) REFERENCES ordini(id_ordine)
);