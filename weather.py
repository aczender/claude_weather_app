import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

import requests
from dotenv import load_dotenv

load_dotenv()

CITIES = ["Budapest", "Dublin", "Stockholm", "Athens"]


def fetch_weather(city: str) -> dict:
    api_key = os.environ["OPENWEATHER_API_KEY"]
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return {
        "name": city,
        "condition": data["weather"][0]["description"].capitalize(),
        "max": data["main"]["temp_max"],
        "min": data["main"]["temp_min"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
    }


def build_html(forecasts: list[dict]) -> str:
    today = date.today().strftime("%A, %d %B %Y")
    rows = ""
    for f in forecasts:
        rows += f"""
        <tr>
          <td style="padding:12px 16px;font-weight:600">{f['name']}</td>
          <td style="padding:12px 16px">{f['condition']}</td>
          <td style="padding:12px 16px">{f['max']:.0f}°C / {f['min']:.0f}°C</td>
          <td style="padding:12px 16px">{f['humidity']}%</td>
          <td style="padding:12px 16px">{f['wind']:.1f} m/s</td>
        </tr>"""

    return f"""
    <html><body style="font-family:sans-serif;color:#1a1a1a;max-width:600px;margin:auto">
      <h2 style="border-bottom:2px solid #4a90e2;padding-bottom:8px;color:#4a90e2">
        🌤 Daily Weather Report — {today}
      </h2>
      <table style="width:100%;border-collapse:collapse;font-size:15px">
        <thead>
          <tr style="background:#4a90e2;color:#fff">
            <th style="padding:10px 16px;text-align:left">City</th>
            <th style="padding:10px 16px;text-align:left">Condition</th>
            <th style="padding:10px 16px;text-align:left">High / Low</th>
            <th style="padding:10px 16px;text-align:left">Humidity</th>
            <th style="padding:10px 16px;text-align:left">Wind</th>
          </tr>
        </thead>
        <tbody>{rows}
        </tbody>
      </table>
      <p style="color:#888;font-size:12px;margin-top:24px">
        Data from <a href="https://openweathermap.org">OpenWeatherMap</a> · sent automatically
      </p>
    </body></html>"""


def send_email(subject: str, html_body: str) -> None:
    sender = os.environ["GMAIL_ADDRESS"]
    password = os.environ["GMAIL_APP_PASSWORD"]
    recipients_raw = os.environ.get("RECIPIENT_EMAILS", sender)
    recipients = [r.strip() for r in recipients_raw.split(",") if r.strip()]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())


def main():
    forecasts = [fetch_weather(city) for city in CITIES]  # type: ignore[arg-type]
    today = date.today().strftime("%d %b %Y")
    html = build_html(forecasts)
    send_email(f"Weather Report — {today}", html)
    print(f"Email sent for {today}")


if __name__ == "__main__":
    main()
