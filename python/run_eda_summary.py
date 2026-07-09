"""Print control-tower KPIs from parquet facts."""
from pathlib import Path
import pandas as pd

data = Path(__file__).resolve().parents[1] / "data"
orders = pd.read_parquet(data / "fact_orders.parquet")
ship = pd.read_parquet(data / "fact_shipments.parquet")
rev = orders[orders["is_revenue"] == True]
if rev.empty:
    rev = orders[orders["is_revenue"] == 1]
o = orders.groupby("order_id").agg(otif=("is_otif", "min"), perfect=("is_perfect_order", "min"))
print("revenue_m", round(rev["net_sales"].sum() / 1e6, 1))
print("orders", orders["order_id"].nunique())
print("otif_pct", round(100 * o["otif"].mean(), 1))
print("perfect_pct", round(100 * o["perfect"].mean(), 1))
print("freight_m", round(ship["freight_cost"].sum() / 1e6, 1))
print("co2_t", round(ship["co2_kg"].sum() / 1000, 1))
