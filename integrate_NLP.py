import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

# Download once
nltk.download("stopwords")
nltk.download("wordnet")

# Load data
df = pd.read_csv("data.csv")

# -----------------------------
# TEXT CLEANING FUNCTION
# -----------------------------
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return " ".join(words)

df["clean_text"] = df["text"].apply(clean_text)


# -----------------------------
# NLP FEATURE CREATION
# -----------------------------
tfidf = TfidfVectorizer(max_features=500)

X_text = tfidf.fit_transform(df["clean_text"])


# -----------------------------
# NUMERIC FEATURES (FROM BEFORE)
# -----------------------------
df["total_spend"] = df["price"] * df["quantity"]

df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month
df["dayofweek"] = df["date"].dt.dayofweek


# -----------------------------
# SPLIT DATA (AVOID LEAKAGE)
# -----------------------------
target = "target"

X_num = df[["total_spend", "month", "dayofweek"]]
y = df[target]

X_train_num, X_test_num, X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_num, X_text, y, test_size=0.2, random_state=42
)


# -----------------------------
# SCALE NUMERIC FEATURES
# -----------------------------
scaler = StandardScaler()
X_train_num = scaler.fit_transform(X_train_num)
X_test_num = scaler.transform(X_test_num)


# -----------------------------
# COMBINE TEXT + NUMERIC
# -----------------------------
from scipy.sparse import hstack

X_train_final = hstack([X_train_text, X_train_num])
X_test_final = hstack([X_test_text, X_test_num])


print("Final feature shape:", X_train_final.shape)
