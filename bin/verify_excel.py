"""Verify Excel output"""
import pandas as pd
import glob

files = glob.glob('outputs/*.xlsx')
if files:
    latest_file = max(files, key=lambda x: x)
    print(f"Reading: {latest_file}\n")
    df = pd.read_excel(latest_file)
    print(df.to_string())
    print(f"\nColumns: {list(df.columns)}")
    print(f"Rows: {len(df)}")
