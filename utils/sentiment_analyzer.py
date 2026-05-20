import joblib
from utils.nlp_preprocessing import clean_text

model = joblib.load('models/sentiment_model.pkl')

# Load TF-IDF
vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
def analyze_sentiment(messages):

    positive = 0
    negative = 0

    sentiment_results = []

    for msg in messages:

        cleaned = clean_text(msg)

        vectorized = vectorizer.transform([cleaned])

        prediction = model.predict(vectorized)[0]

        if prediction == 1:
            positive += 1
            sentiment = "Positive"

        else:
            negative += 1
            sentiment = "Negative"

        sentiment_results.append({
            'message': msg,
            'sentiment': sentiment
        })

    total = positive + negative

    positive_percent = round((positive / total) * 100, 2)
    negative_percent = round((negative / total) * 100, 2)

    return {
        'positive': positive,
        'negative': negative,
        'positive_percent': positive_percent,
        'negative_percent': negative_percent,
        'results': sentiment_results
    }