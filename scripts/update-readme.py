import pandas as pd
import os

# Path to the CSV file
csv_file = "tips.csv"
readme_file = "README.md"

# Read the CSV file
try:
    df = pd.read_csv(csv_file, header=0)
except FileNotFoundError:
    raise FileNotFoundError(f"{csv_file} not found")
except pd.errors.EmptyDataError:
    raise ValueError(f"{csv_file} is empty or invalid")

required_columns = ["Date", "Tips"]
if not all(col in df.columns for col in required_columns):
    missing_cols = [col for col in required_columns if col not in df.columns]
    raise ValueError(f"Missing columns: {', '.join(missing_cols)}")


# Convert date column to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)

# Check for invalid dates
if df["Date"].isna().any():
    raise ValueError("Some dates in 'date' column are invalid")







display_columns = ["Date", "Time-Worked", "Tips"]
df["Date_display"] = df["Date"].dt.strftime("%d.%m.%Y")
sample_data = df[["Date_display", "Time-Worked", "Tips"]].head(5).rename(columns={"Date_display": "Date"}).to_markdown(index=False)

# Calculate sum of tips per month
df["year_month"] = df["Date"].dt.strftime("%Y-%m")  # Format as YYYY-MM
monthly_tips = df.groupby("year_month")[["Tips", "Time-Worked"]].sum().round(2)

# Format monthly tips as a Markdown list
monthly_tips_list = "\n".join(
    [f"- {month} - ({totals['Time-Worked']}h): ${totals['Tips']:.2f}" for month, totals in monthly_tips.iterrows()]
)

# Get last updated date
last_updated = df["Date"].max().strftime("%Y-%m-%d")

total_tips = df['Tips'].sum()

# Content to add to README
new_content = f"""# My Project

## Tips Data Overview
Last updated: {last_updated}

### Sample Data
{sample_data}

### Monthly Tips Summary
{monthly_tips_list}

*This section is automatically updated when `tips.csv` changes.*
"""

# Write to README.md
with open(readme_file, "w") as f:
    f.write(new_content)

print("README.md updated successfully!")