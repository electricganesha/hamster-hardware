# sensors.py
# Utility functions for reading temperature and humidity

TEMP_PATH = "/sys/bus/iio/devices/iio:device0/in_temp_input"
HUMIDITY_PATH = "/sys/bus/iio/devices/iio:device0/in_humidityrelative_input"

def read_first_line(filename):
    try:
        with open(filename, "rt") as f:
            value = int(f.readline())
        return True, value
    except Exception:
        return False, -1

def get_temperature():
    flag, temp = read_first_line(TEMP_PATH)
    return temp // 1000 if flag else None

def get_humidity():
    flag, hum = read_first_line(HUMIDITY_PATH)
    return hum // 1000 if flag else None
