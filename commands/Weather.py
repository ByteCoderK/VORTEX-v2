import requests
weather = ''
def live_weather(city):
    api_key = "25bd76ae6cf5eb2e0e71604ff5eb2bcd"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    # Check the response code
    if response.status_code == 200:
        # Fetch weather description, temperature, humidity, and wind speed
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        # Speak the weather information
        return weather == print(f"The current weather in {city} is {weather_description},\n\t   The temperature is {temperature} degrees Celsius,\n\t   The humidity is {humidity} percent,\n\t   The wind speed is {wind_speed} meters per second.")
    else:
        # Speak an error message if the response code is not 200 (e.g., city not found)
        return weather == print("Sorry, I couldn't fetch the weather information for the specified city.")