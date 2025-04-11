# Negozio - Sistema di Gestione e Analisi per un E-Commerce

Python
MySQL
Tkinter
License
Negozio è un progetto che simula la gestione e l'analisi dati di un negozio online, progettato per dimostrare competenze avanzate come SQL Developer e Data Analyst. Combina un database relazionale MySQL con un'interfaccia grafica Python (Tkinter) per interagire con i dati in modo intuitivo.
Scopo del Progetto
Progettazione Database: Creazione di uno schema relazionale per gestire fornitori, prodotti, clienti, ordini e pagamenti.

Analisi Dati: Query SQL avanzate per estrarre insight aziendali (es. prodotti più venduti, stock basso).

Interfaccia Utente: GUI per visualizzare, modificare e inserire dati senza bisogno di strumenti esterni.

Portfolio: Progetto professionale per il CV, che evidenzia competenze tecniche e analitiche.

Tecnologie Utilizzate
MySQL: Database relazionale per la gestione dei dati.

Python: Logica di backend e GUI (mysql-connector-python, tkinter, ttkthemes).

Git: Versionamento del codice su GitHub.

Struttura del Database
Il database negozio include le seguenti tabelle:
fornitori: Informazioni sui fornitori (es. nome, email).

categorie: Classificazioni dei prodotti (es. Elettronica, Abbigliamento).

prodotti: Dettagli dei prodotti (es. prezzo, stock).

clienti: Dati dei clienti (es. nome, email).

ordini e dettagli_ordini: Informazioni sulle vendite.

pagamenti: Registrazione dei pagamenti.

Schema Relazionale:
Relazioni uno-a-molti (es. fornitori → prodotti) e molti-a-molti (tramite dettagli_ordini).

Vincoli di integrità (chiavi primarie, esterne, valori di default).

Funzionalità Principali
Gestione Database:
Schema relazionale con vincoli per garantire l'integrità dei dati.

Dati di esempio realistici per testare il sistema.

Analisi Dati:
Query per analisi aziendali, come:
Prodotti con stock basso.

Clienti con ordini non pagati.

Vendite per categoria.

Clienti con spesa sopra la media.

Vista SQL (riepilogo_ordini) per riepiloghi chiari.

Interfaccia Grafica:
Tabelle interattive per visualizzare i risultati delle query.

Funzionalità di modifica, rimozione e inserimento (es. nuovi clienti).

Inserimento dati casuali per test rapidi.

Automazione:
Script Python per gestire il database e generare dati.

Struttura della Repository

negozio-analysis/
├── create_database.sql  # Schema del database
├── insert_data.sql     # Dati di esempio
├── db_manager.py       # Gestione della connessione al database
├── data_operations.py  # Operazioni di inserimento e cancellazione
├── gui_components.py   # Componenti dell'interfaccia grafica
├── main.py            # Applicazione principale
├── requirements.txt   # Dipendenze Python
├── README.md         # Documentazione del progetto
└── LICENSE           # Licenza MIT

Installazione e Configurazione
Prerequisiti
MySQL 8.0+ installato e in esecuzione.

Python 3.8+ con le seguenti librerie:
bash

pip install -r requirements.txt

(Include mysql-connector-python e ttkthemes).

Configurazione del Database
Puoi scegliere tra due approcci per inizializzare il database:
Manuale (raccomandato per personalizzazioni):
Esegui i file SQL per creare e popolare il database negozio:
bash

mysql -u root -p < create_database.sql
mysql -u root -p < insert_data.sql

Questi file offrono flessibilità per usare il DBMS preferito (es. MySQL, MariaDB).

Diretto tramite Python:
Configura le credenziali del database in db_manager.py (host, user, password).

Avvia main.py, che si collegherà al database esistente.

Esecuzione
Dopo aver configurato il database, esegui:
bash

python main.py

Utilizzo
Analisi Dati:
Dalla GUI, seleziona una query (es. "Prodotti Più Venduti") per visualizzare i risultati in una tabella interattiva.

Gestione Dati:
Inserisci nuovi clienti tramite il form dedicato.

Aggiungi dati casuali per test con un clic.

Modifica o rimuovi record direttamente dalle tabelle.

Cancellazione:
Usa l'opzione "Cancella Tutto" per svuotare il database (con conferma).

Esempi di Query
Prodotti con Stock Basso
sql

SELECT p.nome_prodotto, p.quantita_stock, f.nome_fornitore
FROM prodotti p
JOIN fornitori f ON p.id_fornitore = f.id_fornitore
WHERE p.quantita_stock < 10;

Clienti Sopra la Media
sql

SELECT CONCAT(c.nome, ' ', c.cognome) AS cliente, SUM(o.totale) AS spesa_totale
FROM clienti c
JOIN ordini o ON c.id_cliente = o.id_cliente
GROUP BY c.id_cliente, c.nome, c.cognome
HAVING SUM(o.totale) > (SELECT AVG(totale) FROM ordini WHERE totale IS NOT NULL);

Vista Riepilogo Ordini
sql

SELECT o.id_ordine, CONCAT(c.nome, ' ', c.cognome) AS cliente, SUM(d.quantita * d.prezzo_unitario) AS totale_calcolato,
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

Competenze Dimostrate
SQL:
Progettazione di database relazionali con vincoli.

Query avanzate (join, aggregazioni, sottoquery, viste).

Python:
Creazione di GUI interattive con Tkinter.

Automazione di operazioni sul database.

Gestione delle connessioni e degli errori.

Analisi Dati:
Estrazione di insight utili per decisioni aziendali.

Best Practices:
Codice modulare e organizzato.

Documentazione chiara per gli utenti.

Miglioramenti Futuri
Aggiunta di trigger SQL per aggiornare automaticamente lo stock.

Export dei risultati in CSV per analisi esterne.

Visualizzazioni grafiche (es. Matplotlib per grafici di vendita).

Supporto per altri DBMS (es. PostgreSQL).

