# 🌤 Daily Weather Email App

A Python script that fetches current weather data for selected cities and sends a daily HTML email summary via Gmail. Designed to run automatically in the cloud (no Mac required) using a Claude scheduled agent.

---

## Features

- Fetches live weather data from [OpenWeatherMap](https://openweathermap.org/)
- Sends a styled HTML email with a summary table
- Supports multiple recipient emails
- Runs daily in the cloud via Claude scheduled agent

---

## Cities Tracked

| City | Country |
|------|---------|
| Budapest | Hungary |
| Dublin | Ireland |
| Stockholm | Sweden |
| Athens | Greece |

---

## Email Summary Includes

| Column | Description |
|--------|-------------|
| City | City name |
| Condition | Weather description (e.g. "Partly cloudy") |
| High / Low | Max and min temperature in °C |
| Humidity | Relative humidity in % |
| Wind | Wind speed in m/s |

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/aczender/claude_weather_app.git
cd claude_weather_app
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file

```bash
cp .env.example .env
```

Then fill in your credentials in `.env`:

```env
GMAIL_ADDRESS=you@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
RECIPIENT_EMAILS=you@gmail.com,friend@gmail.com
OPENWEATHER_API_KEY=your_api_key_here
```

> ⚠️ `.env` is listed in `.gitignore` and will never be committed.

---

## Credentials

### Gmail App Password
1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Create a new app password (name it e.g. "Weather App")
3. Copy the 16-character code into `GMAIL_APP_PASSWORD`

> This is **not** your regular Gmail password. 2FA must be enabled on your Google account.

### OpenWeatherMap API Key
1. Sign up at [openweathermap.org](https://openweathermap.org/)
2. Go to **API Keys** in your account dashboard
3. Copy your key into `OPENWEATHER_API_KEY`

> New API keys take ~10 minutes to activate after creation.

---

## Run Manually

```bash
python3 weather.py
```

Expected output:
```
Email sent for 01 Jun 2026
```

---

## Automated Daily Runs

The script is scheduled to run daily via a **Claude scheduled agent** — no server or Mac required. The agent runs in the cloud and triggers `weather.py` on a cron schedule.

---

## Project Structure

```
weather_app/
├── weather.py          # Main script
├── requirements.txt    # Python dependencies
├── .env                # Your credentials (not committed)
├── .env.example        # Credentials template
├── .gitignore
└── README.md
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | HTTP calls to OpenWeatherMap API |
| `python-dotenv` | Load credentials from `.env` file |

---

## Customisation

**Change cities** — edit the `CITIES` list in `weather.py`:
```python
CITIES = ["Budapest", "Dublin", "Stockholm", "Athens"]
```

**Add recipients** — add comma-separated emails in `.env`:
```env
RECIPIENT_EMAILS=you@gmail.com,second@gmail.com,third@gmail.com
```

**Change units** — modify the `units` param in `fetch_weather()`:
```python
params = {"q": city, "appid": api_key, "units": "imperial"}  # °F
```

---

## Roadmap

- [ ] Add 5-day forecast (OpenWeatherMap `/forecast` endpoint)
- [ ] Add weather icons to the email
- [ ] Support more cities via config file
- [ ] Add a weekly digest mode

---

## License

MIT
