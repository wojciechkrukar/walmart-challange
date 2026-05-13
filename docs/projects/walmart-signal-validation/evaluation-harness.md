# Evaluation Harness — walmart-signal-validation

## Strict forward-rolling time-series CV specification

This is the single source of truth for how the OOS metrics in `runtime/benchmarks/baseline.json` are computed. Any deviation requires a Class D PR (per `docs/team/review_policy.md`).

### Algorithm

```
Inputs:
  df: DataFrame indexed by fiscal-quarter end date,
      columns = [walmart_revenue, fred_yoy_lag1, walmart_yoy_lag1, ...]
  min_train: int   = 16   (≥ 4 years of data so the model sees ≥ 1 full business cycle)
  step:      int   = 1    (advance one quarter per fold)

Procedure:
  predictions = []
  FOR i IN range(min_train, len(df)):
      train = df.iloc[:i]                     # quarters 0 .. i-1
      test  = df.iloc[i : i+1]                # single OOS quarter

      # Critical: every quantity used to build `test` features MUST already exist in `train`.
      # The lag-1 construction in `architecture.md` enforces this at feature-build time.

      # Baseline: Q(t) = Q(t-4) * (1 + mean YoY computed on train only)
      mu_train       = train['walmart_yoy'].mean()
      baseline_pred  = train['walmart_revenue'].iloc[i-4] * (1 + mu_train)

      # Signal model: OLS on train, predict on test
      model          = sm.OLS(train.walmart_revenue, sm.add_constant(train[features])).fit()
      signal_pred    = model.predict(sm.add_constant(test[features])).iloc[0]

      predictions.append({
          'date':       test.index[0],
          'actual':     test['walmart_revenue'].iloc[0],
          'baseline':   baseline_pred,
          'signal':     signal_pred,
      })

Outputs:
  cv_df = DataFrame(predictions)
  Compute MAPE / RMSE on cv_df for each window:
    - Full
    - Pre-COVID    (date < '2020-01-01')
    - COVID        ('2020-01-01' ≤ date ≤ '2021-04-01')
    - Post-COVID   (date > '2021-04-01')
    - Ex-COVID     (Pre-COVID ∪ Post-COVID)
```

### Forbidden constructs

- `from sklearn.model_selection import KFold` — REJECT
- `from sklearn.model_selection import ShuffleSplit` — REJECT
- `train_test_split(..., shuffle=True)` — REJECT
- `train_test_split(...)` without `shuffle=False` — REJECT (the default is `True`)
- Any positional `iloc` shift that could wrap negative indices into the tail of the DataFrame — REJECT

### Required assertions

The notebook MUST contain explicit assertions immediately after the CV loop:

```python
assert cv_df['date'].is_monotonic_increasing, "Folds must be forward-rolling"
assert (cv_df['date'].diff().dropna() > pd.Timedelta(0)).all(), "No reverse steps"
assert mu_train_history is monotonic-by-construction (one mean per training window)
```

### Baseline regression gate

`runtime/benchmarks/baseline.json` is the frozen reference. A future PR that changes any of these numbers by more than ±0.05 percentage points (MAPE) is a Class D PR.

### Reproducibility

The harness is fully deterministic:
- No `random_state` is set because no randomness is used.
- pandas / numpy / statsmodels versions are pinned in `requirements.txt`.
- Re-running `jupyter nbconvert --execute --inplace analysis.ipynb` MUST produce byte-identical metrics in the verdict cells.
