# DV_Project# Italy Export Diversification & Concentration (HS6) — Selected European Partners (2013–2024)

This project analyzes Italy’s export structure across 10 key European partner countries using HS6-level trade data (2013–2024).  
The core objective is to quantify **export concentration vs. diversification** and evaluate **stability over time**, then summarize results through a regime-based classification.

## Selected Partners
Czech Republic, Romania, Austria, Netherlands, Germany, France, Spain, Switzerland, Poland, Belgium.

## Research Questions
1. How diversified are Italy’s exports across the selected partner markets (HS6 level)?
2. Which partners show structurally concentrated export patterns (high dependency on few products)?
3. Are concentration/diversification patterns stable over time, or shock-sensitive?
4. Which partner relationships appear most resilient vs. most vulnerable based on a joint structure–stability view?

## Data
**Source:** TradeMap bilateral export tables at HS6 product level.  
**HS6 explanation:** HS6 is the Harmonized System 6-digit product classification. Each 6-digit code represents a specific product category.  
Using HS6 enables a detailed view of export composition across thousands of product categories.

## Methodology (High-level)
- Compute product-level export shares per partner-year.
- Build concentration/diversification indicators:
  - HHI (Herfindahl–Hirschman Index)
  - CR3/CR5/CR10 (top product concentration ratios)
  - Normalized entropy (diversification measure)
- Apply a 2-step regime framework:
  - Step 2: Diversification regime (diversified / transitional / structurally concentrated)
  - Step 3: Stability regime (stable / moderately stable / shock-sensitive)
- Produce final partner classification and summary table for the latest year.

## Project Structure
- `data/raw/` : Raw TradeMap export tables (xls/htm)
- `data/processed/` : Cleaned datasets and computed metrics (csv)
- `src/` : Python scripts for the pipeline
- `figures/` : Exported charts (png)
- `report/` : Final PDF and presentation outputs`
- `author/`: Maryamsadat Parpenchi

## How to Run
### 1) Install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
