import os
import pandas as pd

# Load most recent transaction ledger for stat checking.
DATA_FILE = os.path.join("data", "transaction_audit.csv")


df = pd.read_csv(DATA_FILE)

# Sum usd per user.
user_totals = df.groupby("u_id")["usd"].sum().reset_index()

# Velocity per user.
user_velocity = df.groupby("u_id").size().reset_index(name="txn_count")
mask = user_velocity["txn_count"] > 70
velocity_alert = user_velocity[mask]

print(velocity_alert)
