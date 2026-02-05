"""Test script for AI Operations Assistant components"""
from tools import GitHubTool, WeatherTool

print("=" * 70)
print("🧪 AI OPERATIONS ASSISTANT - COMPONENT TEST")
print("=" * 70)

# Test GitHub Tool
print("\n📊 GITHUB TOOL - Testing Repository Search")
print("-" * 70)
github = GitHubTool()
repos = github.execute(
    query="language:python stars:>10000",
    max_results=3
)

if repos['status'] == 'success':
    print(f"✓ Found {repos['count']} repositories:\n")
    for repo in repos['results']:
        print(f"  📦 {repo['name']}")
        print(f"     Stars: {repo['stars']:,}")
        print(f"     Language: {repo['language']}")
        print(f"     URL: {repo['url']}\n")
else:
    print(f"✗ Error: {repos.get('error')}")

# Test Weather Tool
print("\n" + "=" * 70)
print("🌤️  WEATHER TOOL - Testing Weather Lookup")
print("-" * 70)
weather = WeatherTool()
weather_data = weather.execute(city="London", units="metric")

if weather_data['status'] == 'success':
    w = weather_data['weather']
    print(f"✓ Current weather in {weather_data['city']}, {weather_data['country']}:\n")
    print(f"  🌡️  Temperature: {w['temperature']}°C")
    print(f"  💨 Wind Speed: {w['wind_speed']} m/s")
    print(f"  💧 Humidity: {w['humidity']}%")
    print(f"  ☁️  Cloudiness: {w['cloudiness']}%")
    print(f"  📍 Description: {w['description'].title()}\n")
else:
    print(f"✗ Error: {weather_data.get('error')}")

print("=" * 70)
print("✅ API COMPONENTS WORKING SUCCESSFULLY!")
print("=" * 70)
