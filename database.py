import sqlite3

def init_db():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_lungo TEXT,
            codice_breve TEXT,
            click INTEGER DEFAULT 0,
            data_creazione TEXT DEFAULT CURRENT_TIMESTAMP,
            scadenza TEXT DEFAULT NULL
        )
    """)
    conn.commit()
    conn.close()

def salva_url(url_lungo, codice_breve, scadenza=None):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (url_lungo, codice_breve, scadenza) VALUES (?, ?, ?)", (url_lungo, codice_breve, scadenza))
    conn.commit()
    conn.close()

def trova_url(codice_breve):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url_lungo, scadenza FROM urls WHERE codice_breve = ?", (codice_breve,))
    risultato = cursor.fetchone()
    conn.close()
    return risultato

def aggiorna_click(codice_breve):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE urls SET click = click + 1 WHERE codice_breve = ?", (codice_breve,))
    conn.commit()
    conn.close()

def get_tutti_url():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url_lungo, codice_breve, click, data_creazione, scadenza FROM urls")
    risultati = cursor.fetchall()
    conn.close()
    return risultati

def elimina_url(codice_breve):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urls WHERE codice_breve = ?", (codice_breve,))
    conn.commit()
    conn.close()