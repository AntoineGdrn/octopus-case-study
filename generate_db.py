import os
import numpy as np
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import sqlite3
import sys

if os.path.exists("database.db"):
    os.remove("database.db")  # Supprime le fichier existant pour repartir à zéro

def log_inline(msg, width=80):
    sys.stdout.write("\r" + f"{msg:<{width}}")
    sys.stdout.flush()

conn = sqlite3.connect("database.db")  # crée le fichier
cur = conn.cursor()

cur.execute("""
CREATE TABLE HouseholdParticipation (
    HouseholdId INTEGER PRIMARY KEY AUTOINCREMENT,
    HasParticipated BOOLEAN NOT NULL
);
""")
cur.execute("""
CREATE TABLE CalendarSessions (
    SessionId INTEGER PRIMARY KEY AUTOINCREMENT,
    SessionDatetime DATETIME NOT NULL
);
""")

cur.execute("""
CREATE TABLE LoadCurves (
    LoadCurveId INTEGER PRIMARY KEY AUTOINCREMENT,
    Datetime DATETIME NOT NULL,
    Consumption INTEGER NOT NULL,
    HouseholdId INTEGER NOT NULL,
    FOREIGN KEY (HouseholdId)
        REFERENCES HouseholdParticipation(HouseholdId)
        ON DELETE CASCADE
);
""")

cur.execute("""
CREATE TABLE EnergyPrices (
    EnergyPriceId INTEGER PRIMARY KEY AUTOINCREMENT,
    StartDatetime DATETIME NOT NULL,
    EndDatetime DATETIME NOT NULL,
    PriceDayAhead DECIMAL(10,2) NOT NULL,
    Area VARCHAR(50) NOT NULL
);
""")

files = {
    "household_participation": "participants_eco_sessions.csv",
    "calendar_sessions": "calendrier_sessions.csv",
    "load_curves": "courbes_charge.csv",
    "energy_prices": "fr_prices_2025.csv"
}

file_path = os.path.join("./data", files["household_participation"])
if not os.path.exists(file_path):
    log_inline(f"File {file_path} not found. Please make sure it exists in the current directory.")
    exit(1)
df = pd.read_csv(file_path, delimiter=";")
for _, row in df.iterrows():
    id = row["id"]
    has_participated = row["eco_session_participant"]
    if has_participated == "OUI":
        has_participated = 1
    else:
        has_participated = 0
    cur.execute("INSERT INTO HouseholdParticipation (HouseholdId, HasParticipated) VALUES (?, ?)", (id, has_participated))

file_path = os.path.join("./data", files["load_curves"])
if not os.path.exists(file_path):
    log_inline(f"File {file_path} not found. Please make sure it exists in the current directory.")
    exit(1)
df = pd.read_csv(file_path, delimiter=";")
for _, row in df.iterrows():
    id = row["id"]
    date = row["date"]
    dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=ZoneInfo("Europe/Paris"))
    consumption = row["consumption (W)"]
    cur.execute("INSERT INTO LoadCurves (Datetime, Consumption, HouseholdId) VALUES (?, ?, ?)", (dt.isoformat(), consumption, id))


file_path = os.path.join("./data", files["calendar_sessions"])
if not os.path.exists(file_path):
    log_inline(f"File {file_path} not found. Please make sure it exists in the current directory.")
    exit(1)
df = pd.read_csv(file_path, delimiter=";")
for _, row in df.iterrows():
    date = row["date"]
    hour = row["heure"]
    dt = datetime.strptime(f"{date} {hour}", "%d/%m/%Y %H")
    dt = dt.replace(tzinfo=ZoneInfo("Europe/Paris"))
    cur.execute("INSERT INTO CalendarSessions (SessionDatetime) VALUES (?)", (dt.isoformat(),))


file_path = os.path.join("./data", files["energy_prices"])
if not os.path.exists(file_path):
    log_inline(f"File {file_path} not found. Please make sure it exists in the current directory.")
    exit(1)
df = pd.read_csv(file_path, delimiter=";")
for _, row in df.iterrows():
    date = row["Date"]
    splited_date = date.split("-")
    start_datetime = datetime.strptime(f"{splited_date[0].strip()}", "%d/%m/%Y %H:%M:%S").replace(tzinfo=ZoneInfo("Europe/Paris")).isoformat()
    end_datetime = datetime.strptime(f"{splited_date[1].strip()}", "%d/%m/%Y %H:%M:%S").replace(tzinfo=ZoneInfo("Europe/Paris")).isoformat()
    priceDayAhead = row["Day-ahead Price (EUR/MWh)"]
    area = row["Area"]
    cur.execute("INSERT INTO EnergyPrices (StartDatetime, EndDatetime, PriceDayAhead, Area) VALUES (?, ?, ?, ?)", (start_datetime, end_datetime, priceDayAhead, area))

conn.commit()
conn.close()