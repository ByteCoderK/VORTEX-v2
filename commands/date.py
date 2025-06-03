import datetime

def date():
    return datetime.datetime.now().strftime("Today is %B %d, %Y")

print(date())

