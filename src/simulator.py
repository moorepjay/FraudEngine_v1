import pandas as pd
from faker import Faker
import os
import random
from datetime import datetime, timedelta


data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
registry_path = os.path.join(data_dir, "user_registry.csv")
transaction_path = os.path.join(data_dir, "transaction_audit.csv")
# IDENTITY
# Every transaction needs to be tethered to an entity. There is not always a clean user_id,
# so we simulate the pieces that create that ID.

user_registry = []

fake = Faker()
Faker.seed(1414)

# Loop generates user and device ID's for "registered users".
for i in range(100):
    user_id = fake.uuid4()
    device_id = fake.mac_address()
    entry = {"u_id": user_id, "d_id": device_id}
    user_registry.append(entry)


# Save as CSV
if not os.path.exists(registry_path):
    print("Investigator Note: No registry found. Generating new population...")
    # ... [Insert your User Generation Loop here] ...
    user_df = pd.DataFrame(user_registry)
    user_df.to_csv(registry_path, index=False)
else:
    print("Investigator Note: Registry found. Loading existing suspects...")
    user_df = pd.read_csv(registry_path)


# TRANSACTION

ledger = []
base_time = datetime.now()

for i in range(5000):
    user_df = pd.read_csv(registry_path)
    random_user = user_df.sample(n=1)
    u_id = random_user["u_id"].values[0]
    d_id = random_user["d_id"].values[0]
    purchase_amount = round(random.uniform(10, 500))
    purchase_date = base_time - timedelta(minutes=i * 15)

    txn = {
        "purchase_date": purchase_date,
        "u_id": u_id,
        "d_id": d_id,
        "usd": purchase_amount,
        "status": 1,
    }
    ledger.append(txn)

txn_df = pd.DataFrame(ledger)
txn_df.to_csv(transaction_path, index=False)
