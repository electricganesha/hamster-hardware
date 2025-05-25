# session.py
# Session management logic for hamster wheel
import requests
import time
import math

API_URL = "https://hamster-red.vercel.app/api/hamster-session"

class HamsterSession:
    def __init__(self):
        self.active = False
        self.rotations = 0
        self.rotation_times = []
        self.temperatures = []
        self.humidities = []
        self.start = None
        self.last_activity = None

    def start_session(self, now):
        self.active = True
        self.start = now
        self.rotations = 0
        self.rotation_times = []
        self.temperatures = []
        self.humidities = []
        print("Session started at", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))

    def log_rotation(self, now, temp, hum):
        self.rotations += 1
        self.rotation_times.append(now)
        self.temperatures.append(temp)
        self.humidities.append(hum)
        self.last_activity = now
        print(f"Rotation {self.rotations}: Temp={temp if temp is not None else 'N.A.'}°C, Humidity={hum if hum is not None else 'N.A.'}%")

    def end_session(self):
        session_end = self.last_activity
        valid_temps = [t for t in self.temperatures if t is not None and not (isinstance(t, float) and math.isnan(t))]
        valid_hums = [h for h in self.humidities if h is not None and not (isinstance(h, float) and math.isnan(h))]
        avg_temp = (sum(valid_temps) / len(valid_temps)) if valid_temps else None
        avg_hum = (sum(valid_hums) / len(valid_hums)) if valid_hums else None
        # Convert timestamps to ISO 8601 strings for DateTime compatibility
        start_time_iso = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(self.start)) if self.start else None
        end_time_iso = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(session_end)) if session_end else None
        session_data = {
            "startTime": start_time_iso,
            "endTime": end_time_iso,
            "rotations": self.rotations,
            "temperature": avg_temp,
            "humidity": avg_hum,
            "image": None  # Optional, set to a string if you have an image
        }
        print("Session ended at", end_time_iso)
        print("Session data:", session_data)
        try:
            response = requests.post(API_URL, json=session_data)
            print("Posted to API, status:", response.status_code)
            print("API response:", response.text)
        except Exception as e:
            print("Failed to post to API:", e)
        self.active = False
        self.start = None
        self.last_activity = None
