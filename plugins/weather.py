import requests
import os

class WeatherPlugin:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    async def get_weather(self, city: str) -> str:
        """Get weather for a city"""
        if not self.api_key:
            return "❌ Weather API key not configured. Add OPENWEATHER_API_KEY to .env"
        
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                feels = data['main']['feels_like']
                desc = data['weather'][0]['description']
                humidity = data['main']['humidity']
                
                return f"""🌤️ **Weather in {city.title()}**
                
🌡️ Temperature: {temp}°C (feels like {feels}°C)
☁️ Conditions: {desc.title()}
💧 Humidity: {humidity}%"""
            else:
                return f"❌ City '{city}' not found"
        except Exception as e:
            return f"❌ Weather error: {str(e)}"
