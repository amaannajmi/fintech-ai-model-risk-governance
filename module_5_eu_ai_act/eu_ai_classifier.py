# -*- coding: utf-8 -*-
# This script classifies an AI model under the EU AI Act
# It asks a series of questions about the model and its use case
# and automatically determines the risk level and legal obligations

import json
from datetime import datetime

# ── STEP 1: DEFINE THE MODEL PROFILE ──────────────────────────────
# This is where we describe our fraud detection model
# and its context so the classifier can assess it correctly
# Each field maps to a specific criterion in the EU AI Act

model_profile = {
    "model_name": "Credit Card Fraud Detection Classifier",
    "version": "1.0",
    "developer": "Amaan Najmi",
    "date": datetime.today().strftime("%Y-%m-%d"),

    # Does this model affect people's access to financial services?
    "affects_financial_services": True,

    # Does this model make or influence decisions about individuals?
    "affects_individuals": True,

    # Is this model used in a safety-critical system?
    "safety_critical": False,

    # Does this model use biometric data?
    "uses_biometric_data": False,

    # Is this model used for social scoring by a government?
    "social_scoring": False,

    # Does this model exploit vulnerable groups?
    "exploits_vulnerable": False,

    # Is this model used for real-time remote biometric identification?
    "biometric_identification": False,

    # Does this model operate in education, employment, or law enforcement?
    "sensitive_sector": False,

    # Is there a human reviewing the model's decisions before action is taken?
    "human_oversight": True,

    # Is the model's decision-making process explainable?
    "explainable": True,

    # Has the model been tested for bias and fairness?
    "bias_tested": True,

    # Is there documentation describing the model?
    "documented": True,

    # Is there a system to monitor the model after deployment?
    "monitored": True
}

# ── STEP 2: CLASSIFICATION LOGIC ──────────────────────────────────
# The EU AI Act has 4 risk levels:
# 1. UNACCEPTABLE — banned outright (e.g. social scoring, subliminal manipulation)
# 2. HIGH — heavily regulated (e.g. credit decisions, employment, law enforcement)
# 3. LIMITED — some transparency obligations (e.g. chatbots)
# 4. MINIMAL — no specific obligations (e.g. spam filters, recommendation systems)

def classify_risk(profile):
    """
    Classifies an AI model under the EU AI Act.
    Returns risk level, reasoning, and list of obligations.
    """

    # Check for UNACCEPTABLE risk first — these are banned
    if profile["social_scoring"]:
        return "UNACCEPTABLE", "Model performs social scoring by public authorities.", []

    if profile["exploits_vulnerable"]:
        return "UNACCEPTABLE", "Model exploits vulnerable groups.", []

    if profile["biometric_identification"]:
        return "UNACCEPTABLE", "Model performs real-time biometric identification in public spaces.", []

    # Check for HIGH risk
    # Financial services AI that affects individuals is HIGH risk under Annex III
    if profile["affects_financial_services"] and profile["affects_individuals"]:
        reasoning = (
            "Model operates in financial services and affects individual outcomes. "
            "Under EU AI Act Annex III, AI systems used in creditworthiness assessment "
            "and fraud detection that affect individuals are classified as HIGH RISK."
        )
        obligations = [
            "Establish a risk management system",
            "Ensure data governance and training data quality",
            "Produce technical documentation",
            "Enable automatic logging of events (audit trail)",
            "Provide transparency to affected individuals",
            "Ensure human oversight of model decisions",
            "Achieve appropriate accuracy, robustness and cybersecurity",
            "Register the system in the EU AI Act database before deployment"
        ]
        return "HIGH", reasoning, obligations

    # Check for LIMITED risk
    if profile["affects_individuals"]:
        reasoning = "Model interacts with or affects individuals but does not meet HIGH risk criteria."
        obligations = [
            "Inform individuals they are interacting with an AI system",
            "Maintain basic transparency obligations"
        ]
        return "LIMITED", reasoning, obligations

    # Default to MINIMAL risk
    reasoning = "Model does not meet criteria for higher risk categories."
    obligations = [
        "No specific EU AI Act obligations — follow general best practices"
    ]
    return "MINIMAL", reasoning, obligations

# ── STEP 3: RUN THE CLASSIFICATION ────────────────────────────────
print("Running EU AI Act Risk Classification...")
print(f"Model: {model_profile['model_name']}")
print("-" * 50)

risk_level, reasoning, obligations = classify_risk(model_profile)

print(f"\nRISK LEVEL: {risk_level}")
print(f"\nReasoning: {reasoning}")

print("\nLegal Obligations:")
for i, obligation in enumerate(obligations, 1):
    print(f"  {i}. {obligation}")

# ── STEP 4: CHECK COMPLIANCE STATUS ───────────────────────────────
# We check whether our model already meets the key obligations
# based on what we have built in this project

print("\nCompliance Status Check:")
compliance_checks = {
    "Technical documentation": model_profile["documented"],
    "Explainability (SHAP)": model_profile["explainable"],
    "Bias and fairness testing": model_profile["bias_tested"],
    "Human oversight": model_profile["human_oversight"],
    "Post-deployment monitoring": model_profile["monitored"]
}

all_compliant = True
for check, status in compliance_checks.items():
    icon = "PASS" if status else "FAIL"
    print(f"  [{icon}] {check}")
    if not status:
        all_compliant = False

overall = "COMPLIANT" if all_compliant else "PARTIALLY COMPLIANT - ACTION REQUIRED"
print(f"\nOverall Status: {overall}")

# ── STEP 5: SAVE RESULTS TO JSON ──────────────────────────────────
results = {
    "model_name": model_profile["model_name"],
    "version": model_profile["version"],
    "date": model_profile["date"],
    "risk_level": risk_level,
    "reasoning": reasoning,
    "obligations": obligations,
    "compliance_checks": compliance_checks,
    "overall_status": overall
}

with open("data/eu_ai_act_results.json", "w") as f:
    json.dump(results, f, indent=4)
print("\nSaved: data/eu_ai_act_results.json")

# ── STEP 6: GENERATE TEXT REPORT ──────────────────────────────────
summary_lines = [
    "# EU AI Act Risk Classification Report",
    f"## {model_profile['model_name']} v{model_profile['version']}",
    f"**Date:** {model_profile['date']}",
    f"**Developer:** {model_profile['developer']}\n",
    "---\n",
    f"## Risk Level: {risk_level}\n",
    "### Reasoning",
    f"{reasoning}\n",
    "### Legal Obligations Under the EU AI Act",
]

for i, obligation in enumerate(obligations, 1):
    summary_lines.append(f"{i}. {obligation}")

summary_lines.append("\n### Compliance Status\n")
summary_lines.append("| Requirement | Status |")
summary_lines.append("|-------------|--------|")

for check, status in compliance_checks.items():
    icon = "PASS" if status else "FAIL"
    summary_lines.append(f"| {check} | {icon} |")

summary_lines.append(f"\n**Overall Status: {overall}**")

summary_lines.append("\n### What This Means")
summary_lines.append(
    "This model is classified as HIGH RISK under the EU AI Act. "
    "It must meet all obligations listed above before deployment "
    "in the European Union. The compliance checks above show "
    "which obligations have already been addressed through this "
    "governance framework."
)

summary_text = "\n".join(summary_lines)

with open("outputs/eu_ai_act_report.md", "w", encoding="utf-8") as f:
    f.write(summary_text)

print("Saved: outputs/eu_ai_act_report.md")
print("\nEU AI Act classification complete.")