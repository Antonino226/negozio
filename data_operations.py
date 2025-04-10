import random
from datetime import datetime, timedelta
from tkinter import messagebox

class DataOperations:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def insert_random_data(self, parent=None):
        conn = self.db_manager.connect()
        if not conn:
            return
        
        cursor = conn.cursor()
        try:
            nomi = ["Mario", "Laura", "Giulia", "Paolo"]
            cognomi = ["Rossi", "Bianchi", "Verdi", "Neri"]
            nome = random.choice(nomi)
            cognome = random.choice(cognomi)
            email = f"{nome.lower()}.{cognome.lower()}@email.com"
            telefono = f"3{random.randint(20, 49)}{random.randint(1000000, 9999999)}"
            query_cliente = "INSERT INTO clienti (nome, cognome, email, telefono, data_registrazione) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query_cliente, (nome, cognome, email, telefono, datetime.now().date()))
            
            cursor.execute("SELECT id_cliente FROM clienti ORDER BY id_cliente DESC LIMIT 1")
            id_cliente = cursor.fetchone()[0]
            totale = random.uniform(10, 500)
            query_ordine = "INSERT INTO ordini (id_cliente, data_ordine, stato_ordine, totale) VALUES (%s, %s, %s, %s)"
            cursor.execute(query_ordine, (id_cliente, datetime.now(), random.choice(["In Attesa", "Completato"]), totale))
            
            cursor.execute("SELECT id_ordine FROM ordini ORDER BY id_ordine DESC LIMIT 1")
            id_ordine = cursor.fetchone()[0]
            cursor.execute("SELECT id_prodotto, prezzo FROM prodotti ORDER BY RAND() LIMIT 1")
            id_prodotto, prezzo = cursor.fetchone()
            query_dettaglio = "INSERT INTO dettagli_ordini (id_ordine, id_prodotto, quantita, prezzo_unitario) VALUES (%s, %s, %s, %s)"
            cursor.execute(query_dettaglio, (id_ordine, id_prodotto, random.randint(1, 5), prezzo))
            
            conn.commit()
            messagebox.showinfo("Successo", "Dati casuali inseriti!", parent=parent)
        except mysql.connector.Error as err:
            messagebox.showerror("Errore", f"Errore: {err}", parent=parent)
        finally:
            conn.close()

    def delete_all_data(self, parent=None):
        from tkinter import messagebox
        if messagebox.askyesno("Conferma", "Vuoi cancellare tutti i dati?", parent=parent):
            queries = [
                "DELETE FROM pagamenti",
                "DELETE FROM dettagli_ordini",
                "DELETE FROM ordini",
                "DELETE FROM clienti",
                "DELETE FROM prodotti",
                "DELETE FROM categorie",
                "DELETE FROM fornitori"
            ]
            conn = self.db_manager.connect()
            if conn:
                cursor = conn.cursor()
                try:
                    for query in queries:
                        cursor.execute(query)
                    conn.commit()
                    messagebox.showinfo("Successo", "Tutti i dati sono stati cancellati!", parent=parent)
                except mysql.connector.Error as err:
                    messagebox.showerror("Errore", f"Errore: {err}", parent=parent)
                finally:
                    conn.close()