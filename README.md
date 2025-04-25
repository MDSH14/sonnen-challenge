# Sonnen Data Engineering Challenge

This project processes and cleans a time series dataset of battery measurements using Python and Docker.

---

## 🧠 What It Does

- Loads a raw CSV file with battery data.
- Cleans the data:
  - Removes duplicates
  - Converts numeric and datetime fields safely
  - Drops corrupted rows
- Aggregates:
  - Calculates total `grid_purchase` and `grid_feedin` per hour
  - Flags the hour with the highest `grid_feedin`
- Outputs two files:
  - `cleaned_transformed_data.csv`
  - `error_rows.csv`

---

## 🚀 How to Run Using Docker

### 1. Clone this repository and open the folder:

```bash
git clone https://github.com/MDSH14/sonnen-challenge.git
cd sonnen-challenge
