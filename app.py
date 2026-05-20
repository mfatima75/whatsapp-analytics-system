from utils.summary_generator import generate_behavior_summary
from utils.behavior_analyzer import analyze_behavior
from utils.sentiment_analyzer import analyze_sentiment
from utils.helper import fetch_stats, most_busy_users, monthly_timeline
from utils.chat_parser import parse_chat
from utils.personality_generator import generate_personality_insights
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from flask import Flask, render_template, request,send_file
import plotly
import plotly.express as px
import json
import os
from utils.engagement_analyzer import calculate_engagement
from utils.report_generator import generate_report
from utils.helper import (
    hourly_timeline,
    fetch_stats,
    most_busy_users,
    monthly_timeline,
    daily_timeline,
    user_level_analysis,
    generate_wordcloud,
    most_common_words,
    extract_emojis,
    detect_night_owl,
    response_time_analysis,
    activity_heatmap,
    user_sentiment_analysis,
    friendship_interaction
)

app = Flask(__name__)
analytics_data = {}
busy_users = {}
user_analysis = {}
timeline_json = None
daily_timeline_json = None
hourly_timeline_json = None



# Upload Folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():

    return render_template(
        'index.html',
        **analytics_data
    )


@app.route('/sentiment')
def sentiment():

    return render_template(
        'sentiment.html',
        positive=analytics_data.get('positive', 0),
        negative=analytics_data.get('negative', 0),
        positive_percent=analytics_data.get('positive_percent', 0),
        negative_percent=analytics_data.get('negative_percent', 0),
        pie_chart_json=analytics_data.get('pie_chart_json'),
        user_sentiments=analytics_data.get('user_sentiments')
    )


@app.route('/behavior')
def behavior():

    return render_template(
        'behavior.html',
        behavior_data=analytics_data.get('behavior_data'),
        behavior_summary=analytics_data.get('behavior_summary'),
        night_owl_data = analytics_data.get('night_owl_data'),
        response_data=analytics_data.get('response_data'),
        users_list=analytics_data.get('users_list'),
        engagement_scores=analytics_data.get('engagement_scores'),
        user_sentiments=analytics_data.get('user_sentiments'),
        personality_insights=analytics_data.get('personality_insights'),
        friendship_graph=analytics_data.get('friendship_graph')
    )

    return render_template('behavior.html')

@app.route('/users')
def users_page():

    return render_template(
        'users.html',
        busy_users=busy_users,
        user_analysis=user_analysis,
        timeline_json=timeline_json,
        daily_timeline_json=daily_timeline_json,
        hourly_timeline_json=hourly_timeline_json,
        night_owl_data=analytics_data.get('night_owl_data'),
        heatmap_json=analytics_data.get('heatmap_json')
    )


@app.route('/evaluation')
def evaluation():

    return render_template(
        'evaluation.html',
        model_metrics=analytics_data.get('model_metrics')
    )


@app.route('/upload', methods=['POST'])
def upload_chat():
    global analytics_data
    global busy_users
    global user_analysis
    global timeline_json
    global daily_timeline_json
    global hourly_timeline_json

    if 'chat_file' not in request.files:
        return "No file uploaded"

    file = request.files['chat_file']

    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    file.save(filepath)

    # Parse chat
    df = parse_chat(filepath)

    users_list = df['User'].unique().tolist()

    # Basic stats
    # Fetch analytics
    total_messages, total_words, media_messages, total_links = fetch_stats(df)

    # Total users
    total_users = df['User'].nunique()

    # Most busy users
    busy_users = most_busy_users(df)

    user_analysis = user_level_analysis(df)

    # WordCloud
    wordcloud_image = generate_wordcloud(df)

    wordcloud_path = 'static/images/wordcloud.png'

    wordcloud_image.save(wordcloud_path)

    # Top words
    top_words = most_common_words(df)

    emoji_data = extract_emojis(df)

    if emoji_data:

        emoji_df = pd.DataFrame(
            emoji_data,
            columns=['Emoji', 'Count']
        )

        emoji_fig = px.pie(
            emoji_df,
            names='Emoji',
            values='Count',
            title='Emoji Usage Distribution'
        )

        emoji_json = json.dumps(
            emoji_fig,
            cls=plotly.utils.PlotlyJSONEncoder
        )

    else:

        emoji_json = None
    # Monthly timeline
    timeline = monthly_timeline(df)

    daily_data = daily_timeline(df)

    daily_fig = px.line(
        daily_data,
        x='Only_date',
        y='Message',
        markers=True,
        title='Daily Chat Activity'
    )

    daily_fig.update_layout(
        template='plotly_white',
        height=400
    )

    daily_timeline_json = json.dumps(
        daily_fig,
        cls=plotly.utils.PlotlyJSONEncoder
    )

    hourly_data = hourly_timeline(df)

    heatmap_data = activity_heatmap(df)

    heatmap_fig = px.imshow(

        heatmap_data,

        labels=dict(
            x="Hour of Day",
            y="Day",
            color="Messages"
        ),

        title="Weekly Activity Heatmap",

        aspect="auto"
    )

    heatmap_fig.update_layout(
        template='plotly_white',
        height=500
    )

    heatmap_json = json.dumps(
        heatmap_fig,
        cls=plotly.utils.PlotlyJSONEncoder
    )


    night_owl_data = detect_night_owl(df)
    response_data = response_time_analysis(df)

    hourly_fig = px.line(
        hourly_data,
        x='Hour',
        y='Messages',
        markers=True,
        title='Hourly Chat Activity'
    )

    hourly_fig.update_layout(
        template='plotly_white',
        height=400
    )

    hourly_timeline_json = json.dumps(
        hourly_fig,
        cls=plotly.utils.PlotlyJSONEncoder
    )

    print("\nHourly Timeline Generated Successfully")
    print(hourly_data.head())

    # Convert Series to DataFrame
    busy_df = busy_users.reset_index()

    busy_df.columns = ['User', 'Messages']

    # Plotly Bar Chart
    fig = px.bar(
        busy_df,
        x='User',
        y='Messages',
        color='Messages',
        title='Top Active Users',
        text='Messages'
    )

    # Chart Styling
    fig.update_layout(
        template='plotly_white',
        height=400
    )

    # Convert chart to JSON
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # Timeline Line Chart
    timeline_fig = px.line(
        timeline,
        x='Date',
        y='Message',
        markers=True,
        title='Monthly Chat Activity'
    )

    timeline_fig.update_layout(
        template='plotly_white',
        height=400
    )

    timeline_json = json.dumps(
        timeline_fig,
        cls=plotly.utils.PlotlyJSONEncoder
    )

    # Extract messages
    messages = df['Message'].astype(str).tolist()

    # Sentiment Analysis
    sentiment_data = analyze_sentiment(messages)

    user_sentiments = user_sentiment_analysis(
        df,
        analyze_sentiment
    )
    # Sentiment counts

    positive = sentiment_data['positive']

    negative = sentiment_data['negative']

    positive_percent = sentiment_data['positive_percent']

    negative_percent = sentiment_data['negative_percent']

    # Behavioral Intelligence
    behavior_data = analyze_behavior(df, sentiment_data)

    # Generate AI Summary
    behavior_summary = generate_behavior_summary(behavior_data)

    interaction_data = friendship_interaction(df)


    G = nx.Graph()

    # ADD EDGES

    for pair, weight in interaction_data.items():

        # SHOW ONLY STRONG INTERACTIONS

        if weight >= 5:
            user1, user2 = pair

            G.add_edge(user1, user2, weight=weight)



    # DRAW GRAPH

    plt.figure(figsize=(10, 8))

    pos = nx.spring_layout(G, seed=42)

    edges = G.edges(data=True)

    weights = [edge[2]['weight'] / 5 for edge in edges]

    nx.draw(

        G,
        pos,

        with_labels=True,

        node_size=3000,

        font_size=10,

        width=[w * 0.5 for w in weights]

    )

    graph_path = 'static/images/friendship_graph.png'

    plt.savefig(graph_path)

    plt.close()
    engagement_scores = calculate_engagement(
        busy_users,
        response_data,
        night_owl_data,
        sentiment_data
    )

    personality_insights = generate_personality_insights(

        engagement_scores,

        response_data,

        night_owl_data,

        user_sentiments

    )

    # Load model evaluation metrics

    with open('models/model_metrics.json', 'r') as f:

        model_metrics = json.load(f)

    print("\nBehavior Summary:")
    print(behavior_summary)

    print("\nBehavior Analysis Completed")
    print(behavior_data)

    # Sentiment Pie Chart
    sentiment_labels = ['Positive', 'Negative']

    sentiment_values = [
        sentiment_data['positive'],
        sentiment_data['negative']
    ]

    pie_fig = px.pie(
        names=sentiment_labels,
        values=sentiment_values,
        title='Sentiment Distribution',
        hole=0.4
    )

    pie_fig.update_layout(
        template='plotly_white',
        height=400
    )

    # Convert to JSON
    pie_chart_json = json.dumps(
        pie_fig,
        cls=plotly.utils.PlotlyJSONEncoder
    )

    print("\nSentiment Analysis Completed")
    print(sentiment_data)

    print(df[['Message', 'Cleaned_Message']].head())

    # Store report data

    analytics_data = {

        "total_messages": total_messages,
        "total_users": total_users,
        "total_words": total_words,
        "media_messages": media_messages,
        "total_links": total_links,
        "response_data": response_data,
        "users_list": users_list,
        "engagement_scores": engagement_scores,
        "personality_insights": personality_insights,

        "busy_users": busy_users,
        "user_analysis": user_analysis,

        "graph_json": graph_json,
        "timeline_json": timeline_json,
        "daily_timeline_json":daily_timeline_json,

        "positive": positive,
        "negative": negative,
        "positive_percent": positive_percent,
        "negative_percent": negative_percent,
        "heatmap_json": heatmap_json,
        "user_sentiments": user_sentiments,

        "pie_chart_json": pie_chart_json,
        "night_owl_data": night_owl_data,

        "behavior_data": behavior_data,
        "behavior_summary": behavior_summary,

        "wordcloud_path": wordcloud_path,
        "top_words": top_words,
        "interaction_data": interaction_data,
        "friendship_graph": graph_path,

        "emoji_data": emoji_data,
        "emoji_json": emoji_json,

        "model_metrics": model_metrics
    }

    return render_template(
        'index.html',
        total_messages=total_messages,
        total_users=total_users,
        total_words=total_words,
        media_messages=media_messages,
        total_links=total_links,
        busy_users=busy_users,
        graph_json=graph_json,
        timeline_json=timeline_json,
        daily_timeline_json=daily_timeline_json,
        pie_chart_json=pie_chart_json,
        # behavior_data=behavior_data,
        # behavior_summary=behavior_summary,
        user_analysis=user_analysis,
        top_words=top_words,
        wordcloud_path=wordcloud_path,
        emoji_data=emoji_data,
        emoji_json=emoji_json,
        model_metrics=model_metrics,
        hourly_timeline_json=hourly_timeline_json,

        upload_success=True,

        positive=sentiment_data['positive'],
        negative=sentiment_data['negative'],
        positive_percent=sentiment_data['positive_percent'],
        negative_percent=sentiment_data['negative_percent']
    )

@app.route('/download-report')

def download_report():

    report_path = 'static/reports/chat_analysis_report.pdf'

    data = {

        "total_messages": analytics_data.get('total_messages', 0),

        "total_users": analytics_data.get('total_users', 0),

        "total_words": analytics_data.get('total_words', 0),

        "total_links": analytics_data.get('total_links', 0),

        "positive": analytics_data.get('positive', 0),

        "negative": analytics_data.get('negative', 0),

        "personality_insights":
            analytics_data.get('personality_insights', {}),

        "engagement_scores":
            analytics_data.get('engagement_scores', {}),

        "night_owl_data":
            analytics_data.get('night_owl_data', {})

    }

    generate_report(data, report_path)

    return send_file(
        report_path,
        as_attachment=True
    )
if __name__ == '__main__':
    app.run(debug=True)