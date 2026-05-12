# Data Drift Monitor Report
## Fraud Detection Model — Feature Distribution Analysis

### Methodology
Reference data: first 2,500 transactions (training period)
New data: second 2,500 transactions (monitoring period)
Test used: Kolmogorov-Smirnov two-sample test
Drift threshold: p-value < 0.05

### Results

| Feature | KS Statistic | P-Value | Drift Detected |
|---------|-------------|---------|----------------|
| V14 | 0.0164 | 0.8899 | No |
| V1 | 0.022 | 0.5807 | No |
| V4 | 0.0288 | 0.251 | No |
| V17 | 0.0192 | 0.7462 | No |
| V10 | 0.0232 | 0.5117 | No |
| V12 | 0.0176 | 0.8336 | No |
| Amount | 0.0236 | 0.4894 | No |

### Findings
- No significant drift detected across monitored features.
- Model inputs remain stable. No immediate action required.

### Recommendation
- Run this monitor monthly or after any major change in transaction patterns.
- If drift persists, retrain the model on more recent data.