from urlextract import URLExtract
from collections import Counter
import emoji
from wordcloud import WordCloud
from collections import Counter


extract = URLExtract()


# Fetch statistics
def fetch_stats(df):

    # Total messages
    total_messages = df.shape[0]

    # Total words
    words = []

    for message in df['Message']:
        words.extend(message.split())

    total_words = len(words)

    # Media messages
    media_messages = df[df['Message'].str.contains('<Media omitted>', na=False)].shape[0]

    # Links shared
    links = []

    for message in df['Message']:
        links.extend(extract.find_urls(message))

    total_links = len(links)

    return total_messages, total_words, media_messages, total_links


# Most busy users
def most_busy_users(df):

    x = df['User'].value_counts().head()

    return x


# Emoji analysis
def emoji_helper(df):

    emojis = []

    for message in df['Message']:

        for char in message:
            if char in emoji.EMOJI_DATA:
                emojis.append(char)

    return Counter(emojis).most_common(10)

# Monthly timeline
def monthly_timeline(df):

    timeline = df.groupby(df['Date'].dt.to_period('M')).count()['Message'].reset_index()

    timeline['Date'] = timeline['Date'].astype(str)

    return timeline

def user_level_analysis(df):

    user_stats = {}

    users = df['User'].unique()

    for user in users:

        user_df = df[df['User'] == user]

        total_messages = user_df.shape[0]

        total_words = user_df['Message'].apply(
            lambda x: len(str(x).split())
        ).sum()

        avg_message_length = user_df['Message'].apply(
            lambda x: len(str(x))
        ).mean()

        user_stats[user] = {
            'messages': total_messages,
            'words': total_words,
            'avg_length': round(avg_message_length, 2)
        }

    return user_stats

def generate_wordcloud(df):

    text = " ".join(df['Cleaned_Message'].dropna())

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis'
    ).generate(text)

    return wordcloud.to_image()


def most_common_words(df):

    words = []

    for message in df['Cleaned_Message'].dropna():

        for word in message.split():

            words.append(word)

    common_words = Counter(words).most_common(10)

    return common_words

def extract_emojis(df):

    emojis = []

    for message in df['Message'].dropna():

        for char in message:

            if char in emoji.EMOJI_DATA:

                emojis.append(char)

    emoji_counts = Counter(emojis).most_common(10)

    return emoji_counts

def daily_timeline(df):

    daily = df.groupby('Only_date').count()['Message'].reset_index()

    return daily

def hourly_timeline(df):

    hourly = df.groupby(df['Date'].dt.hour).count()['Message'].reset_index()

    hourly.columns = ['Hour', 'Messages']

    return hourly

def detect_night_owl(df):

    results = {}

    users = df['User'].unique()

    for user in users:

        user_df = df[df['User'] == user]

        total_msgs = len(user_df)

        if total_msgs == 0:
            continue

        night_msgs = user_df[
            (user_df['Date'].dt.hour >= 22) |
            (user_df['Date'].dt.hour <= 5)
        ]

        night_count = len(night_msgs)

        percentage = round((night_count / total_msgs) * 100, 2)

        if percentage >= 50:
            label = "Night Owl 🌙"

        elif percentage <= 20:
            label = "Early Bird ☀️"

        else:
            label = "Balanced User ⚖️"

        results[user] = {
            "night_percentage": percentage,
            "label": label
        }

    return results

def response_time_analysis(df):

    df = df.sort_values('Date')

    results = {}

    users = df['User'].unique()

    for user in users:

        response_times = []

        previous_time = None
        previous_user = None

        for index, row in df.iterrows():

            current_user = row['User']
            current_time = row['Date']

            if previous_user is not None:

                if current_user == user and previous_user != user:

                    diff = (current_time - previous_time).total_seconds() / 60

                    if diff >= 0:
                        response_times.append(diff)

            previous_time = current_time
            previous_user = current_user

        if len(response_times) > 0:

            avg_response = round(sum(response_times) / len(response_times), 2)

            if avg_response <= 5:
                label = "Fast Responder ⚡"

            elif avg_response <= 30:
                label = "Moderate Responder ⏳"

            else:
                label = "Delayed Responder 🐢"

            results[user] = {
                "avg_response": avg_response,
                "label": label
            }

    return results

def activity_heatmap(df):

    heatmap = df.pivot_table(
        index=df['Date'].dt.day_name(),
        columns=df['Date'].dt.hour,
        values='Message',
        aggfunc='count'
    ).fillna(0)

    # DAY ORDER

    days_order = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ]

    heatmap = heatmap.reindex(days_order)

    return heatmap

def user_sentiment_analysis(df, analyze_sentiment):

    user_sentiments = {}

    users = df['User'].unique()

    for user in users:

        user_df = df[df['User'] == user]

        messages = user_df['Message'].astype(str).tolist()

        sentiment = analyze_sentiment(messages)

        positive = sentiment['positive_percent']

        negative = sentiment['negative_percent']

        # LABEL

        if positive > negative:
            label = "Positive 😊"

        elif negative > positive:
            label = "Negative 😠"

        else:
            label = "Neutral 😐"

        user_sentiments[user] = {
            'positive': positive,
            'negative': negative,
            'label': label
        }

    return user_sentiments

from collections import defaultdict

def friendship_interaction(df):

    interactions = defaultdict(int)

    users = df['User'].tolist()

    # LOOP THROUGH CHAT

    for i in range(len(users) - 1):

        current_user = users[i]

        next_user = users[i + 1]

        # IGNORE SELF INTERACTION

        if current_user != next_user:

            pair = tuple(sorted([current_user, next_user]))

            interactions[pair] += 1

    return interactions
