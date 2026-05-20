def generate_behavior_summary(behavior_data):

    summary = "This user demonstrates "

    # Social Style
    if behavior_data['extrovert_label'] == "Extrovert":
        summary += "highly social and expressive communication behavior, "
    else:
        summary += "more reserved and introverted communication behavior, "

    # Emotional Style
    if behavior_data['emotional_label'] == "Emotional":
        summary += "with emotionally engaging interaction patterns. "
    else:
        summary += "with controlled emotional expression. "

    # Participation
    if behavior_data['active_label'] == "Active":
        summary += "The user actively participates in conversations "
    else:
        summary += "The user shows relatively passive participation "

    # Communication Style
    if behavior_data['formal_label'] == "Formal":
        summary += "while maintaining a formal communication style."
    else:
        summary += "while preferring a casual communication style."

    return summary