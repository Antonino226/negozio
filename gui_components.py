import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox

def create_table_window(query, title, db_manager):
    columns, data = db_manager.fetch_data(query)
    if not columns or not data:
        messagebox.showinfo("Nessun Dato", "La query non ha restituito risultati.")
        return
    
    window = tk.Toplevel()
    window.title(title)
    window.geometry("900x500")
    
    frame = ttk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    
    for i, row in enumerate(data):
        tag = "even" if i % 2 == 0 else "odd"
        tree.insert("", tk.END, values=row, tags=(tag,))
    tree.tag_configure("even", background="#ffffff")
    tree.tag_configure("odd", background="#e6f3ff")
    
    # Frame per i pulsanti di azione
    action_frame = ttk.Frame(window)
    action_frame.pack(pady=5)
    
    remove_button = ttk.Button(action_frame, text="Rimuovi", state="disabled")
    modify_button = ttk.Button(action_frame, text="Modifica", state="disabled")
    remove_button.pack(side=tk.LEFT, padx=5)
    modify_button.pack(side=tk.LEFT, padx=5)
    
    # Mappatura delle query alle tabelle, colonne ID e tabelle dipendenti
    table_map = {
        "Prodotti per Categoria": ("prodotti", "id_prodotto", ["dettagli_ordini"]),
        "Totale Vendite per Categoria": ("categorie", "nome_categoria", []),  # Aggregazione, no rimozione
        "Clienti con Ordini Non Pagati": ("ordini", "id_ordine", ["dettagli_ordini", "pagamenti"]),
        "Prodotti con Stock Basso": ("prodotti", "id_prodotto", ["dettagli_ordini"]),
        "Media Prezzo per Categoria": ("categorie", "nome_categoria", []),  # Aggregazione, no rimozione
        "Clienti Sopra la Media": ("clienti", "id_cliente", ["ordini"]),
        "Prodotti Più Venduti": ("prodotti", "id_prodotto", ["dettagli_ordini"]),
        "Ordini Sopra Massimo Pagamento": ("ordini", "id_ordine", ["dettagli_ordini", "pagamenti"]),
        "Stato Stock Prodotti": ("prodotti", "id_prodotto", ["dettagli_ordini"]),
        "Riepilogo Ordini": ("ordini", "id_ordine", ["dettagli_ordini", "pagamenti"])
    }
    
    table_info = table_map.get(title, (None, None, []))
    table, id_col, dependent_tables = table_info
    
    def on_select(event):
        selected_item = tree.selection()
        if selected_item and table and id_col in columns:
            remove_button.config(state="normal")
            modify_button.config(state="normal")
            selected_values = tree.item(selected_item[0], "values")
            id_index = columns.index(id_col)
            selected_id = selected_values[id_index]
            
            remove_button.config(command=lambda: remove_row(selected_id))
            modify_button.config(command=lambda: modify_row(selected_id, selected_values))
        else:
            remove_button.config(state="disabled")
            modify_button.config(state="disabled")
    
    def remove_row(selected_id):
        if not table:
            messagebox.showerror("Errore", "Tabella non identificata per questa query.")
            return
        
        if messagebox.askyesno("Conferma", f"Vuoi rimuovere la riga con {id_col}={selected_id}?"):
            try:
                # Elimina i record dipendenti
                for dep_table in dependent_tables:
                    if dep_table == "dettagli_ordini":
                        dep_query = "DELETE FROM dettagli_ordini WHERE id_ordine = %s"
                    elif dep_table == "pagamenti":
                        dep_query = "DELETE FROM pagamenti WHERE id_ordine = %s"
                    elif dep_table == "ordini":
                        dep_query = "DELETE FROM ordini WHERE id_cliente = %s"
                    else:
                        continue
                    db_manager.execute_query(dep_query, (selected_id,), parent=window)
                
                # Elimina il record principale
                delete_query = f"DELETE FROM {table} WHERE {id_col} = %s"
                db_manager.execute_query(delete_query, (selected_id,), parent=window)
                
                # Aggiorna la tabella
                columns, new_data = db_manager.fetch_data(query)
                tree.delete(*tree.get_children())
                for i, row in enumerate(new_data):
                    tag = "even" if i % 2 == 0 else "odd"
                    tree.insert("", tk.END, values=row, tags=(tag,))
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile rimuovere: {str(e)}")
    
    def modify_row(selected_id, current_values):
        if not table:
            messagebox.showerror("Errore", "Tabella non identificata per questa query.")
            return
        
        modify_window = tk.Toplevel(window)
        modify_window.title(f"Modifica {id_col}={selected_id}")
        modify_window.geometry("400x300")
        
        entries = []
        for i, col in enumerate(columns):
            ttk.Label(modify_window, text=col).grid(row=i, column=0, pady=5, padx=5, sticky="w")
            entry = ttk.Entry(modify_window)
            entry.insert(0, current_values[i])
            if col == id_col:  # Rendi l'ID non modificabile
                entry.config(state="disabled")
            entries.append(entry)
            entry.grid(row=i, column=1, pady=5, padx=5)
        
        def save_changes():
            new_values = [entry.get() for entry in entries]
            if id_col in columns:
                update_query = f"UPDATE {table} SET {', '.join([f'{col} = %s' for col in columns if col != id_col])} WHERE {id_col} = %s"
                params = [val for val in new_values if columns[new_values.index(val)] != id_col] + [selected_id]
                try:
                    db_manager.execute_query(update_query, params, parent=modify_window)
                    columns, new_data = db_manager.fetch_data(query)
                    tree.delete(*tree.get_children())
                    for i, row in enumerate(new_data):
                        tag = "even" if i % 2 == 0 else "odd"
                        tree.insert("", tk.END, values=row, tags=(tag,))
                    modify_window.destroy()
                except Exception as e:
                    messagebox.showerror("Errore", f"Impossibile modificare: {str(e)}")
        
        ttk.Button(modify_window, text="Salva", command=save_changes).grid(row=len(columns), column=0, columnspan=2, pady=10)
    
    tree.bind("<<TreeviewSelect>>", on_select)
    
    ttk.Button(window, text="Chiudi", command=window.destroy).pack(pady=5)

def create_insert_cliente_window(db_manager):
    window = tk.Toplevel()
    window.title("Inserisci Cliente")
    window.geometry("300x250")
    
    frame = ttk.Frame(window, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(frame, text="Nome").grid(row=0, column=0, pady=5, sticky="w")
    nome_entry = ttk.Entry(frame)
    nome_entry.grid(row=0, column=1, pady=5)
    
    ttk.Label(frame, text="Cognome").grid(row=1, column=0, pady=5, sticky="w")
    cognome_entry = ttk.Entry(frame)
    cognome_entry.grid(row=1, column=1, pady=5)
    
    ttk.Label(frame, text="Email").grid(row=2, column=0, pady=5, sticky="w")
    email_entry = ttk.Entry(frame)
    email_entry.grid(row=2, column=1, pady=5)
    
    ttk.Label(frame, text="Telefono").grid(row=3, column=0, pady=5, sticky="w")
    telefono_entry = ttk.Entry(frame)
    telefono_entry.grid(row=3, column=1, pady=5)
    
    def submit():
        from datetime import datetime
        query = "INSERT INTO clienti (nome, cognome, email, telefono, data_registrazione) VALUES (%s, %s, %s, %s, %s)"
        params = (nome_entry.get(), cognome_entry.get(), email_entry.get(), telefono_entry.get(), datetime.now().date())
        db_manager.execute_query(query, params, parent=window)
        window.destroy()
    
    ttk.Button(frame, text="Inserisci", command=submit).grid(row=4, column=0, columnspan=2, pady=10)