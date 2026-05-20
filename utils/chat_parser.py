from utils.nlp_preprocessing import clean_text
import re
import pandas as pd


def parse_chat(file_path):

    # Read file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    # Pattern for WhatsApp exported chat
    pattern = r'\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s?[APMapm ]{2,4})\]\s'

    # Extract dates
    dates = re.findall(pattern, data)

    # Split messages
    messages = re.split(pattern, data)[1:]

    date_list = []
    user_list = []
    message_list = []

    # Process extracted data
    for i in range(0, len(messages), 2):

        try:
            date = messages[i]
            message = messages[i + 1]

            date_list.append(date)

            # Extract user and message
            entry = re.split(r'([^:]+):\s', message, maxsplit=1)

            if len(entry) >= 3:
                user = entry[1].strip()
                msg = entry[2].strip()

            else:
                user = 'Group Notification'
                msg = message.strip()

            user_list.append(user)
            message_list.append(msg)

        except:
            pass

    # Create dataframe
    df = pd.DataFrame({
        'Date': date_list,
        'User': user_list,
        'Message': message_list
    })

    # Convert to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Only_date'] = df['Date'].dt.date
    # Clean messages
    df['Cleaned_Message'] = df['Message'].apply(clean_text)

    return df