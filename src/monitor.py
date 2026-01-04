import os
import pandas as pd

# Load most recent transaction ledger for stat checking.
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.abspath(
    os.path.join(script_dir, "..", "data", "transaction_audit.csv")
)


if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)

    # Convert the 'purchase_date' column to actual datetime objects
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    # Sort the values so the oldest transaction is at the top
    df = df.sort_values(by=["u_id", "purchase_date"])
    # Calculate time-gap between user txns.
    df["time_gap_sec"] = df.groupby("u_id")["purchase_date"].diff().dt.total_seconds()
    print(df[["u_id", "purchase_date", "time_gap_sec"]].head(10))

    # HIGH VOLUME
    user_volume = df.groupby("u_id").size().reset_index(name="txn_count")
    mask = user_volume["txn_count"] > 50
    volume_alerts = user_volume[mask]

    # VELOCITY
    velocity_mask = df["time_gap_sec"] < 5
    velocity_alerts = df[velocity_mask]

    print("\n" + "=" * 30)
    print("      FORENSIC CASE SUMMARY")
    print("\n" + "=" * 30)

    # For now we will report on users that are flagged for both alerts.
    set_volume = set(volume_alerts["u_id"])
    set_velocity = set(velocity_alerts["u_id"])
    high_risk_ids = set_volume.intersection(set_velocity)

    print(f"Total Transactions: {len(df)}")
    print(f"Volume Alerts:      {len(set_volume)}")
    print(f"Velocity Alerts:    {len(set_velocity)}")
    print(f"High-Risk Suspects: {len(high_risk_ids)}")

    if high_risk_ids:
        print("\n[!] TARGETS IDENTIFIED:")
        for suspect in high_risk_ids:
            print(f" -> {suspect}")
else:
    print(f"Investigator Error: Evidence file not found at {DATA_FILE}")
