# -*- coding: utf-8 -*-
# This script detects data drift between a reference dataset and new data
# It uses statistical tests to check if the distribution of each feature
# has changed significantly — which would mean the model may need retraining

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# ── STEP 1: LOAD THE REFERENCE DATA ───────────────────────────────
# The reference data is what the model was originally trained on
# We use the first 2,500 rows of our sample as the "historical" data
print("Loading reference data...")
data = pd.read_csv("data/sample.csv")

# Split into reference (first half) and new data (second half)
# This simulates what would happen in production:
# reference = data from when model was trained
# new_data = data coming in today
reference = data.iloc[:2500].copy()
new_data = data.iloc[2500:].copy()

print(f"Reference data: {len(reference)} transactions")
print(f"New data: {len(new_data)} transactions")

# ── STEP 2: SELECT FEATURES TO MONITOR ────────────────────────────
# We monitor the most important features identified by SHAP
# Plus the transaction amount which is always worth watching
features_to_monitor = ["V14", "V1", "V4", "V17", "V10", "V12", "Amount"]

# ── STEP 3: RUN STATISTICAL DRIFT TEST ────────────────────────────
# We use the Kolmogorov-Smirnov (KS) test for each feature
# This test compares two distributions and tells us:
# - KS Statistic: how different are the two distributions? (0 = identical, 1 = completely different)
# - P-value: how confident are we that the difference is real and not random?
# If p-value < 0.05, we flag it as drift — the difference is statistically significant

print("\nRunning drift detection tests...")
print(f"{'Feature':<12} {'KS Statistic':<15} {'P-Value':<12} {'Drift Detected'}")
print("-" * 55)

results = []

for feature in features_to_monitor:
    ref_values = reference[feature].dropna()
    new_values = new_data[feature].dropna()
    
    # Run the KS test
    ks_stat, p_value = stats.ks_2samp(ref_values, new_values)
    
    # Flag as drift if p-value is below 0.05
    drift_detected = p_value < 0.05
    
    results.append({
        "feature": feature,
        "ks_statistic": round(float(ks_stat), 4),
        "p_value": round(float(p_value), 4),
        "drift_detected": bool(drift_detected)
    })
    
    status = "YES - ALERT" if drift_detected else "No"
    print(f"{feature:<12} {ks_stat:<15.4f} {p_value:<12.4f} {status}")

# ── STEP 4: SAVE RESULTS TO JSON ──────────────────────────────────
with open("data/drift_results.json", "w") as f:
    json.dump(results, f, indent=4)
print("\nSaved: data/drift_results.json")

# ── STEP 5: CREATE DRIFT CHART ─────────────────────────────────────
# We create a bar chart showing the KS statistic for each feature
# The red line at 0.05 is the drift threshold
# Any bar above the line means drift has been detected

features = [r["feature"] for r in results]
ks_stats = [r["ks_statistic"] for r in results]
colours = ["#FF5722" if r["drift_detected"] else "#2196F3" for r in results]

plt.figure(figsize=(10, 6))
bars = plt.bar(features, ks_stats, color=colours)

# Add the threshold line
plt.axhline(y=0.05, color="red", linestyle="--",
            linewidth=1.5, label="Drift threshold (p=0.05)")

# Add value labels on bars
for bar, val in zip(bars, ks_stats):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
             f"{val:.4f}", ha="center", va="bottom", fontsize=9)

plt.xlabel("Feature")
plt.ylabel("KS Statistic")
plt.title("Data Drift Monitor — Feature Distribution Comparison")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/drift_monitor.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: outputs/drift_monitor.png")

# ── STEP 6: GENERATE TEXT REPORT ──────────────────────────────────
print("\nGenerating drift report...")

drifted = [r for r in results if r["drift_detected"]]
stable = [r for r in results if not r["drift_detected"]]

summary_lines = [
    "# Data Drift Monitor Report",
    "## Fraud Detection Model — Feature Distribution Analysis\n",
    "### Methodology",
    "Reference data: first 2,500 transactions (training period)",
    "New data: second 2,500 transactions (monitoring period)",
    "Test used: Kolmogorov-Smirnov two-sample test",
    "Drift threshold: p-value < 0.05\n",
    "### Results\n",
    "| Feature | KS Statistic | P-Value | Drift Detected |",
    "|---------|-------------|---------|----------------|"
]

for r in results:
    status = "YES - ALERT" if r["drift_detected"] else "No"
    summary_lines.append(
        f"| {r['feature']} | {r['ks_statistic']} | "
        f"{r['p_value']} | {status} |"
    )

summary_lines.append("\n### Findings")

if drifted:
    summary_lines.append(
        f"- Drift detected in {len(drifted)} feature(s): "
        f"{', '.join([r['feature'] for r in drifted])}"
    )
    summary_lines.append(
        "- These features have changed significantly since training."
    )
    summary_lines.append(
        "- Model retraining or recalibration is recommended."
    )
else:
    summary_lines.append(
        "- No significant drift detected across monitored features."
    )
    summary_lines.append(
        "- Model inputs remain stable. No immediate action required."
    )

summary_lines.append("\n### Recommendation")
summary_lines.append(
    "- Run this monitor monthly or after any major change in transaction patterns."
)
summary_lines.append(
    "- If drift persists, retrain the model on more recent data."
)

summary_text = "\n".join(summary_lines)

with open("outputs/drift_report.md", "w", encoding="utf-8") as f:
    f.write(summary_text)

print("Saved: outputs/drift_report.md")
print("\nData drift monitoring complete.")