"""
app.py - Demo interattiva per CEO/CFO
Avvio: streamlit run app.py
(richiede: pip install streamlit)
"""
import streamlit as st

st.set_page_config(page_title="AI ROI Estimator", layout="centered")
st.title("AI Business Case: Build vs Buy vs Status Quo")
st.write("Inserisci i dati della tua azienda per stimare payback period e ROI.")

n_customers_total = st.number_input("Numero totale clienti", min_value=1, value=7043)
churn_rate = st.slider("Tasso di churn stimato (%)", 0.0, 100.0, 26.5) / 100
arpu = st.number_input("Revenue mensile media per cliente (€)", min_value=0.0, value=65.0)
retention_success_rate = st.slider("Efficacia intervento di retention (%)", 0.0, 100.0, 30.0) / 100

st.subheader("Status Quo (team manuale)")
agents_needed = st.number_input("N. agenti retention", min_value=0, value=2)
hourly_wage = st.number_input("Costo orario agente (€)", min_value=0.0, value=20.0)
hours_per_month = st.number_input("Ore/mese per agente", min_value=0, value=160)

st.subheader("Build (modello proprio)")
server_monthly_cost = st.number_input("Costo server mensile (€)", min_value=0.0, value=90.0)
maintenance_hours_per_month = st.number_input("Ore manutenzione/mese", min_value=0, value=8)
dev_hourly_rate = st.number_input("Costo orario sviluppatore (€)", min_value=0.0, value=35.0)

st.subheader("Buy (API esterna)")
api_cost_per_call = st.number_input("Costo per chiamata API (€)", min_value=0.0, value=0.002, format="%.4f")
scoring_frequency_per_month = st.number_input("Scoring al mese (n. volte)", min_value=1, value=1)

# --- Calcoli ---
n_risk = round(n_customers_total * churn_rate)
rev_risk = n_risk * arpu
rev_saved = rev_risk * retention_success_rate

sq_cost = agents_needed * hourly_wage * hours_per_month
build_cost = server_monthly_cost + (maintenance_hours_per_month * dev_hourly_rate)
buy_cost = api_cost_per_call * n_customers_total * scoring_frequency_per_month

st.header("Risultati")
st.metric("Clienti a rischio/mese", n_risk)
st.metric("Revenue salvata stimata/mese (€)", f"{rev_saved:,.0f}")

col1, col2, col3 = st.columns(3)
for col, nome, costo in [(col1, "Status Quo", sq_cost),
                          (col2, "Build", build_cost),
                          (col3, "Buy", buy_cost)]:
    risparmio_netto = rev_saved - costo
    roi_12m = ((rev_saved * 12 - costo * 12) / (costo * 12) * 100) if costo > 0 else 0
    payback = (costo / risparmio_netto) if risparmio_netto > 0 else float("inf")
    col.subheader(nome)
    col.write(f"Costo/mese: €{costo:,.0f}")
    col.write(f"Risparmio netto: €{risparmio_netto:,.0f}")
    col.write(f"ROI 12m: {roi_12m:.0f}%")
    col.write(f"Payback: {payback:.1f} mesi" if payback != float("inf") else "Payback: N/A")
