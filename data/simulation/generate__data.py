import pandas as pd
import random
from datetime import datetime, timedelta

def generate_logs(unit_ids, start_date, end_date):
    logs = []
    for unit_id in unit_ids:
        current_date = start_date
        while current_date <= end_date:
            logs.append({
                "unit_id": unit_id,
                "log_date": current_date,
                "hours_operated": round(random.uniform(2, 12), 2),
                "fuel_used": round(random.uniform(10, 40), 2),
                "breakdown": random.choice([False, False, True]),
                "remarks": random.choice(["Normal", "Minor Issue", "Major Issue", ""])
                })
            current_date += timedelta(days=1)
    return pd.DataFrame(logs)

if __name__ == "__main__":
    df = generate_logs(unit_ids=[1, 2, 3], start_date=datetime(2025, 1, 1), end_date=datetime(2025, 1, 30))
    df.to_csv("equipment_logs.csv", index=False)
    print("Simulasi data selesai disimpan.")