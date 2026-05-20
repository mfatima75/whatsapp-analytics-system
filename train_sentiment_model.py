import pandas as pd
import joblib
import json
from sklearn.metrics import precision_score, recall_score, f1_score

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from utils.nlp_preprocessing import clean_text


# Load dataset
columns = ['target', 'id', 'date', 'flag', 'user', 'text']

df = pd.read_csv(
    'datasets/training.1600000.processed.noemoticon.csv',
    encoding='latin-1',
    names=columns
)

# Keep required columns only
df = df[['target', 'text']]

# Convert target labels
df['target'] = df['target'].replace(4, 1)

# Reduce dataset size for faster training
df = df.sample(50000, random_state=42)

print("Dataset Loaded Successfully")
print(df.head())


# NLP Cleaning
df['cleaned_text'] = df['text'].apply(clean_text)

print("\nText Cleaning Completed")


# Features and Labels
X = df['cleaned_text']
y = df['target']


# TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=5000)

X_vectorized = vectorizer.fit_transform(X)

print("\nTF-IDF Vectorization Completed")


# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTrain-Test Split Completed")


# Logistic Regression Model
model = LogisticRegression()

model.fit(X_train, y_train)

print("\nModel Training Completed")


# Predictions
y_pred = model.predict(X_test)


# Evaluation
accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(y_test, y_pred)

recall = recall_score(y_test, y_pred)

f1 = f1_score(y_test, y_pred)

print("\nAccuracy:", accuracy)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))


# Save model
joblib.dump(model, 'models/sentiment_model.pkl')

# Save vectorizer
joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')

# Save metrics

metrics = {

    "accuracy": round(accuracy * 100, 2),
    "precision": round(precision * 100, 2),
    "recall": round(recall * 100, 2),
    "f1_score": round(f1 * 100, 2)
}

with open('models/model_metrics.json', 'w') as f:

    json.dump(metrics, f)

print("\nModel & Vectorizer Saved Successfully")