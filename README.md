# URL Shortener Locale

**Autore:** Felix Olaru  
**Progetto:** Sviluppato come esercizio pratico durante il periodo di stage.



## Obiettivo del Progetto

L'obiettivo di questa applicazione web è fornire uno strumento semplice per accorciare URL lunghi, simile a un mini Bitly locale. L'utente può incollare un URL lungo, ottenere un link breve generato casualmente, usarlo per essere reindirizzato al sito originale e monitorare il numero di click ricevuti da ogni link.



## Tecnologie Utilizzate

- Python 3
- `Flask` — framework web per gestire le rotte e le richieste HTTP
- `SQLite` — database locale per salvare URL e statistiche
- `random` & `string` — generazione casuale dei codici brevi
- `HTML + Jinja2` — interfaccia web con template dinamici



## Struttura del Progetto

```
url_shortener/
├── app.py            ← cuore dell'applicazione, gestisce le rotte Flask
├── database.py       ← tutte le funzioni che interagiscono con il database
├── urls.db           ← file del database SQLite (generato automaticamente)
└── templates/
    └── index.html    ← pagina web dell'applicazione
```



## Struttura del Codice

### `app.py`

| Funzione | Responsabilità |
| :--- | :--- |
| `home()` | Mostra la pagina principale con il form e la lista dei link |
| `crea()` | Riceve l'URL lungo, genera il codice breve e lo salva nel database |
| `reindirizza(codice)` | Cerca il codice nel database e reindirizza all'URL originale |
| `genera_codice()` | Genera una stringa casuale di 6 caratteri alfanumerici |

### `database.py`

| Funzione | Responsabilità |
| :--- | :--- |
| `init_db()` | Crea il database e la tabella se non esistono |
| `salva_url()` | Inserisce un nuovo URL lungo e codice breve nel database |
| `trova_url()` | Cerca e restituisce l'URL lungo associato a un codice breve |
| `aggiorna_click()` | Incrementa il contatore click di un link |
| `get_tutti_url()` | Restituisce tutti i link salvati con le relative statistiche |



## Struttura del Database

Il database contiene una singola tabella `urls` con i seguenti campi:

| Campo | Tipo | Descrizione |
| :--- | :--- | :--- |
| `id` | INTEGER | Identificatore univoco autoincrementale |
| `url_lungo` | TEXT | L'URL originale inserito dall'utente |
| `codice_breve` | TEXT | Il codice casuale di 6 caratteri generato |
| `click` | INTEGER | Numero di volte che il link breve è stato utilizzato |



## Installazione e Avvio

1. Clona il repository o scarica i file del progetto.
2. Installa le dipendenze necessarie:
   ```bash
   pip3 install flask
   ```
3. Avvia l'applicazione:
   ```bash
   python3 app.py
   ```
4. Apri il browser e vai su:
   ```
   http://127.0.0.1:5000
   ```



## Funzionalità dell'Applicazione

1. **Accorciare un URL** — incolla un URL lungo nel form e clicca "Accorcia!". Viene generato un codice breve casuale di 6 caratteri.
2. **Usare il link breve** — vai su `http://127.0.0.1:5000/abc123` per essere reindirizzato automaticamente all'URL originale.
3. **Statistiche** — nella pagina principale è visibile la lista di tutti i link creati con il numero di click ricevuti.



## Esempio di Utilizzo

```
URL inserito:  https://www.google.com
Codice breve:  aB3kQ1
Link breve:    http://127.0.0.1:5000/aB3kQ1

→ Visitando il link breve si viene reindirizzati a https://www.google.com
→ Il contatore click si aggiorna automaticamente ad ogni visita
```



## Problemi Incontrati e Soluzioni Adottate

| Problema Incontrato | Soluzione Adottata |
| :--- | :--- |
| *Import duplicati:* `from flask import Flask` era scritto tre volte causando un errore di endpoint. | Unificati tutti gli import di Flask in una sola riga. |
| *Codice breve non univoco:* due link potevano ricevere lo stesso codice casuale. | La funzione `genera_codice()` usa `random.choices()` su un pool di 62 caratteri, rendendo le collisioni estremamente improbabili. |
| *Codice non trovato:* visitare un link breve inesistente causava un errore interno. | Aggiunto controllo con risposta `404` e messaggio "Link non trovato!". |