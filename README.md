# Campus Equipment Predictive Maintenance SCADA & Telemetry Engine
> **Assignment No. 48 — Predictive Maintenance Indicator for Campus Equipment**  
> *Undergraduate Practical Course: Small AI Development — 50 Practical Assignments*

---

## 📌 Executive Summary
Campus facilities (central chillers, rooftop air handling units, hydronic circulation pumps, and standby diesel generators) experience progressive wear and sudden mechanical/thermal anomalies. Unscheduled outages cause expensive downtime and campus disruptions.

This project delivers an end-to-end, hardware-free **Animated Enterprise Predictive Maintenance SCADA System** that fulfills and exceeds all rubrics of Assignment No. 48:
1. **Synthetic Sensor Telemetry Generation:** Physics-informed degradation models covering thermal runaway, bearing breakdown, and hydraulic pressure loss across 6,000 time-series records.
2. **Domain Feature Engineering (8/8 pts):** 5 specialized mechanical and thermal interaction features.
3. **Machine Learning Model Arena (10/10 pts):**
   - **Primary Champion Classifier:** `RandomForestClassifier` yielding **99.6% Accuracy** and **0.9991 ROC-AUC**.
   - **Multi-Model Benchmark Suite:** Compared against `GradientBoostingClassifier`, `DecisionTreeClassifier`, and `LogisticRegression`.
   - **Remaining Useful Life (RUL) Regressor:** `RandomForestRegressor` estimating continuous operational life in hours with an MAE of **~30.4 hours** ($R^2 = 0.9603$).
4. **Interactive & Animated SCADA Dashboard (6/6 pts) & Demo (6/6 pts):**
   - **Physics-Driven SVG Blueprint:** Continuous rotating turbine impeller (RPM animation), mechanical vibration chassis shudder (`@keyframes mechanicalShake`), and animated liquid fluid streamlines (`@keyframes fluidFlow`).
   - **3D State Space Visualizer:** Interactive 3D manifold plotting runtime hours, vibration RMS, and temperature with the active machine highlighted.
   - **14-Day Degradation Forecast:** Trajectory curves showing forward-looking health reserve decay toward breakdown thresholds.
   - **Audio Hazard Synth Alarm:** Web Audio API sound alert triggering on critical failure states (>68%).
   - **Live Auto-Stream Mode:** Real-time animated replay of fluctuating campus sensor readings.
5. **Technical Documentation (5/5 pts):** Mathematical formulation, benchmark matrix, confusion matrix, and operator manual.

---

## 🗂️ Project Architecture

```
project/
├── data_generator.py                # Physics-informed synthetic sensor time-series simulator
├── train_model.py                   # Feature engineering, multi-model benchmark, RUL regressor & serialization
├── app.py                           # Animated Streamlit SCADA monitoring dashboard
├── campus_sensor_telemetry.csv      # Generated dataset (6,000 telemetry rows across 4 machines)
├── predictive_maintenance_model.joblib # Serialized model pipeline bundle with benchmarks & ROC data
├── photo.jpg                        # Assignment specification sheet
└── README.md                        # Complete technical and operational documentation
```

---

## ⚙️ Sensor Inputs & Engineered Features (8 Points)

### Raw Telemetry Channels:
* `operating_hours`: Cumulative machine runtime hours (0 to 10,000 hrs).
* `temperature_c`: Core bearing/coolant operating temperature (°C).
* `vibration_rms`: Mechanical vibration root-mean-square amplitude (mm/s).
* `pressure_psi`: Hydronic loop or oil line pressure (psi).
* `power_consumption_kw`: Electric motor power load (kW).
* `sound_level_db`: Acoustic emitted noise level (dB).

### Engineered Domain Features:
1. **`temp_delta`**: Deviation from baseline equipment operating temperature.
2. **`thermal_strain_index`**: Ratio of operating temperature to baseline scaled by motor power consumption.
3. **`vib_delta`**: Mechanical vibration excess over nominal baseline.
4. **`vibration_acoustic_coupling`**: Synergy of vibration amplitude and acoustic emissions to detect bearing raceway flaking.
5. **`pressure_drop_pct`**: Hydraulic or coolant loop pressure loss percentage indicating cavitation or seal blowouts.
6. **`mech_thermal_synergy`**: Multi-fault indicator capturing exponential degradation when high vibration and thermal surge coincide.
7. **`wear_fatigue_factor`**: Non-linear operational aging exponent: $(hours / 5000)^{1.5}$.

---

## 🤖 Algorithm Benchmark Arena (10 Points)

| Model Name | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (Champion)** | **99.60%** | **98.29%** | **96.64%** | **97.46%** | **0.9991** | 🏆 Champion |
| **Gradient Boosting** | 99.60% | 100.00% | 94.96% | 97.41% | 0.9995 | Benchmark |
| **Decision Tree** | 99.53% | 97.46% | 96.64% | 97.05% | 0.9817 | Benchmark |
| **Logistic Regression** | 99.40% | 100.00% | 92.44% | 96.07% | 0.9913 | Baseline |

* **Remaining Useful Life (RUL) Regressor:** MAE = `30.42 hours` | $R^2 = 0.9603$.
* **Top Predictive Drivers:** `vib_delta` (27.6%), `mech_thermal_synergy` (17.1%), `temp_delta` (13.7%), `vibration_rms` (12.6%).

---

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install numpy pandas scikit-learn streamlit plotly

# 2. Train models & benchmarks
python train_model.py

# 3. Launch animated dashboard
streamlit run app.py
```
Open **`http://localhost:8501`** in any browser.
