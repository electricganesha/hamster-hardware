import requests
import time

API_URL = "https://hamster-red.vercel.app/api/hamster-session"

class HamsterSession:
    def __init__(self):
        self.active = False
        self.rotations = 0
        self.rotation_log = []
        self.start = None
        self.last_activity = None
        self.last_temp = None
        self.last_hum = None

    def start_session(self, now):
        self.active = True
        self.start = now
        self.rotations = 0
        self.rotation_log = []
        self.last_temp = None
        self.last_hum = None
        print("Session started at", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))

    def log_rotation(self, now, temp, hum):
        # Use last known values if current readings are None
        if temp is None:
            temp = self.last_temp
        else:
            self.last_temp = temp

        if hum is None:
            hum = self.last_hum
        else:
            self.last_hum = hum

        # Ensure values are always floats, fallback to -1.0 if still None
        temp = float(temp) if temp is not None else -1.0
        hum = float(hum) if hum is not None else -1.0

        self.rotations += 1
        self.rotation_log.append({
            "timestamp": float(now),
            "temperature": temp,
            "humidity": hum
        })
        self.last_activity = now

        print(f"Rotation {self.rotations}: Temp={temp}°C, Humidity={hum}%")

    def end_session(self):
        session_end = self.last_activity

        if self.rotations < 5:
            print(f"Session discarded (only {self.rotations} rotations)")
            self.active = False
            self.start = None
            self.last_activity = None
            return

        session_data = {
            "images": [],
            "rotationLog": self.rotation_log
        }

        print("Session ended at", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(session_end)))
        print("Session data:", session_data)

        try:
            response = requests.post(API_URL, json=session_data)
            print("Posted to API, status:", response.status_code)
        except Exception as e:
            print("Failed to post to API:", e)

        self.active = False
        self.start = None
        self.last_activity = None
