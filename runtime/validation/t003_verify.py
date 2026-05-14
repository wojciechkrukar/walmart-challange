"""T003 audit verification script — runs § 3 logic and prints spot-check table."""
import pandas as pd
from pandas.tseries.offsets import MonthEnd

# Load raw data (same paths as notebook)
fred_raw = pd.read_csv("data/retail_sales_fred.csv", parse_dates=["date"])
wmt_raw  = pd.read_csv("data/walmart_revenue.csv",   parse_dates=["date"])

# ---------- fiscal quarter assignment (copied from notebook) ----------
def assign_fiscal_quarter(dt):
    m = dt.month
    y = dt.year
    if m == 1:
        return (y - 1, 4)
    elif m in (2, 3, 4):
        return (y, 1)
    elif m in (5, 6, 7):
        return (y, 2)
    elif m in (8, 9, 10):
        return (y, 3)
    else:   # 11, 12
        return (y, 4)

print("=== 1. assign_fiscal_quarter spot-checks ===")
for mo, label in [(1,"Jan"), (2,"Feb"), (11,"Nov"), (12,"Dec"), (4,"Apr")]:
    dt  = pd.Timestamp(2011, mo, 1)
    got = assign_fiscal_quarter(dt)
    print(f"  2011-{label} → {got}")

# ---------- aggregate to fiscal quarters ----------
fred_monthly = fred_raw[["date","value"]].copy().sort_values("date").reset_index(drop=True)
fred_monthly.rename(columns={"value":"rsxfs_monthly"}, inplace=True)
fred_monthly["fy"], fred_monthly["fq"] = zip(*fred_monthly["date"].map(assign_fiscal_quarter))

def fiscal_quarter_end(fy, fq):
    if fq == 1:   return pd.Timestamp(fy, 4, 30)
    elif fq == 2: return pd.Timestamp(fy, 7, 31)
    elif fq == 3: return pd.Timestamp(fy, 10, 31)
    else:         return pd.Timestamp(fy + 1, 1, 31)

fred_quarterly = (
    fred_monthly
    .groupby(["fy","fq"])
    .agg(
        rsxfs_fq_sum=("rsxfs_monthly","sum"),
        months_present=("rsxfs_monthly","count"),
        last_month_in_quarter=("date","max"),
    )
    .reset_index()
)
fred_quarterly["fq_end"] = fred_quarterly.apply(
    lambda r: fiscal_quarter_end(r["fy"], r["fq"]), axis=1
)
fred_quarterly = fred_quarterly[fred_quarterly["months_present"] == 3].copy()
fred_quarterly = fred_quarterly.sort_values("fq_end").reset_index(drop=True)

# YoY computed BEFORE merge
fred_quarterly["rsxfs_yoy"] = fred_quarterly["rsxfs_fq_sum"] / fred_quarterly["rsxfs_fq_sum"].shift(4) - 1

# feature_release_date = last_month_end + 45 days
fred_quarterly["last_month_end"] = fred_quarterly["last_month_in_quarter"] + MonthEnd(0)
fred_quarterly["feature_release_date"] = fred_quarterly["last_month_end"] + pd.Timedelta(days=45)

print("\n=== 2. FRED quarterly frame (first 8 rows) ===")
print(fred_quarterly[["fy","fq","fq_end","last_month_in_quarter","last_month_end","feature_release_date","rsxfs_yoy"]].head(8).to_string(index=False))

# ---------- Walmart quarterly + decision dates ----------
wmt_q = wmt_raw[["date","value"]].copy().sort_values("date").reset_index(drop=True)
wmt_q.rename(columns={"value":"revenue"}, inplace=True)

def fiscal_quarter_start(fq_end_date):
    m = fq_end_date.month
    y = fq_end_date.year
    if m == 4:    return pd.Timestamp(y, 2, 1)
    elif m == 7:  return pd.Timestamp(y, 5, 1)
    elif m == 10: return pd.Timestamp(y, 8, 1)
    elif m == 1:  return pd.Timestamp(y - 1, 11, 1)
    else:         raise ValueError(f"Bad month {m}")

wmt_merged = wmt_q.copy().sort_values("date").reset_index(drop=True)
wmt_merged["fq_start"]     = wmt_merged["date"].map(fiscal_quarter_start)
wmt_merged["decision_date"] = wmt_merged["fq_start"] - pd.Timedelta(days=1)

# ---------- merge_asof ----------
fred_for_merge = fred_quarterly[["fq_end","feature_release_date","rsxfs_fq_sum","rsxfs_yoy"]].copy()
fred_for_merge = fred_for_merge.sort_values("feature_release_date").reset_index(drop=True)
wmt_for_merge  = wmt_merged.sort_values("decision_date").reset_index(drop=True)

merged = pd.merge_asof(
    wmt_for_merge,
    fred_for_merge,
    left_on="decision_date",
    right_on="feature_release_date",
    direction="backward",
    suffixes=("", "_fred"),
)

# Assertion
bad_rows = merged[merged["feature_release_date"] > merged["decision_date"]]
assert len(bad_rows) == 0, f"LOOK-AHEAD VIOLATION: {len(bad_rows)} rows"
print(f"\n=== 3. Anti-look-ahead assertion PASSED: {len(merged)} rows ===")

# revenue YoY
merged["revenue_yoy"] = merged["revenue"] / merged["revenue"].shift(4) - 1

# ---------- Spot-check: the three rows from the Review Request ----------
display_cols = ["date","decision_date","feature_release_date","fq_end","rsxfs_yoy","revenue_yoy"]
analysis_df = merged[merged["revenue_yoy"].notna() & merged["rsxfs_yoy"].notna()].copy()
analysis_df = analysis_df.sort_values("date").reset_index(drop=True)

print("\n=== 4. Full spot-check table (first 5 rows with both YoY available) ===")
print(analysis_df[display_cols].head(5).to_string(index=False, float_format="{:.6f}".format))

# Specifically print the three target rows for the Review Request
print("\n=== 5. Three spot-check rows from Review Request ===")
target_dates = [pd.Timestamp("2011-10-31"), pd.Timestamp("2012-01-31"), pd.Timestamp("2012-04-30")]
for td in target_dates:
    row = analysis_df[analysis_df["date"] == td]
    if len(row) == 0:
        # Maybe date shows as end of month – check nearby
        row = merged[merged["date"] == td]
    if len(row) == 0:
        print(f"  {td.date()} NOT FOUND in merged frame")
    else:
        r = row.iloc[0]
        print(f"\n  Walmart Q ending {r['date'].date()}")
        print(f"    decision_date       = {r['decision_date'].date()}")
        print(f"    feature_release_date= {r['feature_release_date'].date() if pd.notna(r['feature_release_date']) else 'NaT'}")
        print(f"    fq_end (FRED used)  = {r['fq_end'].date() if pd.notna(r['fq_end']) else 'NaT'}")
        print(f"    rsxfs_yoy           = {r['rsxfs_yoy']:.6f}" if pd.notna(r['rsxfs_yoy']) else "    rsxfs_yoy           = NaN")
        print(f"    revenue_yoy         = {r['revenue_yoy']:.6f}" if pd.notna(r['revenue_yoy']) else "    revenue_yoy         = NaN")
        ok = r['feature_release_date'] <= r['decision_date'] if pd.notna(r['feature_release_date']) else False
        print(f"    lag OK (frd <= dec) = {ok}")

# ---------- Revenue look-ahead check ----------
print("\n=== 6. Revenue look-ahead check ===")
print("Columns in merged frame:", list(merged.columns))
# Check: revenue_yoy is computed after the merge; it's the TARGET column
# Confirm it is not used as a predictor (no revenue value from Q or future in fred_for_merge)
print("Columns in fred_for_merge:", list(fred_for_merge.columns))
# revenue should appear only once in merged (the target)
rev_cols = [c for c in merged.columns if 'revenue' in c.lower()]
print("Revenue-related columns in merged:", rev_cols)

print("\n=== 7. last_month_end vs fq_end check ===")
# Confirm feature_release_date is from last_month_end not fq_end
sample = fred_quarterly[["fy","fq","fq_end","last_month_end","feature_release_date"]].head(8)
for _, r in sample.iterrows():
    from_last = r['last_month_end'] + pd.Timedelta(days=45)
    from_fqend = r['fq_end'] + pd.Timedelta(days=45)
    match_last  = r['feature_release_date'] == from_last
    match_fqend = r['feature_release_date'] == from_fqend
    note = "from last_month_end" if match_last else ("from fq_end" if match_fqend else "UNKNOWN")
    print(f"  FY{r['fy']} fQ{r['fq']}: frd={r['feature_release_date'].date()}, from_last={from_last.date()}, from_fqend={from_fqend.date()} → {note}")
