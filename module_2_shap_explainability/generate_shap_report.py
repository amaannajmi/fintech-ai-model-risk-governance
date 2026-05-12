# -*- coding: utf-8 -*-
# This script does three things:
# 1. Loads the trained fraud detection model
# 2. Runs SHAP to explain why the model makes each decision
# 3. Saves charts and a summary report to the outputs folder

import shap
import pickle
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ── STEP 1: LOAD THE TRAINED MODEL ────────────────────────────────
# We saved this model in Session 3 as a .pkl file
# Now we load it back so we can explain its decisions
print("Loading model...")
with open("data/fraud_model.pkl", "rb") as f:
    model = pickle.load(f)

# ── STEP 2: LOAD THE SAMPLE DATASET ───────────────────────────────
# We use the 5,000 row sample we created earlier
# We drop 'Time' and 'Class' just like we did when training
print("Loading data...")
data = pd.read_csv("data/sample.csv")
X = data.drop(["Class", "Time"], axis=1)

# ── STEP 3: TAKE A SMALL SUBSET FOR SHAP ──────────────────────────
# SHAP can be slow on large datasets
# 500 rows is enough to get reliable explanations
X_sample = X.sample(n=500, random_state=42)

# ── STEP 4: CREATE THE SHAP EXPLAINER ─────────────────────────────
# TreeExplainer is designed specifically for Random Forest models
# It is fast and accurate for tree-based models
print("Running SHAP analysis... this may take a minute.")
explainer = shap.TreeExplainer(model)

# This calculates SHAP values for every row in our sample
# Each SHAP value tells us how much each feature contributed
# to pushing the prediction towards fraud or away from fraud
shap_values = explainer.shap_values(X_sample)

# Random Forest returns shap_values as a 3D array in newer versions of SHAP
# We check the format and handle both cases
if isinstance(shap_values, list):
    shap_fraud = shap_values[1]
else:
    shap_fraud = shap_values[:, :, 1]

# ── STEP 5: SAVE CHART 1 — SUMMARY BAR CHART ──────────────────────
# This chart shows the TOP features that matter most overall
# The longer the bar, the more important that feature is
print("Saving charts...")
plt.figure()
shap.summary_plot(
    shap_fraud,
    X_sample,
    plot_type="bar",
    show=False  # Don't show on screen, just save to file
)
plt.title("SHAP Feature Importance - Fraud Detection Model")
plt.tight_layout()
plt.savefig("outputs/shap_importance.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: outputs/shap_importance.png")

# ── STEP 6: SAVE CHART 2 — DETAILED DOT PLOT ──────────────────────
# This chart shows MORE detail — not just which features matter
# but HOW they affect the prediction
# Red dots = high feature value, Blue dots = low feature value
# Dots on the right = pushed towards fraud
# Dots on the left = pushed away from fraud
plt.figure()
shap.summary_plot(
    shap_fraud,
    X_sample,
    show=False
)
plt.title("SHAP Summary Plot - Fraud Detection Model")
plt.tight_layout()
plt.savefig("outputs/shap_summary.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: outputs/shap_summary.png")

# ── STEP 7: SAVE TOP FEATURES TO JSON ─────────────────────────────
# We calculate the average importance of each feature
# and save the top 10 to a JSON file
# This will be used later to update the Model Card automatically
mean_shap = np.abs(shap_fraud).mean(axis=0)
feature_importance = dict(zip(X_sample.columns, mean_shap))
top_10 = dict(sorted(feature_importance.items(),
                     key=lambda x: x[1], reverse=True)[:10])

with open("data/shap_top_features.json", "w") as f:
    json.dump({k: round(float(v), 4) for k, v in top_10.items()}, f, indent=4)

print("Saved: data/shap_top_features.json")

# ── STEP 8: PRINT SUMMARY ─────────────────────────────────────────
print("\nTop 10 most important features for fraud detection:")
for feature, importance in top_10.items():
    print(f"  {feature}: {importance}")

print("\nSHAP analysis complete.")