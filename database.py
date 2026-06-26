"""Modulo per la gestione del database SQLite dell'URL Shortener."""

import sqlite3


def init_db():
    """Crea il database e la tabella urls se non esistono."""
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
    """Inserisce un nuovo URL lungo e codice breve nel database."""
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (url_lungo, codice_breve, scadenza) VALUES (?, ?, ?)",
        (url_lungo, codice_breve, scadenza)
    )
    conn.commit()
    conn.close()


def trova_url(codice_breve):
    """Cerca e restituisce l'URL lungo associato a un codice breve."""
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT url_lungo, scadenza FROM urls WHERE codice_breve = ?",
        (codice_breve,)
    )
    risultato = cursor.fetchone()
    conn.close()
    return risultato


def aggiorna_click(codice_breve):
    """Incrementa il contatore click di un link."""
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE urls SET click = click + 1 WHERE codice_breve = ?",
        (codice_breve,)
    )
    conn.commit()
    conn.close()


def get_tutti_url():
    """Restituisce tutti i link salvati con le relative statistiche."""
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT url_lungo, codice_breve, click, data_creazione, scadenza FROM urls"
    )
    risultati = cursor.fetchall()
    conn.close()
    return risultati


def elimina_url(codice_breve):
    """Elimina un link dal database."""
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM urls WHERE codice_breve = ?",
        (codice_breve,)
    )
    conn.commit()
    conn.close()
