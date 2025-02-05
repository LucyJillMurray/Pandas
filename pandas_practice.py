import pandas as pd
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)       # Adjust width to avoid concatenation
pd.set_option('display.max_colwidth', None)  # Prevent truncation of long values



csv_file = "data.csv"
imported_df = pd.read_csv(csv_file)
print("\nImported DataFrame:")
print(imported_df)

# Step 3: Perform common Pandas operations

# Display basic statistics
print("\nBasic Statistics:")
print(imported_df.describe())

def drop(price):
    return price*97/100 #if price drops by 3%

imported_df['date'] = pd.to_datetime(imported_df['date'], format="%m/%d/%Y")
imported_df["next_day"] = imported_df.groupby("ticker")["date"].shift(-1)
imported_df["trade_drop"] = imported_df["close"].apply(drop)
imported_df["five_days"] = imported_df.groupby("ticker")["close"].shift(-5)
print(imported_df)
other = imported_df
inner_join = pd.merge(imported_df, other, left_on=["next_day","ticker"],right_on=["date","ticker" ], how="inner")
print("\nInner Join (Inner join on date with next day):")
print(inner_join)

inner_join = inner_join.drop(columns=["trade_drop_y"])
inner_join = inner_join.drop(columns=["next_day_y"])
inner_join = inner_join.drop(columns=["five_days_y"])
filtered_df = inner_join[inner_join["trade_drop_x"]> inner_join['close_y']]
print(filtered_df)
#filtered_df["five_days_x"] = pd.to_numeric(filtered_df["five_days_x"], errors="coerce")

#filtered_df["five_days_x"] = filtered_df["five_days_x"].replace("<ULL>", pd.NA)
#filtered_df = filtered_df.dropna()
#filtered_df = filtered_df.dropna(subset=["five_days_x"])

def safe_sum(filtered_df):
    try:
        return float(filtered_df["five_days_x"]) - float(filtered_df["close_y"])
    except (ValueError, TypeError):
        return np.nan
    
filtered_df["profit"] = filtered_df.apply(safe_sum, axis=1)

#imported_df["profit"] =filtered_df["close_y"]-["five_days_x"]
print(filtered_df)
filtered_df1 = filtered_df[filtered_df["ticker"] == "sol-za"]
print(filtered_df1)
total = filtered_df1["profit"].sum()
print(total)

summary = filtered_df.groupby("ticker")["profit"].agg(
    max_profit="max", 
    min_profit="min", 
    avg_profit="mean"
)
print(summary)



