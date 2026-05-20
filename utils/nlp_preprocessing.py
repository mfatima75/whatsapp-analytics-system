import re
from nltk.corpus import stopwords
from utils.stopwords import ROMAN_URDU_STOPWORDS

# English stopwords
stop_words = set(stopwords.words('english'))

# Roman Urdu stopwords
roman_urdu_stopwords = {
    'hai', 'han', 'ka', 'ki', 'ke', 'ko',
    'me', 'mai', 'main', 'tum', 'hum',
    'ap', 'aap', 'ye', 'wo', 'tha', 'thi',
    'to', 'se', 'par', 'or', 'aur'
}
def clean_text(message):

    # Lowercase
    message = message.lower()
    # Remove URLs
    message = re.sub(r'http\S+', '', message)
    # Remove punctuation
    message = re.sub(r'[^\w\s]', '', message)
    # Remove numbers
    message = re.sub(r'\d+', '', message)
    # Tokenization
    words = message.split()
    filtered_words = []
    for word in words:

        if (
                word not in stop_words
                and word not in ROMAN_URDU_STOPWORDS
                and len(word) > 2
        ):
            filtered_words.append(word)

            return " ".join(filtered_words)
    # Remove stopwords
    cleaned_words = []

    for word in words:
        if word not in stop_words and word not in roman_urdu_stopwords:
            cleaned_words.append(word)
    # Join cleaned words
    cleaned_message = ' '.join(cleaned_words)
    return cleaned_message