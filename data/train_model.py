# -*- coding: utf-8 -*-
# This script does three things:
# 1. Loads the real Kaggle credit card fraud dataset
# 2. Trains a real classification model on it
# 3. Saves the model and its performance metrics so other modules can use them

import os
import pickle
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score, roc_auc_score)

# ── STEP 1: LOAD THE REAL DATASET ─────────────────────────────────
# We are loading the CSV file from the data folder
# This dataset has 284,807 real credit card transactions
# 492 of them are fraud - that is only 0.17% which is very imbalanced
print("Loading dataset...")
data = pd.read_csv("data/creditcard.csv")

print(f"Dataset loaded. Total transactions: {len(data)}")
print(f"Fraud cases: {data['Class'].sum()}")
print(f"Legitimate cases: {(data['Class'] == 0).sum()}")

# ── STEP 2: SEPARATE FEATURES AND LABEL ───────────────────────────
# 'Class' is the column we want to predict - 1 means fraud, 0 means legitimate
# We drop 'Time' as it is not useful for prediction
X = data.drop(["Class", "Time"], axis=1)  # Features
y = data["Class"]                          # Label

# ── STEP 3: SPLIT INTO TRAINING AND TESTING DATA ──────────────────
# 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# stratify=y makes sure both splits have the same ratio of fraud to legitimate

print("\nTraining model... this may take a minute.")

# ── STEP 4: TRAIN THE MODEL ────────────────────────────────────────
# We use 50 trees instead of 100 to keep it faster on a large dataset
model = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
# n_jobs=-1 means use all your CPU cores to speed up training
model.fit(X_train, y_train)

# ── STEP 5: MEASURE REAL PERFORMANCE ──────────────────────────────
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

metrics = {
    "accuracy": round(accuracy_score(y_test, y_pred), 4),
    "precision": round(precision_score(y_test, y_pred), 4),
    "recall": round(recall_score(y_test, y_pred), 4),
    "f1_score": round(f1_score(y_test, y_pred), 4),
    "roc_auc": round(roc_auc_score(y_test, y_prob), 4)
}

print("\nModel training complete. Real performance metrics:")
for metric, value in metrics.items():
    print(f"  {metric}: {value}")

# ── STEP 6: SAVE THE MODEL AND METRICS ────────────────────────────
with open("data/fraud_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("data/model_metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("\nModel saved to: data/fraud_model.pkl")
print("Metrics saved to: data/model_metrics.json")