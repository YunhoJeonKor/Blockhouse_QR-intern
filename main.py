import pandas as pd
from ofi_utils import compute_order_flow, compute_rolling_ofi, compute_integrated_ofi

# Load your data
df = pd.read_csv('first_25000_rows.csv')
df['ts_recv'] = pd.to_datetime(df['ts_recv'])
df['ts_event'] = pd.to_datetime(df['ts_event'])

# 1. Compute Order Flow
df_with_ofi = compute_order_flow(df)

# 2. Aggregate into 10s windows
df_with_deep = compute_rolling_ofi(df_with_ofi)

# 3. Compute Integrated OFI using PCA
df_final, w1_vector = compute_integrated_ofi(df_with_deep)

# Save result
df_final.to_csv('ofi_features_output.csv', index=False)
