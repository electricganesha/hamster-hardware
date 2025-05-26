import requests
import time
import math

API_URL = "https://hamster-red.vercel.app/api/hamster-session"

class HamsterSession:
    def __init__(self):
        self.active = False
        self.rotations = 0
        self.rotation_log = []
        self.start = None
        self.last_activity = None

    def start_session(self, now):
        self.active = True
        self.start = now
        self.rotations = 0
        self.rotation_log = []
        print("Session started at", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))

    def log_rotation(self, now, temp, hum):
        self.rotations += 1
        self.rotation_log.append({
            "timestamp": float(now),  # Make sure it's a float
            "temperature": float(temp) if temp is not None else None,
            "humidity": float(hum) if hum is not None else None
        })
        self.last_activity = now
        print(f"Rotation {self.rotations}: Temp={temp if temp is not None else 'N.A.'}°C, Humidity={hum if hum is not None else 'N.A.'}%")

    def end_session(self):
        session_end = self.last_activity

        session_data = {
            # These are handled by Prisma (id, createdAt)
            "images": [],  # Add image URLs here if any, or leave empty
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
