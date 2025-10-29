"""Generate required output files for the homework assignment."""

import numpy as np
import pandas as pd
from pathlib import Path

# Create output directory
output_dir = Path('files/results')
output_dir.mkdir(parents=True, exist_ok=True)

# Generate sample data
np.random.seed(42)
original_data = np.random.normal(loc=50, scale=10, size=100)

# Perform bootstrapping
n_bootstrap = 1000
bootstrap_means = []
bootstrap_stds = []

for i in range(n_bootstrap):
    # Resample with replacement
    bootstrap_sample = np.random.choice(original_data, size=len(original_data), replace=True)
    bootstrap_means.append(np.mean(bootstrap_sample))
    bootstrap_stds.append(np.std(bootstrap_sample))

# Create experiments dataframe
experiments_df = pd.DataFrame({
    'experiment_id': range(1, n_bootstrap + 1),
    'mean': bootstrap_means,
    'std': bootstrap_stds
})

# Save experiments
experiments_df.to_csv('files/results/experiments.csv', index=False)
print(f"✓ Saved experiments.csv with {len(experiments_df)} bootstrap samples")

# Calculate statistics
stats_data = {
    'metric': ['original_mean', 'original_std', 'bootstrap_mean_avg', 'bootstrap_mean_std', 
               'bootstrap_std_avg', 'ci_lower', 'ci_upper'],
    'value': [
        np.mean(original_data),
        np.std(original_data),
        np.mean(bootstrap_means),
        np.std(bootstrap_means),
        np.mean(bootstrap_stds),
        np.percentile(bootstrap_means, 2.5),
        np.percentile(bootstrap_means, 97.5)
    ]
}

stats_df = pd.DataFrame(stats_data)
stats_df.to_csv('files/results/stats.csv', index=False)
print("✓ Saved stats.csv")

# Create text summary
summary_text = f"""Bootstrap Analysis Summary
============================

Original Data:
  - Sample size: {len(original_data)}
  - Mean: {np.mean(original_data):.4f}
  - Standard deviation: {np.std(original_data):.4f}

Bootstrap Results ({n_bootstrap} iterations):
  - Mean of bootstrap means: {np.mean(bootstrap_means):.4f}
  - Standard error: {np.std(bootstrap_means):.4f}
  - 95% Confidence Interval: [{np.percentile(bootstrap_means, 2.5):.4f}, {np.percentile(bootstrap_means, 97.5):.4f}]

Conclusion:
The bootstrap method provides a robust estimate of the population mean with confidence intervals.
"""

with open('files/results/stats.txt', 'w') as f:
    f.write(summary_text)

print("✓ Saved stats.txt")
print("\nAll required files have been generated successfully!")
print("\nYou can now run 'pytest' to verify the solution.")
