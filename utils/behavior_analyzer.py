import re


def analyze_behavior(df, sentiment_data):

    total_messages = len(df)

    # Average words per message
    df['word_count'] = df['Message'].apply(
        lambda x: len(str(x).split())
    )

    avg_words = df['word_count'].mean()

    # Emoji count
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE
    )

    emoji_count = df['Message'].apply(
        lambda x: len(emoji_pattern.findall(str(x)))
    ).sum()

    # Positive sentiment percentage
    positive_percent = sentiment_data['positive_percent']

    # --- Behavioral Scores ---

    extrovert_score = min(
        100,
        int((total_messages / 10) + (avg_words * 2))
    )

    emotional_score = min(
        100,
        int((emoji_count * 2) + positive_percent)
    )

    active_score = min(
        100,
        int(total_messages / 5)
    )

    formal_score = max(
        0,
        100 - emoji_count
    )

    # --- Labels ---

    extrovert_label = (
        "Extrovert"
        if extrovert_score >= 50
        else "Introvert"
    )

    emotional_label = (
        "Emotional"
        if emotional_score >= 50
        else "Reserved"
    )

    active_label = (
        "Active"
        if active_score >= 50
        else "Passive"
    )

    formal_label = (
        "Formal"
        if formal_score >= 50
        else "Casual"
    )

    return {

        'extrovert_score': extrovert_score,
        'extrovert_label': extrovert_label,

        'emotional_score': emotional_score,
        'emotional_label': emotional_label,

        'active_score': active_score,
        'active_label': active_label,

        'formal_score': formal_score,
        'formal_label': formal_label
    }