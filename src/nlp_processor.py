import pandas as pd
import re
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

file = pd.read_csv("data/raw_reviews.csv")

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"\@\w+|\#", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

file["Cleaned_Review"] = file["Review"].apply(clean_text)

def rating_to_label(rating):
    if rating >= 4:
        return "Positive"
    elif rating == 3:
        return "Neutral"
    else:
        return "Negative"

file["True_Label"] = file["Rating"].apply(rating_to_label)

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(file["Cleaned_Review"])

model = LogisticRegression(class_weight="balanced")
model.fit(X, file["True_Label"])    

file["ML_Predicted_Label"] = model.predict(X)

print(classification_report(file["True_Label"], file["ML_Predicted_Label"], zero_division=0))

file.to_csv("data/processed_reviews.csv", index=False)

print(file)
print("Data saved to data/processed_reviews.csv!")