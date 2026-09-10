"""
financial_model.py
Confronto Status Quo vs Build vs Buy per un caso di churn prediction/retention.
Modifica i valori in INPUT con i tuoi numeri reali (anche stime plausibili vanno bene).
"""

# ============ INPUT (modifica qui) ============
n_customers_total = 7043          # clienti totali (dal tuo dataset churn)
churn_rate = 0.265                # 26.5% - dal tuo notebook
avg_monthly_revenue_per_customer = 65   # ARPU stimato, es. in euro
retention_success_rate = 0.30     # % di clienti a rischio "salvati" grazie all'intervento

# Status Quo: team umano che gestisce retention manualmente
agents_needed = 2
hourly_wage = 20
hours_per_month = 160

# Build: infrastruttura per servire il tuo modello ML
server_monthly_cost = 90          # es. istanza AWS EC2 t3.medium con qualche buffer
maintenance_hours_per_month = 8
dev_hourly_rate = 35

# Buy: API esterna a consumo (es. LLM/servizio scoring predittivo)
api_cost_per_call = 0.002         # costo per cliente scorato
scoring_frequency_per_month = 1   # quante volte al mese scori l'intera customer base

# ============ CALCOLI ============

def clienti_a_rischio(n_customers_total, churn_rate):
    return round(n_customers_total * churn_rate)

def revenue_a_rischio_mensile(n_at_risk, arpu):
    return n_at_risk * arpu

def revenue_salvata_mensile(revenue_a_rischio, retention_success_rate):
    return revenue_a_rischio * retention_success_rate

def costo_status_quo():
    return agents_needed * hourly_wage * hours_per_month

def costo_build():
    return server_monthly_cost + (maintenance_hours_per_month * dev_hourly_rate)

def costo_buy(n_customers_total):
    return api_cost_per_call * n_customers_total * scoring_frequency_per_month

def payback_period_mesi(costo_iniziale_setup, risparmio_mensile_netto):
    if risparmio_mensile_netto <= 0:
        return float("inf")
    return round(costo_iniziale_setup / risparmio_mensile_netto, 1)

def roi_percentuale(risparmio_totale, costo_totale):
    if costo_totale == 0:
        return float("inf")
    return round(((risparmio_totale - costo_totale) / costo_totale) * 100, 1)


def report():
    n_risk = clienti_a_rischio(n_customers_total, churn_rate)
    rev_risk = revenue_a_rischio_mensile(n_risk, avg_monthly_revenue_per_customer)
    rev_saved = revenue_salvata_mensile(rev_risk, retention_success_rate)

    sq_cost = costo_status_quo()
    build_cost = costo_build()
    buy_cost = costo_buy(n_customers_total)

    print("=== SCENARIO OVERVIEW ===")
    print(f"Clienti a rischio churn/mese: {n_risk}")
    print(f"Revenue mensile a rischio: €{rev_risk:,.0f}")
    print(f"Revenue mensile salvata (con retention al {retention_success_rate*100:.0f}%): €{rev_saved:,.0f}\n")

    for nome, costo in [("Status Quo (team manuale)", sq_cost),
                        ("Build (modello proprio)", build_cost),
                        ("Buy (API esterna)", buy_cost)]:
        risparmio_netto = rev_saved - costo
        roi_12m = roi_percentuale(rev_saved * 12, costo * 12)
        payback = payback_period_mesi(costo, risparmio_netto) if risparmio_netto > 0 else float("inf")
        print(f"--- {nome} ---")
        print(f"Costo mensile: €{costo:,.0f}")
        print(f"Risparmio netto mensile: €{risparmio_netto:,.0f}")
        print(f"ROI a 12 mesi: {roi_12m}%")
        print(f"Payback period: {payback} mesi\n")


if __name__ == "__main__":
    report()
