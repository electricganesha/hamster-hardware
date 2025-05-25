import RPi.GPIO as GPIO
import time
from sensors import get_temperature, get_humidity
from session import HamsterSession

# --- Configuration ---
SENSOR_PIN = 4  # BCM pin for hall sensor
INACTIVITY_TIMEOUT = 60  # seconds

# --- Main logic ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Hamster Wheel Session Logger (CTRL+C to exit)")

session = HamsterSession()

try:
    while True:
        value = GPIO.input(SENSOR_PIN)
        if value == GPIO.LOW:
            now = time.time()
            if not session.active:
                session.start_session(now)
            temp = get_temperature()
            hum = get_humidity()
            session.log_rotation(now, temp, hum)
            # Debounce: wait for sensor to go HIGH
            while GPIO.input(SENSOR_PIN) == GPIO.LOW:
                time.sleep(0.01)
        else:
            if session.active and session.last_activity and (time.time() - session.last_activity > INACTIVITY_TIMEOUT):
                session.end_session()
            time.sleep(0.05)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
