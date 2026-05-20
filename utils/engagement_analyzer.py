def calculate_engagement(
        busy_users,
        response_data,
        night_owl_data,
        sentiment_data
):

    engagement_scores = {}

    # MAX VALUES FOR NORMALIZATION

    max_messages = max(busy_users.values)

    max_response = max(
        data['avg_response']
        for data in response_data.values()
    )

    # LOOP THROUGH USERS

    for user in busy_users.index:

        # 1. MESSAGE ACTIVITY SCORE

        message_score = (
            busy_users[user] / max_messages
        ) * 40

        # 2. RESPONSE SCORE

        avg_response = response_data[user]['avg_response']

        response_score = (
            1 - (avg_response / max_response)
        ) * 30

        # 3. NIGHT ACTIVITY SCORE

        night_percent = night_owl_data[user]['night_percentage']

        night_score = (
            night_percent / 100
        ) * 10

        # 4. SENTIMENT SCORE

        sentiment_score = (
            sentiment_data['positive_percent'] / 100
        ) * 20

        # FINAL SCORE

        total_score = round(
            message_score +
            response_score +
            night_score +
            sentiment_score,
            2
        )

        # LABELS

        if total_score >= 75:
            label = "Highly Engaged 🔥"

        elif total_score >= 50:
            label = "Moderately Active ⚡"

        else:
            label = "Passive User 💤"

        engagement_scores[user] = {
            'score': total_score,
            'label': label
        }

    return engagement_scores