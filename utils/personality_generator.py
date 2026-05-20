def generate_personality_insights(

        engagement_scores,

        response_data,

        night_owl_data,

        user_sentiments

):
    insights = {}

    for user in engagement_scores.keys():

        score = engagement_scores[user]['score']

        sentiment = user_sentiments[user]['label']

        response = response_data[user]['avg_response']

        night_percent = night_owl_data[user]['night_percentage']

        text = ""

        # ENGAGEMENT

        if score >= 75:

            text += (
                f"{user} is a highly engaged participant "
                "who actively contributes to conversations. "
            )

        elif score >= 50:

            text += (
                f"{user} shows moderate engagement "
                "within the chat environment. "
            )

        else:

            text += (
                f"{user} appears less active "
                "and participates minimally in discussions. "
            )

        # NIGHT ACTIVITY

        if night_percent >= 40:

            text += (
                "The user is highly active during late-night hours, "
                "indicating night-owl behavior. "
            )

        else:

            text += (
                "The user mostly communicates during regular daytime hours. "
            )

        # RESPONSE SPEED

        if response <= 10:

            text += (
                "Response behavior indicates quick interaction "
                "and strong conversational interest. "
            )

        elif response <= 30:

            text += (
                "The user maintains moderate response timing "
                "during conversations. "
            )

        else:

            text += (
                "Delayed response patterns suggest lower conversational urgency. "
            )

        # SENTIMENT

        if "Positive" in sentiment:

            text += (
                "Sentiment analysis reflects a generally positive "
                "communication style."
            )

        elif "Negative" in sentiment:

            text += (
                "Sentiment patterns indicate comparatively negative "
                "communication behavior."
            )

        else:

            text += (
                "The communication style appears emotionally neutral."
            )

        insights[user] = text

    return insights