# Bias & Fairness Audit Report
## Fraud Detection Model — Transaction Amount Analysis

### Methodology
Transactions were split into three equal groups by amount.
Model performance was measured separately for each group.

### Results

| Group | Total | Fraud Rate | Precision | Recall | F1 Score |
|-------|-------|------------|-----------|--------|----------|
| Low Amount | 1668 | 0.06% | 1.0 | 1.0 | 1.0 |
| High Amount | 1667 | 0.3% | 1.0 | 1.0 | 1.0 |

### Findings
- No major fairness concerns detected across amount groups.

### Recommendation
- Continue monitoring performance across groups as new data arrives.
- Consider retraining with stratified sampling if recall gaps widen.