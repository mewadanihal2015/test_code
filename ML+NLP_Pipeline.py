import pandas as pd
import numpy as np
import random
import string

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# -----------------------------
# 1. GENERATE RANDOM DATASET
# -----------------------------
def random_text():
    words = ["great", "bad", "average", "excellent", "poor", "fast", "slow"]
    return " ".join(random.choices(words, k=random.randint(5, 15)))

np.random.seed(42)

df = pd.DataFrame({
    "price": np.random.randint(5, 100, 200),
    "quantity": np.random.randint(1, 10, 200),
    "review": [random_text() for _ in range(200)],
    "date": pd.date_range(start="2023-01-01", periods=200, freq="D")
})

# Binary target
df["target"] = (df["price"] * df["quantity"] > 300).astype(int)


# -----------------------------
# 2. FEATURE ENGINEERING
# -----------------------------
# Interaction feature
df["total_spend"] = df["price"] * df["quantity"]

# Time features
df["month"] = df["date"].dt.month
df["dayofweek"] = df["date"].dt.dayofweek

# Simple NLP feature
vectorizer = TfidfVectorizer(max_features=50)
X_text = vectorizer.fit_transform(df["review"])


# -----------------------------
# 3. PREPARE DATA
# -----------------------------
X_num = df[["total_spend", "month", "dayofweek"]]
y = df["target"]

X_train_num, X_test_num, X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_num, X_text, y, test_size=0.2, random_state=42
)

# Scale numeric features
scaler = StandardScaler()
X_train_num = scaler.fit_transform(X_train_num)
X_test_num = scaler.transform(X_test_num)

# Combine features
from scipy.sparse import hstack
X_train = hstack([X_train_text, X_train_num])
X_test = hstack([X_test_text, X_test_num])


# -----------------------------
# 4. TRAIN MODEL
# -----------------------------
model = LogisticRegression()
model.fit(X_train, y_train)

# -----------------------------
# 5. EVALUATE
# -----------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)
