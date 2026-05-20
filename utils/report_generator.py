from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

styles = getSampleStyleSheet()


def generate_report(data, output_path):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter
    )

    elements = []

    # TITLE

    title = Paragraph(

        "<b>Intelligent WhatsApp Analytics Report</b>",

        styles['Title']

    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    # SECTION 1

    elements.append(

        Paragraph(

            "<b>1. Chat Statistics</b>",

            styles['Heading2']

        )
    )

    stats_text = f"""

    Total Messages: {data['total_messages']}<br/>
    Total Users: {data['total_users']}<br/>
    Total Words: {data['total_words']}<br/>
    Total Links: {data['total_links']}<br/>

    """

    elements.append(
        Paragraph(stats_text, styles['BodyText'])
    )

    elements.append(Spacer(1, 20))

    # SECTION 2

    elements.append(

        Paragraph(

            "<b>2. Sentiment Analysis</b>",

            styles['Heading2']

        )
    )

    sentiment_text = f"""

    Positive Messages: {data['positive']}<br/>
    Negative Messages: {data['negative']}<br/>

    """

    elements.append(
        Paragraph(sentiment_text, styles['BodyText'])
    )

    elements.append(Spacer(1, 20))

    # SECTION 3

    elements.append(

        Paragraph(

            "<b>3. AI Personality Insights</b>",

            styles['Heading2']

        )
    )

    for user, insight in data['personality_insights'].items():

        text = f"<b>{user}</b>: {insight}<br/><br/>"

        elements.append(
            Paragraph(text, styles['BodyText'])
        )

    elements.append(Spacer(1, 20))

    # SECTION 4

    elements.append(

        Paragraph(

            "<b>4. Engagement Scores</b>",

            styles['Heading2']

        )
    )

    for user, score in data['engagement_scores'].items():

        text = f"""

        <b>{user}</b><br/>
        Engagement Score: {score['score']}<br/><br/>

        """

        elements.append(
            Paragraph(text, styles['BodyText'])
        )

    elements.append(Spacer(1, 20))

    # SECTION 5

    elements.append(

        Paragraph(

            "<b>5. Night Owl Detection</b>",

            styles['Heading2']

        )
    )

    for user, night in data['night_owl_data'].items():

        text = f"""

        <b>{user}</b><br/>
        Night Activity: {night['night_percentage']}%<br/><br/>

        """

        elements.append(
            Paragraph(text, styles['BodyText'])
        )

    elements.append(Spacer(1, 20))

    # SECTION 6

    elements.append(

        Paragraph(

            "<b>6. Smart Recommendations</b>",

            styles['Heading2']

        )
    )

    recommendations = [

        "Maintain positive communication for better engagement.",

        "Users with delayed response behavior should improve participation.",

        "High night-time activity patterns were detected in several users.",

        "Strong interaction patterns indicate active group collaboration."

    ]

    for rec in recommendations:

        elements.append(
            Paragraph(f"• {rec}", styles['BodyText'])
        )

    elements.append(Spacer(1, 20))

    # SECTION 7

    elements.append(

        Paragraph(

            "<b>7. Friendship Interaction Graph</b>",

            styles['Heading2']

        )
    )

    try:

        graph = Image(
            'static/images/friendship_graph.png',
            width=400,
            height=300
        )

        elements.append(graph)

    except:

        pass

    doc.build(elements)