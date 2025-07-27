import random


def weather_info(location: str):
    """Return fake weather information for a given location."""
    temperature = random.randint(15, 40)  # Random temperature between 15°C and 40°C
    return f"The weather in {location} is {temperature}°C and sunny."