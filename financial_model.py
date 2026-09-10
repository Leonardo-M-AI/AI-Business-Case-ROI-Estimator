"""
financial_model.py
Compares three scenarios for handling customer churn: Status Quo (manual team),
Build (your own ML model), and Buy (external API/SaaS).
Edit the values in the INPUT section with your own numbers.
"""

# ============ INPUT (edit these) ============
n_customers_total = 7043               # total customers (from your churn dataset)
churn_rate = 0.265                     # 26.5% - from your churn-predictor notebook
avg_monthly_revenue_per_customer = 65  # estimated ARPU, in your currency
retention_success_rate = 0.30          # % of at-risk customers "saved" by the intervention

# Status Quo: human team handling retention manually
agents_needed = 2
hourly_wage = 20
hours_per_month = 160

# Build: infrastructure to serve your own ML model
server_monthly_cost = 90               # e.g. a small AWS EC2 instance with buffer
maintenance_hours_per_month = 8
dev_hourly_rate = 35

# Buy: external API charged per use (e.g. LLM or predictive scoring service)
api_cost_per_call = 0.002              # cost per customer scored
scoring_frequency_per_month = 1        # how many times per month you score the full customer base


# ============ CALCULATIONS ============

def customers_at_risk(n_customers_total, churn_rate):
    return round(n_customers_total * churn_rate)


def monthly_revenue_at_risk(n_at_risk, arpu):
    return n_at_risk * arpu


def monthly_revenue_saved(revenue_at_risk, retention_success_rate):
    return revenue_at_risk * retention_success_rate


def cost_status_quo():
    return agents_needed * hourly_wage * hours_per_month


def cost_build():
    return server_monthly_cost + (maintenance_hours_per_month * dev_hourly_rate)


def cost_buy(n_customers_total):
    return api_cost_per_call * n_customers_total * scoring_frequency_per_month


def payback_period_months(setup_cost, net_monthly_saving):
    if net_monthly_saving <= 0:
        return float("inf")
    return round(setup_cost / net_monthly_saving, 1)


def roi_percentage(total_saving, total_cost):
    if total_cost == 0:
        return float("inf")
    return round(((total_saving - total_cost) / total_cost) * 100, 1)


def report():
    n_risk = customers_at_risk(n_customers_total, churn_rate)
    rev_risk = monthly_revenue_at_risk(n_risk, avg_monthly_revenue_per_customer)
    rev_saved = monthly_revenue_saved(rev_risk, retention_success_rate)

    scenarios = [
        ("Status Quo (manual team)", cost_status_quo()),
        ("Build (own model)", cost_build()),
        ("Buy (external API)", cost_buy(n_customers_total)),
    ]

    print("=== SCENARIO OVERVIEW ===")
    print(f"Customers at risk of churn / month: {n_risk}")
    print(f"Monthly revenue at risk: {rev_risk:,.0f}")
    print(f"Monthly revenue saved (at {retention_success_rate*100:.0f}% retention success): {rev_saved:,.0f}\n")

    for name, cost in scenarios:
        net_saving = rev_saved - cost
        roi_12m = roi_percentage(rev_saved * 12, cost * 12)
        payback = payback_period_months(cost, net_saving) if net_saving > 0 else float("inf")

        print(f"--- {name} ---")
        print(f"Monthly cost: {cost:,.0f}")
        print(f"Net monthly saving: {net_saving:,.0f}")
        print(f"ROI at 12 months: {roi_12m}%")
        print(f"Payback period: {payback} months\n")


if __name__ == "__main__":
    report()
