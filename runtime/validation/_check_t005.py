import json, pandas as pd

with open('runtime/benchmarks/oos_errors.json') as f:
    oos_bm = json.load(f)
with open('runtime/benchmarks/baseline.json') as f:
    bm_raw = json.load(f)

PANDEMIC_START = pd.Timestamp('2020-01-31')
PANDEMIC_END   = pd.Timestamp('2021-01-31')

baseline_pq = pd.DataFrame(bm_raw['per_quarter'])
baseline_pq['date'] = pd.to_datetime(baseline_pq['date'])

oos_pq = pd.DataFrame(oos_bm['per_quarter'])
oos_pq['date'] = pd.to_datetime(oos_pq['date'])

print(f"OOS per_quarter rows: {len(oos_pq)}")
print(f"Baseline per_quarter rows: {len(baseline_pq)}")
print(f"OOS date range: {oos_pq['date'].min().date()} — {oos_pq['date'].max().date()}")
print(f"Baseline date range: {baseline_pq['date'].min().date()} — {baseline_pq['date'].max().date()}")

aligned = oos_pq.merge(baseline_pq[['date','ape_sna']], on='date', how='inner')
print(f"Matched (inner join): {len(aligned)}")

pandemic_mask = aligned['date'].between(PANDEMIC_START, PANDEMIC_END)
excl_df = aligned[~pandemic_mask]
print(f"Matched excl pandemic: {len(excl_df)}")

aligned_full_delta = aligned['ape_sna'].mean() - aligned['ape_m1'].mean()
aligned_excl_delta = excl_df['ape_sna'].mean() - excl_df['ape_m1'].mean()

print(f"SNA MAPE (matched, full):  {aligned['ape_sna'].mean()*100:.4f}%")
print(f"M1  MAPE (matched, full):  {aligned['ape_m1'].mean()*100:.4f}%")
print(f"Aligned delta (full-sample):    {aligned_full_delta*100:+.4f} pp")
print(f"Aligned delta (excl-pandemic):  {aligned_excl_delta*100:+.4f} pp")
print()
ci_full_lo = oos_bm['M1']['full_sample']['bootstrap_95ci_lo']
ci_full_hi = oos_bm['M1']['full_sample']['bootstrap_95ci_hi']
ci_excl_lo = oos_bm['M1']['pandemic_excluded']['bootstrap_95ci_lo']
ci_excl_hi = oos_bm['M1']['pandemic_excluded']['bootstrap_95ci_hi']
print(f"Bootstrap CIs from oos_errors.json:")
print(f"  Full   CI: [{ci_full_lo*100:+.2f}pp, {ci_full_hi*100:+.2f}pp]")
print(f"  Excl   CI: [{ci_excl_lo*100:+.2f}pp, {ci_excl_hi*100:+.2f}pp]")
print()
sna_full   = bm_raw['sna']['full_sample']['MAPE']
sna_excl   = bm_raw['sna']['pandemic_excluded']['MAPE']
m1_full    = oos_bm['M1']['full_sample']['MAPE']
m1_excl    = oos_bm['M1']['pandemic_excluded']['MAPE']
print(f"SNA MAPE (unmatched, n=49): {sna_full*100:.4f}%")
print(f"SNA MAPE (unmatched, n=44): {sna_excl*100:.4f}%")
print(f"M1  MAPE (unmatched, n=42): {m1_full*100:.4f}%")
print(f"M1  MAPE (unmatched, n=37): {m1_excl*100:.4f}%")
delta_unmatched_full = sna_full - m1_full
delta_unmatched_excl = sna_excl - m1_excl
print(f"Delta MAPE unmatched (full): {delta_unmatched_full*100:+.4f} pp  (SNA n=49 vs M1 n=42)")
print(f"Delta MAPE unmatched (excl): {delta_unmatched_excl*100:+.4f} pp  (SNA n=44 vs M1 n=37)")
print()
pandemic_oos = oos_pq[oos_pq['date'].between(PANDEMIC_START, PANDEMIC_END)]
print(f"Pandemic quarters in OOS per_quarter: {list(pandemic_oos['date'].dt.strftime('%Y-%m-%d'))}")
pandemic_base = baseline_pq[baseline_pq['date'].between(PANDEMIC_START, PANDEMIC_END)]
print(f"Pandemic quarters in baseline per_quarter: {list(pandemic_base['date'].dt.strftime('%Y-%m-%d'))}")
print()
# Verify the falsifiable claim numbers
print("=== Falsifiable claim check ===")
print(f"Claim says M1 MAPE = 2.57% — actual = {m1_full*100:.2f}%  MATCH={abs(m1_full*100-2.57)<0.01}")
print(f"Claim says SNA MAPE = 3.31% — actual = {sna_full*100:.2f}%  MATCH={abs(sna_full*100-3.31)<0.01}")
print(f"Claim says delta = 0.74pp — actual (unmatched) = {delta_unmatched_full*100:.2f}pp  MATCH={abs(delta_unmatched_full*100-0.74)<0.01}")
print(f"Claim says delta excl = 0.84pp — actual (unmatched) = {delta_unmatched_excl*100:.2f}pp  MATCH={abs(delta_unmatched_excl*100-0.84)<0.01}")
print(f"Claim CI full [+0.41, +1.65] — actual [{ci_full_lo*100:.2f}, {ci_full_hi*100:.2f}]")
print(f"Claim CI excl [+0.52, +1.74] — actual [{ci_excl_lo*100:.2f}, {ci_excl_hi*100:.2f}]")
