import os
import pandas as pd

DATA_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "italy")

latest = pd.read_csv(os.path.join(DATA_DIR, "selected10_regimes_latest_year.csv"))
stab   = pd.read_csv(os.path.join(DATA_DIR, "selected10_regimes_stability.csv"))

# اگر stability_step3 از قبل هست، دوباره مرج نکن
if "stability_step3" in latest.columns:
    final = latest.merge(
        stab[["partner","hhi_std","cr10_cv","entropy_std"]],
        on="partner",
        how="left"
    )
else:
    final = latest.merge(
        stab[["partner","stability_step3","hhi_std","cr10_cv","entropy_std"]],
        on="partner",
        how="left"
    )

def regime_step2_abs(r):
    if (r["hhi_hs6"] <= 0.01) and (r["cr10"] <= 0.22) and (r["entropy_norm"] >= 0.74) and (r["active_hs6"] >= 3500):
        return "Real diversification"
    if (r["hhi_hs6"] >= 0.02) and (r["cr10"] >= 0.30) and (r["entropy_norm"] <= 0.70):
        return "Structural concentration"
    return "Transition / mixed"

final["regime_step2_abs"] = final.apply(regime_step2_abs, axis=1)

def interpret(r):
    st = r.get("stability_step3", "Unknown")
    rg = r.get("regime_step2_abs", "Transition / mixed")

    if rg == "Real diversification" and st == "Stable":
        return "Diversified & resilient export structure."
    if rg == "Real diversification" and "Moderately" in st:
        return "Diversified with moderate volatility."
    if rg == "Real diversification" and "Cyclical" in st:
        return "Diversified but shock-sensitive."

    if rg == "Structural concentration" and "Cyclical" in st:
        return "Highly concentrated & volatile."
    if rg == "Structural concentration":
        return "Concentrated export structure."

    if "Cyclical" in st:
        return "Mixed basket, shock-sensitive."
    if "Moderately" in st:
        return "Mixed basket, moderately stable."
    if st == "Stable":
        return "Mixed basket, stable."
    return "Mixed basket."

final["interpretation"] = final.apply(interpret, axis=1)

cols = [
    "partner","year",
    "regime_step2","regime_step2_abs",
    "stability_step3","interpretation",
    "active_hs6","hhi_hs6","cr10","entropy_norm",
    "hhi_std","cr10_cv","entropy_std"
]
cols = [c for c in cols if c in final.columns]
final = final[cols].sort_values(["regime_step2_abs","partner"])

out = os.path.join(DATA_DIR, "step23_final_summary_table.csv")
final.to_csv(out, index=False)

print("Saved:", out)
print(final.to_string(index=False))
