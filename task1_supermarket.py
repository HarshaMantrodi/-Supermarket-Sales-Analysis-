import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# 1. SETUP PATHS
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'supermarket_sales.csv')

# 2. LOAD DATA
try:
    df = pd.read_csv(file_path)
    print("Supermarket Data Loaded Successfully!")
    
    # CLEAN COLUMN NAMES
    df.columns = df.columns.str.strip()
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    sys.exit()

# 3. MAPPING YOUR SPECIFIC COLUMNS
# Based on your terminal output: 'Sales' is your revenue column
rename_map = {
    'Sales': 'total_revenue',
    'gross income': 'profit',
    'Product line': 'category',
    'Date': 'date'
}
df.rename(columns=rename_map, inplace=True)

# 4. DATA PROCESSING
df['date'] = pd.to_datetime(df['date'])

# 5. BUSINESS ANALYSIS (KPIs)
# Revenue and Profit by Branch
branch_perf = df.groupby('Branch')[['total_revenue', 'profit']].sum().sort_values(by='total_revenue', ascending=False)
print("\n--- Branch Performance ---")
print(branch_perf)

# Best-selling Product Categories
category_perf = df.groupby('category')['total_revenue'].sum().sort_values(ascending=False)

# 6. VISUALIZATION
plt.figure(figsize=(14, 6))

# Subplot 1: Sales by Category
plt.subplot(1, 2, 1)
sns.barplot(x=category_perf.values, y=category_perf.index, palette='viridis')
plt.title('Total Sales by Product Category')
plt.xlabel('Revenue ($)')

# Subplot 2: Sales Trend (Daily)
plt.subplot(1, 2, 2)
daily_sales = df.groupby('date')['total_revenue'].sum()
plt.plot(daily_sales.index, daily_sales.values, color='tab:red', marker='o', markersize=4)
plt.title('Daily Sales Performance Trend')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()