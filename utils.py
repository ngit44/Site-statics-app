import os
import requests
import pandas as pd
from datetime import datetime

API_TOKEN = os.getenv("TOKEN")
API_BASE_URL = "https://developers.flowworks.com/fwapi/v2"

START_DATE_STR = "2025-01-01T00:00:00"
END_DATE_STR = "2025-04-01T00:00:00"

def fetch_timeseries(site_id, channel_id):
    url = f"{API_BASE_URL}/sites/{site_id}/channels/{channel_id}/data"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params = {
        "startDateFilter": START_DATE_STR,
        "endDateFilter": END_DATE_STR
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data["Resources"])
            df["TimeStamp"] = pd.to_datetime(df["DataTime"])
            df["DataValue"] = pd.to_numeric(df["DataValue"], errors="coerce")
            return df
        else:
            return None
    except:
        return None

def get_site_summary(site_id, channel_id):
    df = fetch_timeseries(site_id, channel_id)
    if df is None or df.empty:
        return {"error": "No data found for this site/channel."}
    values = df["DataValue"].dropna()
    if values.empty:
        return {"error": "No valid numeric data available."}
    return {
        "min": round(values.min(), 2),
        "max": round(values.max(), 2),
        "avg": round(values.mean(), 2)
    }
