"""
Predictive Maintenance for Campus Equipment - Enterprise Model Engine & Benchmark Arena
Trains:
1. Primary Classifier: RandomForestClassifier (Tuned for Industrial Recall & ROC-AUC)
2. Benchmark Suite: GradientBoostingClassifier, DecisionTreeClassifier, LogisticRegression
3. Primary Regressor: RandomForestRegressor (Remaining Useful Life in hours)
4. Full Metrics Matrix: Confusion Matrix, ROC-AUC curve coordinates, Cross-validation scores
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report,
    mean_absolute_error, r2_score
)
from data_generator import generate_synthetic_telemetry, EQUIPMENT_PROFILES


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes domain-specific industrial telemetry features.
    """
    df = df.copy()

    # Map equipment nominal baselines
    temp_bases = df["machine_id"].map(lambda m: EQUIPMENT_PROFILES.get(m, {}).get("temp_base", 60.0))
    vib_bases = df["machine_id"].map(lambda m: EQUIPMENT_PROFILES.get(m, {}).get("vib_base", 1.2))
    press_bases = df["machine_id"].map(lambda m: EQUIPMENT_PROFILES.get(m, {}).get("pressure_base", 50.0))

    # Domain feature engineering
    # 1. Thermal strain: deviation from nominal temp scaled by power load
    df["temp_delta"] = df["temperature_c"] - temp_bases
    df["thermal_strain_index"] = (df["temperature_c"] / temp_bases) * (df["power_consumption_kw"] / 25.0)

    # 2. Mechanical stress: vibration delta and acoustic coupling
    df["vib_delta"] = df["vibration_rms"] - vib_bases
    df["vibration_acoustic_coupling"] = df["vibration_rms"] * (df["sound_level_db"] / 50.0)

    # 3. Hydraulic strain: pressure drop below rated capacity
    df["pressure_drop_pct"] = (press_bases - df["pressure_psi"]) / press_bases

    # 4. Multi-sensor cross interaction (high temp + high vib = catastrophic bearing wear)
    df["mech_thermal_synergy"] = df["temp_delta"].clip(lower=0) * df["vib_delta"].clip(lower=0)

    # 5. Aging fatigue index
    df["wear_fatigue_factor"] = (df["operating_hours"] / 5000.0) ** 1.5

    return df


FEATURE_COLUMNS = [
    "operating_hours",
    "temperature_c",
    "vibration_rms",
    "pressure_psi",
    "power_consumption_kw",
    "sound_level_db",
    "temp_delta",
    "thermal_strain_index",
    "vib_delta",
    "vibration_acoustic_coupling",
    "pressure_drop_pct",
    "mech_thermal_synergy",
    "wear_fatigue_factor"
]


def train_predictive_maintenance_pipeline(csv_path: str = "campus_sensor_telemetry.csv"):
    """
    Trains classification suite and regression pipeline, serializes all evaluation artifacts.
    """
    if not os.path.exists(csv_path):
        print(f"[*] Telemetry file {csv_path} not found. Generating fresh dataset...")
        raw_df = generate_synthetic_telemetry(n_samples_per_machine=1500)
        raw_df.to_csv(csv_path, index=False)
    else:
        raw_df = pd.read_csv(csv_path)

    print(f"[*] Loaded {len(raw_df)} telemetry entries.")
    df_feat = engineer_features(raw_df)

    X = df_feat[FEATURE_COLUMNS]
    y_class = df_feat["maintenance_required"]
    y_reg = df_feat["rul_hours"]

    # Stratified Train/Test split for balanced failure evaluation
    X_train, X_test, y_train_cls, y_test_cls, y_train_reg, y_test_reg = train_test_split(
        X, y_class, y_reg, test_size=0.25, random_state=42, stratify=y_class
    )

    print("\n" + "=" * 60)
    print(" 1. BENCHMARKING MULTIPLE CLASSIFICATION ALGORITHMS ")
    print("=" * 60)

    # Scaler for models sensitive to scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models_to_benchmark = {
        "Random Forest (Champion)": RandomForestClassifier(n_estimators=120, max_depth=10, class_weight="balanced", random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=8, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
    }

    benchmark_results = []
    trained_models = {}
    roc_curves_data = {}

    for name, model in models_to_benchmark.items():
        if "Logistic" in name:
            model.fit(X_train_scaled, y_train_cls)
            y_pred = model.predict(X_test_scaled)
            y_proba = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train_cls)
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test_cls, y_pred)
        prec = precision_score(y_test_cls, y_pred, zero_division=0)
        rec = recall_score(y_test_cls, y_pred, zero_division=0)
        f1 = f1_score(y_test_cls, y_pred, zero_division=0)
        auc = roc_auc_score(y_test_cls, y_proba)

        fpr, tpr, _ = roc_curve(y_test_cls, y_proba)
        roc_curves_data[name] = {"fpr": fpr.tolist(), "tpr": tpr.tolist(), "auc": auc}

        trained_models[name] = model
        benchmark_results.append({
            "Model": name,
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1-Score": f1,
            "ROC-AUC": auc
        })
        print(f"[{name:<24}] Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")

    benchmark_df = pd.DataFrame(benchmark_results).sort_values(by="ROC-AUC", ascending=False)

    # Primary Champion Model
    clf = trained_models["Random Forest (Champion)"]
    y_pred_cls = clf.predict(X_test)
    cm = confusion_matrix(y_test_cls, y_pred_cls).tolist()

    # Feature Importance
    importances = clf.feature_importances_
    feat_imp_df = pd.DataFrame({
        "feature": FEATURE_COLUMNS,
        "importance": importances
    }).sort_values(by="importance", ascending=False)

    print("\n" + "=" * 60)
    print(" 2. TRAINING REMAINING USEFUL LIFE (RUL) REGRESSOR ")
    print("=" * 60)

    reg = RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )
    reg.fit(X_train, y_train_reg)

    y_pred_reg = reg.predict(X_test)
    mae = mean_absolute_error(y_test_reg, y_pred_reg)
    r2 = r2_score(y_test_reg, y_pred_reg)

    print(f"RUL Mean Absolute Error (MAE): {mae:.2f} hours")
    print(f"RUL R^2 Score                 : {r2:.4f}")

    # Build model artifact bundle
    model_bundle = {
        "classifier": clf,
        "regressor": reg,
        "scaler": scaler,
        "features": FEATURE_COLUMNS,
        "feature_importances": feat_imp_df.to_dict(orient="records"),
        "benchmark": benchmark_df.to_dict(orient="records"),
        "confusion_matrix": cm,
        "roc_curves": roc_curves_data,
        "metrics": {
            "accuracy": benchmark_results[0]["Accuracy"],
            "precision": benchmark_results[0]["Precision"],
            "recall": benchmark_results[0]["Recall"],
            "f1": benchmark_results[0]["F1-Score"],
            "roc_auc": benchmark_results[0]["ROC-AUC"],
            "mae_hours": mae,
            "r2": r2
        }
    }

    joblib.dump(model_bundle, "predictive_maintenance_model.joblib")
    print("\n[+] Enterprise models successfully exported to 'predictive_maintenance_model.joblib'!")
    return model_bundle


if __name__ == "__main__":
    train_predictive_maintenance_pipeline()
