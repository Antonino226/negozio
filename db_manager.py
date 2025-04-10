import mysql.connector
from tkinter import messagebox

class DatabaseManager:
    def __init__(self, host="localhost", user="root", password="root", database="negozio"):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }

    def connect(self):
        try:
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            messagebox.showerror("Errore", f"Connessione fallita: {err}")
            return None

    def fetch_data(self, query):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            conn.close()
            return columns, results
        return [], []

    def execute_query(self, query, params=None, parent=None):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                messagebox.showinfo("Successo", "Operazione completata!", parent=parent)
            except mysql.connector.Error as err:
                messagebox.showerror("Errore", f"Errore: {err}", parent=parent)
            finally:
                conn.close()