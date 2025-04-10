from ttkthemes import ThemedTk
from tkinter import ttk
import tkinter as tk  # Importa tkinter come tk
from db_manager import DatabaseManager
from gui_components import create_table_window, create_insert_cliente_window
from data_operations import DataOperations

# Query predefinite (invariate)
queries = {
    "Prodotti per Categoria": """
        SELECT c.nome_categoria, p.nome_prodotto, p.prezzo, p.quantita_stock, f.nome_fornitore
        FROM prodotti p
        JOIN categorie c ON p.id_categoria = c.id_categoria
        JOIN fornitori f ON p.id_fornitore = f.id_fornitore
        ORDER BY c.nome_categoria, p.nome_prodotto
    """,
    "Totale Vendite per Categoria": """
        SELECT c.nome_categoria, COUNT(DISTINCT o.id_ordine) AS numero_ordini, SUM(d.quantita * d.prezzo_unitario) AS totale_vendite
        FROM categorie c
        JOIN prodotti p ON c.id_categoria = p.id_categoria
        JOIN dettagli_ordini d ON p.id_prodotto = d.id_prodotto
        JOIN ordini o ON d.id_ordine = o.id_ordine
        GROUP BY c.nome_categoria
        HAVING totale_vendite > 50
    """,
    "Clienti con Ordini Non Pagati": """
        SELECT CONCAT(cl.nome, ' ', cl.cognome) AS cliente, o.id_ordine, o.data_ordine, o.totale
        FROM clienti cl
        JOIN ordini o ON cl.id_cliente = o.id_cliente
        LEFT JOIN pagamenti p ON o.id_ordine = p.id_ordine
        WHERE p.id_pagamento IS NULL
    """,
    "Prodotti con Stock Basso": """
        SELECT p.nome_prodotto, p.quantita_stock, f.nome_fornitore, f.telefono
        FROM prodotti p
        JOIN fornitori f ON p.id_fornitore = f.id_fornitore
        WHERE p.quantita_stock < 10
    """,
    "Media Prezzo per Categoria": """
        SELECT c.nome_categoria, AVG(p.prezzo) AS prezzo_medio, COUNT(p.id_prodotto) AS numero_prodotti
        FROM categorie c
        LEFT JOIN prodotti p ON c.id_categoria = p.id_categoria
        GROUP BY c.nome_categoria
    """,
    "Clienti Sopra la Media": """
        SELECT CONCAT(c.nome, ' ', c.cognome) AS cliente, SUM(o.totale) AS spesa_totale
        FROM clienti c
        JOIN ordini o ON c.id_cliente = o.id_cliente
        GROUP BY c.id_cliente, c.nome, c.cognome
        HAVING SUM(o.totale) > (SELECT AVG(totale) FROM ordini WHERE totale IS NOT NULL)
    """,
    "Prodotti Più Venduti": """
        SELECT c.nome_categoria, p.nome_prodotto, SUM(d.quantita) AS quantita_venduta
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
        GROUP BY c.nome_categoria, p.nome_prodotto
    """,
    "Ordini Sopra Massimo Pagamento": """
        SELECT o.id_ordine, o.data_ordine, o.totale
        FROM ordini o
        WHERE o.totale > (
            SELECT MAX(p.importo)
            FROM pagamenti p
            WHERE DATE_FORMAT(p.data_pagamento, '%Y-%m') = DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m')
        )
    """,
    "Stato Stock Prodotti": """
        SELECT p.nome_prodotto, p.quantita_stock,
               CASE 
                   WHEN p.quantita_stock > 50 THEN 'Alto'
                   WHEN p.quantita_stock BETWEEN 10 AND 50 THEN 'Medio'
                   ELSE 'Basso'
               END AS stato_stock
        FROM prodotti p
        ORDER BY p.quantita_stock DESC
    """,
    "Riepilogo Ordini": """
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
        GROUP BY o.id_ordine, c.nome, c.cognome, p.importo
    """
}

# Inizializzazione
db_manager = DatabaseManager()
data_ops = DataOperations(db_manager)

# Creazione della vista (invariata)
db_manager.execute_query("""
    CREATE OR REPLACE VIEW riepilogo_ordini AS
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
    GROUP BY o.id_ordine, c.nome, c.cognome, p.importo
""")

# Interfaccia principale
root = ThemedTk(theme="radiance")
root.title("Negozio - Gestione e Analisi Dati")
root.geometry("800x600")  # Dimensioni finestra

# Stile per i pulsanti (invariato)
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding=5)

# Frame contenitore principale
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Frame per "Analisi Dati" (sinistra)
query_frame = ttk.LabelFrame(main_frame, text="Analisi Dati", padding=10)
query_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

query_canvas = tk.Canvas(query_frame)
query_scrollbar = ttk.Scrollbar(query_frame, orient="vertical", command=query_canvas.yview)
query_inner_frame = ttk.Frame(query_canvas)

query_canvas.pack(side=tk.LEFT, fill=tk.Y)
query_canvas.configure(yscrollcommand=query_scrollbar.set)
query_canvas.create_window((0, 0), window=query_inner_frame, anchor="nw")

# Aggiunta dei pulsanti per le query
row = 0
for title, query in queries.items():
    ttk.Button(query_inner_frame, text=title, command=lambda q=query, t=title: create_table_window(q, t, db_manager)).grid(row=row, column=0, pady=5, sticky="ew")
    row += 1

# Configurazione dinamica dello scrollbar per "Analisi Dati"
query_inner_frame.update_idletasks()
canvas_height = query_canvas.winfo_height() or 600  # Altezza canvas o default
content_height = query_inner_frame.winfo_reqheight()
if content_height > canvas_height:
    query_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    query_canvas.config(scrollregion=(0, 0, query_inner_frame.winfo_reqwidth(), content_height))
else:
    query_canvas.config(scrollregion=(0, 0, query_inner_frame.winfo_reqwidth(), content_height))

query_canvas.config(width=query_inner_frame.winfo_reqwidth())

# Frame per "Gestione Dati" (destra)
manage_frame = ttk.LabelFrame(main_frame, text="Gestione Dati", padding=10)
manage_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

manage_canvas = tk.Canvas(manage_frame)
manage_scrollbar = ttk.Scrollbar(manage_frame, orient="vertical", command=manage_canvas.yview)
manage_inner_frame = ttk.Frame(manage_canvas)

manage_canvas.pack(side=tk.LEFT, fill=tk.Y)
manage_canvas.configure(yscrollcommand=manage_scrollbar.set)
manage_canvas.create_window((0, 0), window=manage_inner_frame, anchor="nw")

# Aggiunta dei pulsanti per la gestione
ttk.Button(manage_inner_frame, text="Inserisci Cliente", command=lambda: create_insert_cliente_window(db_manager)).pack(pady=5, fill=tk.X)
ttk.Button(manage_inner_frame, text="Inserisci Dati Casuali", command=lambda: data_ops.insert_random_data(parent=root)).pack(pady=5, fill=tk.X)
ttk.Button(manage_inner_frame, text="Cancella Tutto", command=lambda: data_ops.delete_all_data(parent=root)).pack(pady=5, fill=tk.X)

# Configurazione dinamica dello scrollbar per "Gestione Dati"
manage_inner_frame.update_idletasks()
canvas_height = manage_canvas.winfo_height() or 600  # Altezza canvas o default
content_height = manage_inner_frame.winfo_reqheight()
if content_height > canvas_height:
    manage_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    manage_canvas.config(scrollregion=(0, 0, manage_inner_frame.winfo_reqwidth(), content_height))
else:
    manage_canvas.config(scrollregion=(0, 0, manage_inner_frame.winfo_reqwidth(), content_height))

manage_canvas.config(width=manage_inner_frame.winfo_reqwidth())

root.mainloop()