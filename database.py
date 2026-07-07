# gestione_db.py
# qui dentro c'è tutta la roba per salvare i link nel database

import sqlite3

nome_db = "urls.db"


def init_db():
    # creo il database la prima volta che parte il programma
    conn = sqlite3.connect(nome_db)
    cursor = conn.cursor()

    query = """
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_lungo TEXT,
            codice_breve TEXT,
            click INTEGER DEFAULT 0,
            data_creazione TEXT DEFAULT CURRENT_TIMESTAMP,
            scadenza TEXT DEFAULT NULL
        )
    """
    cursor.execute(query)

    conn.commit()
    conn.close()


def salva_url(url_lungo, codice_breve, scadenza=None):
    # salvo il nuovo link nel database
    conn = sqlite3.connect(nome_db)
    cursor = conn.cursor()

    dati = (url_lungo, codice_breve, scadenza)
    cursor.execute("INSERT INTO urls (url_lungo, codice_breve, scadenza) VALUES (?, ?, ?)", dati)

    conn.commit()
    conn.close()


def trova_url(codice_breve):
    # cerco il link vero partendo dal codice corto
    conn = sqlite3.connect(nome_db)
    cursor = conn.cursor()

    cursor.execute("SELECT url_lungo, scadenza FROM urls WHERE codice_breve = ?", (codice_breve,))
    risultato = cursor.fetchone()

    conn.close()

    return risultato


def aggiorna_click(codice_breve):
    # ogni volta che qualcuno clicca il link aggiungo 1 al contatore
    conn = sqlite3.connect(nome_db)
    cursor = conn.cursor()

    click_vecchio = cursor.execute("SELECT click FROM urls WHERE codice_breve = ?", (codice_breve,)).fetchone()

    if click_vecchio is not None:
        nuovo_click = click_vecchio[0] + 1
        cursor.execute("UPDATE urls SET click = ? WHERE codice_breve = ?", (nuovo_click, codice_breve))

    conn.commit()
    conn.close()


def get_tutti_url():
    # prendo tutta la lista dei link salvati
    conn = sqlite3.connect(nome_db)
    cursor = conn.cursor()

    cursor.execute("SELECT url_lungo, codice_breve, click, data_creazione, scadenza FROM urls")
    lista_url = cursor.fetchall()

    conn.close()

    return lista_url


def elimina_url(codice_breve):
    # tolgo il link dal database
    conn = sqlite3.connect(nome_db)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM urls WHERE codice_breve = ?", (codice_breve,))

    conn.commit()
    conn.close()
    