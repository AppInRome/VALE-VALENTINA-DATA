# VALE-VALENTINA-DATA

Repository pubblico di conoscenza statistica per VALE e Valentina. Progetto indipendente, non prodotto ufficiale ISTAT.

## Struttura
- semantic/: vocabolario curato, ricerca offline, importatore WordNet candidato
- catalog/: 77 file catalogati e 44 schemi SQLite della base 2.52, 141 indicatori BES
- knowledge/: grafo con 25 concetti e 12 relazioni
- connectors/: Eurostat e World Bank; registro delle altre fonti
- models/: manifest e programmi PC opzionali, senza pesi distribuiti
- methods/: regole statistiche
- tests/: casi di riferimento, non certificazione istituzionale
- validation/: build e controlli
- distribution/knowledge.tsv: pacchetto per VALE 2.53/2.54

## Uso
`python3 validation/check.py` per la validazione offline.
`python3 validation/live_check.py` per collaudi pubblici online espliciti.
`python3 semantic/search.py "Quanti nosocomi?"` per un suggerimento di concetto.

Il pacchetto distribuito ha revisione 25301, identica a quella integrata nella 2.54: l'app già aggiornata può quindi rispondere "Catalogo già aggiornato". Per una revisione futura modificare il vocabolario, incrementare la revisione e rigenerare il pacchetto. Nessuna chiave o informazione personale.

L'app legge esclusivamente il TSV; gli script Python sono strumenti di sviluppo e non vengono eseguiti dal telefono. Catalogato non significa interrogabile. I connettori ulteriori, E5 e il modello locale richiedono integrazione e collaudo. Non usare un modello generativo come fonte di cifre.

I workflow richiedono opt-in mediante variabili del repository. Nessuna API AI a pagamento. Non pubblicare pesi, token, dati privati o dati soggetti a licenze incompatibili.
