import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HOME = os.path.expanduser("~")
DATA_DIR = os.path.join(HOME, "Downloads", "italy")

FINAL_TABLE = os.path.join(DATA_DIR, "step23_final_summary_table.csv")
TS_FILE     = os.path.join(DATA_DIR, "italy_selected10_product_concentration.csv")  # optional

OUT_DIR = os.path.join(DATA_DIR, "figures_export")
os.makedirs(OUT_DIR, exist_ok=True)

if not os.path.exists(FINAL_TABLE):
    raise FileNotFoundError(f"Missing: {FINAL_TABLE} (Run final_analysis.py first)")

df = pd.read_csv(FINAL_TABLE)
latest_year = int(df["year"].max())

# numeric
for c in ["active_hs6","hhi_hs6","cr10","entropy_norm"]:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

df_ts = None
if os.path.exists(TS_FILE):
    df_ts = pd.read_csv(TS_FILE)
    df_ts["year"] = pd.to_numeric(df_ts["year"], errors="coerce")

plt.rcParams.update({
    "figure.dpi": 150,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

def save(path):
    plt.tight_layout()
    plt.savefig(path, dpi=260, bbox_inches="tight")
    plt.close()

# -----------------------
# 1) Scatter: Entropy vs HHI
# -----------------------
p1 = os.path.join(OUT_DIR, "01_scatter_entropy_vs_hhi.png")
plt.figure(figsize=(8, 5))
plt.scatter(df["entropy_norm"], df["hhi_hs6"])
for _, r in df.iterrows():
    plt.text(r["entropy_norm"], r["hhi_hs6"], r["partner"], fontsize=9)
plt.xlabel("Entropy (normalized) — higher means more diversified")
plt.ylabel("HHI (HS6) — higher means more concentrated")
plt.title(f"Diversification vs Concentration (Italy exports, {latest_year})")
save(p1)

# -----------------------
# 2) Bar: CR10 latest year
# -----------------------
p2 = os.path.join(OUT_DIR, "02_bar_cr10_latest_year.png")
tmp = df.sort_values("cr10", ascending=False)
plt.figure(figsize=(8, 5))
plt.bar(tmp["partner"], tmp["cr10"])
plt.xticks(rotation=35, ha="right")
plt.ylabel("CR10 (share of top-10 HS6 products)")
plt.title(f"Top-10 Product Concentration by Partner (CR10, {latest_year})")
save(p2)

# -----------------------
# 3) Bar: HHI latest year
# -----------------------
p3 = os.path.join(OUT_DIR, "03_bar_hhi_latest_year.png")
tmp = df.sort_values("hhi_hs6", ascending=False)
plt.figure(figsize=(8, 5))
plt.bar(tmp["partner"], tmp["hhi_hs6"])
plt.xticks(rotation=35, ha="right")
plt.ylabel("HHI (HS6)")
plt.title(f"Product Concentration by Partner (HHI, {latest_year})")
save(p3)

# -----------------------
# 4) Time series: Entropy over time (optional)
# -----------------------
if df_ts is not None and "entropy_norm" in df_ts.columns:
    p4 = os.path.join(OUT_DIR, "04_timeseries_entropy.png")
    plt.figure(figsize=(8, 5))
    for p in sorted(df_ts["partner"].dropna().unique()):
        g = df_ts[df_ts["partner"] == p].sort_values("year")
        if len(g) > 0:
            plt.plot(g["year"], g["entropy_norm"], label=p)
    plt.xlabel("Year")
    plt.ylabel("Entropy (normalized)")
    plt.title("Diversification Over Time (Entropy)")
    plt.legend(fontsize=7, ncols=2, frameon=False)
    save(p4)
else:
    print("[INFO] Time-series file not found (or entropy_norm missing) -> skipping 04_timeseries_entropy.png")

# -----------------------
# 5) Regime matrix (heatmap-like)
# -----------------------
p5 = os.path.join(OUT_DIR, "05_regime_matrix.png")
order = df.sort_values(["regime_step2_abs","stability_step3","partner"]).reset_index(drop=True)

reg_levels = list(order["regime_step2_abs"].dropna().unique())
stab_levels = list(order["stability_step3"].dropna().unique())
reg_map = {k:i for i,k in enumerate(reg_levels)}
stab_map = {k:i for i,k in enumerate(stab_levels)}

mat = np.zeros((len(order), 2))
mat[:, 0] = [reg_map[x] for x in order["regime_step2_abs"]]
mat[:, 1] = [stab_map[x] for x in order["stability_step3"]]

plt.figure(figsize=(8, 5))
plt.imshow(mat, aspect="auto")
plt.yticks(range(len(order)), order["partner"], fontsize=9)
plt.xticks([0, 1], ["Diversification Regime", "Stability Regime"], fontsize=10)
plt.title("Partner Classification Matrix (Regime + Stability)")
save(p5)

# -----------------------
# 6) Table as image (PNG)
# -----------------------
p6 = os.path.join(OUT_DIR, "06_summary_table.png")
cols = ["partner","regime_step2_abs","stability_step3","hhi_hs6","cr10","entropy_norm","interpretation"]
tbl = df[cols].copy()

# format
tbl["hhi_hs6"] = tbl["hhi_hs6"].map(lambda x: f"{x:.4f}")
tbl["cr10"] = tbl["cr10"].map(lambda x: f"{x:.3f}")
tbl["entropy_norm"] = tbl["entropy_norm"].map(lambda x: f"{x:.3f}")

fig, ax = plt.subplots(figsize=(11, 4.8))
ax.axis("off")

table = ax.table(
    cellText=tbl.values,
    colLabels=tbl.columns,
    cellLoc="left",
    colLoc="left",
    loc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 1.35)

plt.title(f"Partner Summary Table (Latest year = {latest_year})", pad=12)
plt.tight_layout()
plt.savefig(p6, dpi=260, bbox_inches="tight")
plt.close()

print("\n✅ Saved figures to:", OUT_DIR)
for f in sorted(os.listdir(OUT_DIR)):
    if f.lower().endswith(".png"):
        print("-", f)
