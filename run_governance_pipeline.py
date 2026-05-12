# -*- coding: utf-8 -*-
# This is the Governance Pipeline Agent
# It runs all 5 modules in order, collects all outputs,
# checks for any issues, and writes a final governance summary report

import os
import json
import subprocess
import sys
from datetime import datetime

# ── CONFIGURATION ─────────────────────────────────────────────────
# These are the 5 modules in the order they should run
# Each entry has a name and the path to the script
MODULES = [
    {
        "name": "Module 1 — Model Card Generator",
        "script": "module_1_model_card/generate_model_card.py",
        "outputs": ["outputs/model_card.md"]
    },
    {
        "name": "Module 2 — SHAP Explainability Report",
        "script": "module_2_shap_explainability/generate_shap_report.py",
        "outputs": ["outputs/shap_importance.png", "outputs/shap_summary.png", "data/shap_top_features.json"]
    },
    {
        "name": "Module 3 — Bias & Fairness Audit",
        "script": "module_3_bias_fairness/bias_audit.py",
        "outputs": ["outputs/bias_audit.png", "outputs/bias_audit_report.md", "data/bias_audit_results.json"]
    },
    {
        "name": "Module 4 — Data Drift Monitor",
        "script": "module_4_data_drift/drift_monitor.py",
        "outputs": ["outputs/drift_monitor.png", "outputs/drift_report.md", "data/drift_results.json"]
    },
    {
        "name": "Module 5 — EU AI Act Risk Classifier",
        "script": "module_5_eu_ai_act/eu_ai_classifier.py",
        "outputs": ["outputs/eu_ai_act_report.md", "data/eu_ai_act_results.json"]
    }
]

# ── HELPER FUNCTIONS ───────────────────────────────────────────────
def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_step(text):
    print(f"\n>> {text}")

def print_pass(text):
    print(f"   [PASS] {text}")

def print_fail(text):
    print(f"   [FAIL] {text}")

def print_warn(text):
    print(f"   [WARN] {text}")

# ── STEP 1: BANNER ─────────────────────────────────────────────────
print_header("FinTech AI Model Risk Governance Framework")
print(f"  Pipeline Agent v1.0")
print(f"  Run date: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  Developed by: Amaan Najmi")
print("=" * 60)

# ── STEP 2: CHECK PREREQUISITES ───────────────────────────────────
# Before running anything, check that the key files exist
print_step("Checking prerequisites...")

prerequisites = [
    "data/fraud_model.pkl",
    "data/model_metrics.json",
    "data/sample.csv"
]

all_prereqs_met = True
for prereq in prerequisites:
    if os.path.exists(prereq):
        print_pass(f"Found: {prereq}")
    else:
        print_fail(f"Missing: {prereq} — run data/train_model.py first")
        all_prereqs_met = False

if not all_prereqs_met:
    print("\nPrerequisites not met. Please run data/train_model.py first.")
    sys.exit(1)

# ── STEP 3: RUN ALL MODULES IN ORDER ──────────────────────────────
# We keep track of which modules passed and which failed
results = []

for i, module in enumerate(MODULES, 1):
    print_step(f"Running {module['name']}...")

    # Run the module script as a subprocess
    # This is the same as typing 'python script.py' in the terminal
    result = subprocess.run(
        [sys.executable, module["script"]],
        capture_output=True,
        text=True
    )

    # Check if the script ran without errors
    if result.returncode == 0:
        print_pass(f"{module['name']} completed successfully")

        # Check that all expected output files were actually created
        all_outputs_exist = True
        for output in module["outputs"]:
            if os.path.exists(output):
                print_pass(f"Output created: {output}")
            else:
                print_fail(f"Output missing: {output}")
                all_outputs_exist = False

        results.append({
            "module": module["name"],
            "status": "PASS" if all_outputs_exist else "PARTIAL",
            "error": None
        })
    else:
        # If the script failed, capture the error message
        print_fail(f"{module['name']} failed")
        print(f"   Error: {result.stderr[-300:] if result.stderr else 'Unknown error'}")
        results.append({
            "module": module["name"],
            "status": "FAIL",
            "error": result.stderr[-300:] if result.stderr else "Unknown error"
        })

# ── STEP 4: READ KEY RESULTS FOR SUMMARY ──────────────────────────
# We read the JSON outputs from each module to include in the summary
print_step("Reading governance results...")

# Load model metrics
try:
    with open("data/model_metrics.json") as f:
        metrics = json.load(f)
except:
    metrics = {}

# Load bias audit results
try:
    with open("data/bias_audit_results.json") as f:
        bias_results = json.load(f)
    bias_concerns = [r for r in bias_results if r.get("recall", 1) < 0.7]
except:
    bias_results = []
    bias_concerns = []

# Load drift results
try:
    with open("data/drift_results.json") as f:
        drift_results = json.load(f)
    drift_alerts = [r for r in drift_results if r.get("drift_detected")]
except:
    drift_results = []
    drift_alerts = []

# Load EU AI Act results
try:
    with open("data/eu_ai_act_results.json") as f:
        eu_results = json.load(f)
    eu_status = eu_results.get("overall_status", "UNKNOWN")
    eu_risk = eu_results.get("risk_level", "UNKNOWN")
except:
    eu_status = "UNKNOWN"
    eu_risk = "UNKNOWN"

# Load SHAP top features
try:
    with open("data/shap_top_features.json") as f:
        shap_features = json.load(f)
    top_feature = list(shap_features.keys())[0] if shap_features else "Unknown"
except:
    top_feature = "Unknown"

# ── STEP 5: GENERATE FINAL SUMMARY REPORT ─────────────────────────
print_step("Generating final governance summary report...")

passed = len([r for r in results if r["status"] == "PASS"])
failed = len([r for r in results if r["status"] == "FAIL"])
partial = len([r for r in results if r["status"] == "PARTIAL"])

# Determine overall governance health
if failed == 0 and len(drift_alerts) == 0 and len(bias_concerns) == 0:
    overall_health = "HEALTHY"
elif failed == 0 and (len(drift_alerts) > 0 or len(bias_concerns) > 0):
    overall_health = "ATTENTION REQUIRED"
else:
    overall_health = "ACTION REQUIRED"

# Build the summary report
summary_lines = [
    "# Governance Pipeline Summary Report",
    f"**Run Date:** {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}",
    f"**Model:** Credit Card Fraud Detection Classifier v1.0",
    f"**Developer:** Amaan Najmi\n",
    "---\n",
    f"## Overall Governance Health: {overall_health}\n",
    "## Pipeline Execution Summary\n",
    "| Module | Status |",
    "|--------|--------|"
]

for r in results:
    summary_lines.append(f"| {r['module']} | {r['status']} |")

summary_lines.append("\n## Model Performance\n")
summary_lines.append("| Metric | Score |")
summary_lines.append("|--------|-------|")
for metric, value in metrics.items():
    summary_lines.append(f"| {metric} | {value} |")

summary_lines.append(f"\n## Key Governance Findings\n")
summary_lines.append(f"- **Primary fraud signal:** {top_feature} (SHAP analysis)")
summary_lines.append(f"- **Bias concerns detected:** {'Yes — ' + str(len(bias_concerns)) + ' group(s)' if bias_concerns else 'None'}")
summary_lines.append(f"- **Data drift detected:** {'Yes — ' + str(len(drift_alerts)) + ' feature(s)' if drift_alerts else 'None'}")
summary_lines.append(f"- **EU AI Act risk level:** {eu_risk}")
summary_lines.append(f"- **EU AI Act compliance status:** {eu_status}")

summary_lines.append(f"\n## Recommendations\n")
if drift_alerts:
    summary_lines.append(f"- URGENT: Drift detected in {len(drift_alerts)} feature(s). Review model retraining.")
else:
    summary_lines.append("- No drift detected. Schedule next drift check in 30 days.")

if bias_concerns:
    summary_lines.append(f"- URGENT: Bias concerns in {len(bias_concerns)} group(s). Review training data.")
else:
    summary_lines.append("- No fairness concerns detected. Continue monitoring.")

summary_lines.append("- Ensure EU AI Act database registration before any EU deployment.")
summary_lines.append(f"\n---")
summary_lines.append(f"*Generated automatically by the FinTech AI Model Risk Governance Framework*")

summary_text = "\n".join(summary_lines)

with open("outputs/governance_summary.md", "w", encoding="utf-8") as f:
    f.write(summary_text)

# ── STEP 6: PRINT FINAL STATUS ─────────────────────────────────────
print_header("GOVERNANCE PIPELINE COMPLETE")
print(f"  Overall Health:     {overall_health}")
print(f"  Modules Passed:     {passed}/5")
print(f"  Drift Alerts:       {len(drift_alerts)}")
print(f"  Bias Concerns:      {len(bias_concerns)}")
print(f"  EU AI Act Status:   {eu_status}")
print(f"  EU AI Act Risk:     {eu_risk}")
print("=" * 60)
print(f"\n  Full summary saved to: outputs/governance_summary.md")
print(f"\n  All outputs saved to:  outputs/")
print("\n" + "=" * 60)