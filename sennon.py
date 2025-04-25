# %%
import pandas as pd
import sys

# %%
# %% Expected columns
expected_columns = [
    'timestamp', 'serial', 'grid_purchase', 'grid_feedin', 'direct_consumption', 'date'
]

# %% Load the data
try:
    sonnen = pd.read_csv("measurements_coding_challenge.csv", sep=';')
except Exception as e:
    print(f"❌ Error reading CSV file: {e}")
    sys.exit(1)

# %% Convert columns to lowercase immediately
sonnen.columns = sonnen.columns.str.strip().str.lower()

# %%
# %% Validate columns
actual_columns = sonnen.columns.tolist()
expected_columns_lower = [col.lower() for col in expected_columns]

missing_cols = set(expected_columns_lower) - set(actual_columns)

if missing_cols:
    print(f"❌ Missing columns in the data: {missing_cols}")
    sys.exit(1)
else:
    print(f"✅ All expected columns found.")

# %%
error_rows = pd.DataFrame(columns=sonnen.columns)

# %%
# List of datetime columns
datetime_cols = ['timestamp', 'date']

# Now apply similar logic for datetime conversion
for col in datetime_cols:
    while True:
        try:
            sonnen[col] = pd.to_datetime(sonnen[col])
            print(f"✅ Successfully converted {col} to datetime")
            break
        except Exception as e:
            # Same catching logic as numeric
            row = int(str(e).split()[-1])
            error_rows = pd.concat([error_rows, sonnen.iloc[[row]]], axis=0)
            sonnen.drop(row, inplace=True)
            sonnen.reset_index(drop=True, inplace=True)

# %%
sonnen.replace(["NaN", "None", ""], None, inplace=True)

# %%
sonnen.drop_duplicates(inplace=True)

# %%
numeric_cols = ['serial', 'grid_purchase', 'grid_feedin', 'direct_consumption']
dd = list()
for col in numeric_cols:
    while True:
        try:
            sonnen[col] = pd.to_numeric(sonnen[col])
            print(f"✅ Successfully converted {col} to numeric")
            break
        except ValueError as e:
            row = int(str(e).split()[-1])
            dd.append(row)
            error_rows = pd.concat([error_rows , sonnen.iloc[[row]]], axis=0)
            sonnen.drop(row, inplace=True)
            sonnen.reset_index(inplace=True, drop=True)

# %%
sonnen['hour'] = sonnen['timestamp'].dt.hour

# %%
sonnen_grouped = sonnen.groupby(sonnen['hour'])[['grid_purchase', 'grid_feedin']].sum().reset_index()

# %%
sonnen_grouped['max_hour'] = sonnen_grouped['grid_feedin'] == sonnen_grouped['grid_feedin'].max()

# %%
# %% Save output
sonnen_grouped.to_csv("cleaned_transformed_data.csv", index=False)
error_rows.to_csv("error_rows.csv", index=False)

print("✅ Transformation complete. Outputs saved.")


