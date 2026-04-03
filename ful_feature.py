import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load data
df = pd.read_csv("data.csv")

# -----------------------------
# 1. CREATE INTERACTION FEATURES
# -----------------------------
# Example: price × quantity
df["total_spend"] = df["price"] * df["quantity"]

# Example: ratio feature
df["price_per_unit"] = df["price"] / (df["quantity"] + 1)  # avoid division by zero


# -----------------------------
# 2. EXTRACT TIME-BASED FEATURES
# -----------------------------
df["date"] = pd.to_datetime(df["date"])

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["dayofweek"] = df["date"].dt.dayofweek
df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)


# -----------------------------
# 3. DOMAIN KNOWLEDGE FEATURES
# -----------------------------
# Example (e-commerce):
df["high_value_customer"] = (df["total_spend"] > 1000).astype(int)

# Example (finance):
# df["debt_to_income"] = df["debt"] / (df["income"] + 1)

# Example (health):
# df["bmi"] = df["weight"] / (df["height"] ** 2)


# -----------------------------
# 4. AVOID DATA LEAKAGE
# -----------------------------
# Split BEFORE scaling/encoding
target = "target"
X = df.drop(columns=[target])
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# IMPORTANT:
# Never compute statistics (mean, etc.) on full dataset!


# -----------------------------
# 5. SCALE FEATURES
# -----------------------------
numeric_cols = X_train.select_dtypes(include=["int64", "float64"]).columns

scaler = StandardScaler()

# Fit ONLY on training data
X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])

# Apply same transformation to test
X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])


# -----------------------------
# DONE
# -----------------------------
print("Feature engineering complete!")
print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)
