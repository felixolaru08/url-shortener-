"""Modulo principale dell'applicazione URL Shortener."""

import random
import string
from datetime import datetime

from flask import Flask, render_template, request, redirect

from database import init_db, salva_url, trova_url, aggiorna_click, get_tutti_url, elimina_url

app = Flask(__name__)


@app.route("/")
def home():
    """Mostra la pagina principale con la lista dei link."""
    links = get_tutti_url()
    return render_template("index.html", links=links)


@app.route("/crea", methods=["POST"])
def crea():
    """Riceve l'URL lungo, genera il codice breve e lo salva nel database."""
    url_lungo = request.form["url_lungo"]
    scadenza = request.form.get("scadenza") or None

    if not url_lungo.startswith("http://") and not url_lungo.startswith("https://"):
        return render_template(
            "index.html",
            errore="URL non valido! Deve iniziare con http:// o https://",
            links=get_tutti_url()
        )

    codice = genera_codice()
    salva_url(url_lungo, codice, scadenza)
    return render_template("index.html", codice=codice, links=get_tutti_url())


@app.route("/<codice>")
def reindirizza(codice):
    """Cerca il codice nel database e reindirizza all'URL originale."""
    risultato = trova_url(codice)
    if risultato:
        url_lungo, scadenza = risultato
        if scadenza and datetime.now() > datetime.strptime(scadenza, "%Y-%m-%d"):
            return "Link scaduto!", 410
        aggiorna_click(codice)
        return redirect(url_lungo)
    return "Link non trovato!", 404


@app.route("/elimina/<codice>")
def elimina(codice):
    """Elimina un link dal database."""
    elimina_url(codice)
    return redirect("/")


def genera_codice():
    """Genera una stringa casuale di 6 caratteri alfanumerici."""
    caratteri = string.ascii_letters + string.digits
    return "".join(random.choices(caratteri, k=6))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
