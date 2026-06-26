from flask import Flask, render_template, request, redirect
from database import init_db, salva_url, trova_url, aggiorna_click, get_tutti_url, elimina_url
from datetime import datetime
import random
import string

app = Flask(__name__)

@app.route("/")
def home():
    links = get_tutti_url()
    return render_template("index.html", links=links)

@app.route("/crea", methods=["POST"])
def crea():
    url_lungo = request.form["url_lungo"]
    scadenza = request.form.get("scadenza") or None

    if not url_lungo.startswith("http://") and not url_lungo.startswith("https://"):
        return render_template("index.html", errore="URL non valido! Deve iniziare con http:// o https://", links=get_tutti_url())

    codice = genera_codice()
    salva_url(url_lungo, codice, scadenza)
    return render_template("index.html", codice=codice, links=get_tutti_url())

@app.route("/<codice>")
def reindirizza(codice):
    risultato = trova_url(codice)
    if risultato:
        url_lungo, scadenza = risultato
        if scadenza:
            if datetime.now() > datetime.strptime(scadenza, "%Y-%m-%d"):
                return "Link scaduto!", 410
        aggiorna_click(codice)
        return redirect(url_lungo)
    else:
        return "Link non trovato!", 404

@app.route("/elimina/<codice>")
def elimina(codice):
    elimina_url(codice)
    return redirect("/")

def genera_codice():
    caratteri = string.ascii_letters + string.digits
    return "".join(random.choices(caratteri, k=6))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)