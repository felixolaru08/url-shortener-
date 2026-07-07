# app.py
# questo è il file principale, quello che fa partire il sito

import random
import string
from datetime import datetime

from flask import Flask, render_template, request, redirect

from database import init_db, salva_url, trova_url, aggiorna_click, get_tutti_url, elimina_url

app = Flask(__name__)


@app.route("/")
def home():
    # pagina iniziale con tutti i link salvati
    lista_link = get_tutti_url()
    return render_template("index.html", links=lista_link)


@app.route("/crea", methods=["POST"])
def crea():
    # qui arrivano i dati del form quando uno crea un link nuovo
    url_lungo = request.form["url_lungo"]
    scadenza = request.form.get("scadenza")

    if scadenza == "":
        scadenza = None

    # controllo veloce che l'url sia scritto bene
    inizia_con_http = url_lungo.startswith("http://")
    inizia_con_https = url_lungo.startswith("https://")

    if inizia_con_http == False and inizia_con_https == False:
        messaggio_errore = "URL non valido! Deve iniziare con http:// o https://"
        return render_template("index.html", errore=messaggio_errore, links=get_tutti_url())

    codice = genera_codice()
    salva_url(url_lungo, codice, scadenza)

    return render_template("index.html", codice=codice, links=get_tutti_url())


@app.route("/<codice>")
def reindirizza(codice):
    # quando qualcuno clicca sul link corto, arriva qui
    risultato = trova_url(codice)

    if risultato == None:
        return "Link non trovato!", 404

    url_lungo = risultato[0]
    scadenza = risultato[1]

    # controllo se il link è scaduto
    if scadenza:
        data_scadenza = datetime.strptime(scadenza, "%Y-%m-%d")
        adesso = datetime.now()
        if adesso > data_scadenza:
            return "Link scaduto!", 410

    aggiorna_click(codice)
    return redirect(url_lungo)


@app.route("/elimina/<codice>")
def elimina(codice):
    # bottone per cancellare un link dalla lista
    elimina_url(codice)
    return redirect("/")


def genera_codice():
    # creo un codice a caso di 6 lettere/numeri per il link corto
    lettere_e_numeri = string.ascii_letters + string.digits
    codice_nuovo = ""
    for i in range(6):
        codice_nuovo = codice_nuovo + random.choice(lettere_e_numeri)
    return codice_nuovo


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", debug=False)
    