import datetime

def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good Morning Master."
    elif 12 <= hour < 18:
        return "Good Afternoon Master."
    else:
        return "Good Evening Master."