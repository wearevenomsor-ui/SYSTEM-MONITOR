"""
Predictive Maintenance for Campus Equipment - Synthetic Sensor Telemetry Generator
Generates realistic multi-sensor time-series logs for campus equipment:
- HVAC Chillers
- Air Handling Units (AHU)
- Water Circulation Pumps
- Emergency Diesel Generators

Includes physics-informed degradation patterns:
- Thermal Runaway (cooling loop clogging / heat buildup)
- Bearing Degradation (vibration harmonics & acoustic spikes)
- Hydraulic Pressure Decay (impeller cavitation / pipe seal leaks)
- Normal aging vs Anomaly failure states
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

EQUIPMENT_PROFILES = {
    "Chiller-Central-01": {
        "type": "HVAC Chiller",
        "temp_base": 58.0,
        "vib_base": 1.1,
        "pressure_base": 52.0,
        "power_base": 42.0,
        "sound_base": 62.0,
    },
    "AHU-Library-North": {
        "type": "Air Handling Unit",
        "temp_base": 42.0,
        "vib_base": 0.8,
        "pressure_base": 30.0,
        "power_base": 18.0,
        "sound_base": 55.0,
    },
    "Pump-MainLoop-03": {
        "type": "Water Circulation Pump",
        "temp_base": 50.0,
        "vib_base": 1.4,
        "pressure_base": 65.0,
        "power_base": 28.0,
        "sound_base": 68.0,
    },
    "GenSet-Emergency-A": {
        "type": "Diesel Generator",
        "temp_base": 82.0,
        "vib_base": 2.2,
        "pressure_base": 45.0,
        "power_base": 85.0,
        "sound_base": 78.0,
    }
}


def generate_synthetic_telemetry(n_samples_per_machine: int = 1500, random_seed: int = 42) -> pd.DataFrame:
    """
    Generates time-series sensor telemetry for all campus machines.
    Returns a pandas DataFrame ready for feature engineering and training.
    """
    np.random.seed(random_seed)
    all_records = []
    start_time = datetime.now() - timedelta(days=90)

    for machine_id, profile in EQUIPMENT_PROFILES.items():
        base_t = profile["temp_base"]
        base_v = profile["vib_base"]
        base_p = profile["pressure_base"]
        base_kw = profile["power_base"]
        base_db = profile["sound_base"]

        # Simulated operational run hours spanning 200 to 7500 hours
        init_hours = np.random.uniform(500, 3000)
        hours = np.linspace(init_hours, init_hours + 2000, n_samples_per_machine)
        timestamps = [start_time + timedelta(minutes=15 * i) for i in range(n_samples_per_machine)]

        # Gradual baseline wear as hours pile up
        aging_factor = (hours - init_hours) / 4000.0

        # Normal fluctuations
        temp = base_t + (aging_factor * 6.0) + np.random.normal(0, 1.8, n_samples_per_machine)
        vibration = base_v + (aging_factor * 0.8) + np.random.normal(0, 0.12, n_samples_per_machine)
        pressure = base_p - (aging_factor * 3.5) + np.random.normal(0, 1.0, n_samples_per_machine)
        power = base_kw + (aging_factor * 4.0) + np.random.normal(0, 1.5, n_samples_per_machine)
        sound = base_db + (aging_factor * 4.5) + np.random.normal(0, 1.2, n_samples_per_machine)

        # Labels: failure_imminent (0 = Healthy, 1 = Maintenance Required)
        # Remaining Useful Life (RUL) in hours
        failure_labels = np.zeros(n_samples_per_machine, dtype=int)
        rul_hours = np.clip(1200 - (aging_factor * 800) + np.random.normal(0, 30, n_samples_per_machine), 20, 1500)

        # Inject realistic failure episodes (bearing breakdown, thermal runaway, pressure seal blow)
        # Create 3-4 degraded failure clusters per machine
        num_anomalies = int(n_samples_per_machine * 0.16)
        anomaly_starts = np.random.choice(range(100, n_samples_per_machine - 40), size=5, replace=False)

        for start_idx in anomaly_starts:
            duration = np.random.randint(15, 35)
            end_idx = min(start_idx + duration, n_samples_per_machine)
            mode = np.random.choice(["bearing_fault", "thermal_runaway", "seal_leak"])

            for idx in range(start_idx, end_idx):
                severity = (idx - start_idx + 1) / duration
                failure_labels[idx] = 1
                rul_hours[idx] = max(1.0, 48.0 * (1.0 - severity))  # Critical failure imminent in <48h

                if mode == "bearing_fault":
                    vibration[idx] += 3.2 * severity + np.random.uniform(0.5, 1.5)
                    sound[idx] += 18.0 * severity
                    temp[idx] += 8.0 * severity
                elif mode == "thermal_runaway":
                    temp[idx] += 26.0 * severity + np.random.uniform(1.0, 4.0)
                    power[idx] += 12.0 * severity
                elif mode == "seal_leak":
                    pressure[idx] -= 22.0 * severity
                    power[idx] += 9.0 * severity
                    vibration[idx] += 1.6 * severity

        for i in range(n_samples_per_machine):
            all_records.append({
                "timestamp": timestamps[i].strftime("%Y-%m-%d %H:%M:%S"),
                "machine_id": machine_id,
                "equipment_type": profile["type"],
                "operating_hours": round(float(hours[i]), 1),
                "temperature_c": round(float(temp[i]), 2),
                "vibration_rms": round(max(0.1, float(vibration[i])), 3),
                "pressure_psi": round(max(5.0, float(pressure[i])), 2),
                "power_consumption_kw": round(max(1.0, float(power[i])), 2),
                "sound_level_db": round(max(30.0, float(sound[i])), 2),
                "rul_hours": round(float(rul_hours[i]), 1),
                "maintenance_required": int(failure_labels[i])
            })

    df = pd.DataFrame(all_records)
    return df


if __name__ == "__main__":
    print("[*] Generating synthetic telemetry dataset for campus machinery...")
    data = generate_synthetic_telemetry(n_samples_per_machine=1500)
    data.to_csv("campus_sensor_telemetry.csv", index=False)
    print(f"[+] Successfully generated {len(data)} records across {len(EQUIPMENT_PROFILES)} machines.")
    print(f"[+] Saved to campus_sensor_telemetry.csv")
    print(f"[+] Failure class distribution:\n{data['maintenance_required'].value_counts(normalize=True)}")
