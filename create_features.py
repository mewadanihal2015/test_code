# Example feature engineering
df["total_spend"] = df["price"] * df["quantity"]

# Date feature extraction
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["dayofweek"] = df["date"].dt.dayofweek

# Binning
df["age_group"] = pd.cut(df["age"], bins=[0, 18, 35, 60, 100],
                         labels=["child", "young", "adult", "senior"])
