import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

def compute_order_flow(df, levels=10):
    df = df.copy()
    for m in range(levels):
        bp, bs = f'bid_px_0{m}', f'bid_sz_0{m}'
        ap, aqs = f'ask_px_0{m}', f'ask_sz_0{m}'
        bid_of, ask_of = [0], [0]

        for i in range(1, len(df)):
            # bid
            p_now, p_prev = df.loc[i, bp], df.loc[i-1, bp]
            q_now, q_prev = df.loc[i, bs], df.loc[i-1, bs]
            bid_of.append(q_now if p_now > p_prev else q_now - q_prev if p_now == p_prev else -q_now)

            # ask
            p_now, p_prev = df.loc[i, ap], df.loc[i-1, ap]
            q_now, q_prev = df.loc[i, aqs], df.loc[i-1, aqs]
            ask_of.append(-q_now if p_now > p_prev else q_now - q_prev if p_now == p_prev else q_now)

        df[f'of_bid_{m}'] = bid_of
        df[f'of_ask_{m}'] = ask_of
        df[f'ofi_{m}'] = df[f'of_bid_{m}'] - df[f'of_ask_{m}']
    return df


def compute_rolling_ofi(df, levels=10, interval='10S'):
    df = df.copy()
    df['ts_recv'] = pd.to_datetime(df['ts_recv'])
    df.set_index('ts_recv', inplace=True)

    ofi_cols = [f'ofi_{m}' for m in range(levels)]
    bid_cols = [f'of_bid_{m}' for m in range(levels)]
    ask_cols = [f'of_ask_{m}' for m in range(levels)]

    ofi_agg = df[ofi_cols].resample(interval, closed='right', label='right').sum()
    bid_ask_sum = df[bid_cols + ask_cols].resample(interval).sum()
    event_counts = df.resample(interval).size()

    Q_values = []
    for i in range(len(bid_ask_sum)):
        row, delta_N = bid_ask_sum.iloc[i], event_counts.iloc[i]
        q_sum = sum(row[f'of_bid_{m}'] + row[f'of_ask_{m}'] for m in range(levels))
        Q_M_h = q_sum / (2 * delta_N * levels) if delta_N > 0 else np.nan
        Q_values.append(Q_M_h)

    Q_series = pd.Series(Q_values, index=ofi_agg.index, name='Q_M_h')
    deeper_ofi = ofi_agg.div(Q_series, axis=0)
    deeper_ofi.columns = [f'deep_ofi_{m}' for m in range(levels)]
    best_ofi = ofi_agg['ofi_0'].rename('best_level_ofi')

    result = pd.concat([
        ofi_agg.index.to_series().rename('timestamp'),
        best_ofi,
        deeper_ofi,
        Q_series
    ], axis=1).reset_index(drop=True)

    return result


def compute_integrated_ofi(df, levels=10):
    deep_ofi_cols = [f'deep_ofi_{m}' for m in range(levels)]
    X = df[deep_ofi_cols].dropna().values
    pca = PCA(n_components=1)
    pca.fit(X)
    w1 = pca.components_[0]
    w1_normalized = w1 / np.sum(np.abs(w1))
    df.loc[~df[deep_ofi_cols].isnull().any(axis=1), 'integrated_ofi'] = X @ w1_normalized
    return df, w1_normalized
