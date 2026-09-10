# AI Business Case: Customer Retention — Build vs Buy vs Status Quo

## Executive Summary (5 righe max)
[Azienda tipo] perde ogni mese circa €[X] di revenue per churn evitabile.
Confrontando 3 approcci — gestione manuale, modello ML proprietario, API esterna —
il modello [Build/Buy] risulta il più conveniente, con un payback stimato di
[X] mesi e un ROI a 12 mesi del [X]%. Raccomandazione: [una frase].

## 1. Il Problema
- Tasso di churn: [X]% su una base di [N] clienti
- Revenue mensile a rischio: €[X]
- Perché è un problema di business, non solo tecnico: [1-2 frasi]

## 2. Le Tre Opzioni
| Scenario | Costo mensile | Risparmio netto | ROI 12m | Payback |
|---|---|---|---|---|
| Status Quo | €X | €X | X% | X mesi |
| Build | €X | €X | X% | X mesi |
| Buy | €X | €X | X% | X mesi |

(Numeri generati da `financial_model.py`)

## 3. Trade-off da considerare
- **Latenza vs costo**: [quando conviene un modello piccolo/economico vs uno grande]
- **Privacy/GDPR**: [dati trattati in-house vs inviati a un'API esterna]
- **Scalabilità**: [cosa succede se la customer base raddoppia]

## 4. Raccomandazione
[2-3 frasi con la scelta consigliata e sotto quali condizioni cambierebbe]

## 5. Demo
App interattiva disponibile in `app.py` — permette di inserire i propri
numeri e ottenere payback/ROI in tempo reale.

```
pip install streamlit
streamlit run app.py
```

## 6. Modello tecnico di riferimento
Basato su [customer-churn-predictor](link al tuo repo) — Random Forest,
ROC-AUC 0.833, identifica il 70.9% dei clienti che effettivamente abbandonano.

## Limiti dell'analisi
[1-2 frasi oneste: stime ARPU, assunzioni sul tasso di successo della retention, ecc.]
