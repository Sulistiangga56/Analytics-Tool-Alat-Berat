import random
from datetime import datetime, timedelta
from sqlalchemy import text
from db_config import engine

# Contoh data dummy untuk manufacturer dan unit_type
manufacturers = ["Caterpillar", "Komatsu", "Hitachi", "Volvo", "John Deere"]
unit_types = ["Excavator", "Bulldozer", "Loader", "Dump Truck", "Grader"]

def generate_unit_master_data(n=100):
    units = []
    for i in range(1, n+1):
        unit_name = f"Unit-{i:03d}"
        unit_code = f"UC{i:05d}"
        unit_type = random.choice(unit_types)
        manufacturer = random.choice(manufacturers)
        year_manufactured = random.randint(2000, 2023)
        units.append({
            "unit_name": unit_name,
            "unit_code": unit_code,
            "unit_type": unit_type,
            "manufacturer": manufacturer,
            "year_manufactured": year_manufactured
        })
    return units

def generate_equipment_logs(unit_ids, logs_per_unit=10):
    logs = []
    for unit_id in unit_ids:
        start_date = datetime(2025, 1, 1)
        for i in range(logs_per_unit):
            log_date = start_date + timedelta(days=i)
            hours_operated = round(random.uniform(0, 24), 2)
            fuel_used = round(hours_operated * random.uniform(0.5, 1.5), 2)
            breakdown = random.choices([True, False], weights=[0.05, 0.95])[0]
            remarks = "Normal operation" if not breakdown else "Breakdown occurred"
            logs.append({
                "unit_id": unit_id,
                "log_date": log_date.date(),
                "hours_operated": hours_operated,
                "fuel_used": fuel_used,
                "breakdown": breakdown,
                "remarks": remarks
            })
    return logs

def insert_unit_master(units):
    with engine.connect() as conn:
        for u in units:
            conn.execute(
                text(
                    """
                    INSERT INTO unit_master (unit_name, unit_code, unit_type, manufacturer, year_manufactured)
                    VALUES (:unit_name, :unit_code, :unit_type, :manufacturer, :year_manufactured)
                    """
                ),
                u
            )
        conn.commit()

def get_all_unit_ids():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT unit_id FROM unit_master"))
        return [row.unit_id for row in result]

def insert_equipment_logs(logs):
    with engine.connect() as conn:
        for log in logs:
            conn.execute(
                text(
                    """
                    INSERT INTO equipment_logs (unit_id, log_date, hours_operated, fuel_used, breakdown, remarks)
                    VALUES (:unit_id, :log_date, :hours_operated, :fuel_used, :breakdown, :remarks)
                    """
                ),
                log
            )
        conn.commit()

if __name__ == "__main__":
    units = generate_unit_master_data(100)
    insert_unit_master(units)
    unit_ids = get_all_unit_ids()
    logs = generate_equipment_logs(unit_ids, logs_per_unit=10)
    insert_equipment_logs(logs)
    print("Dummy data inserted successfully.")
