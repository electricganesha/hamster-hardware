# Hamster Wheel Logger

This project logs hamster wheel activity using a hall effect sensor and environmental sensors (temperature and humidity) on a Raspberry Pi. It records exercise sessions, calculates statistics, and posts the data to a remote API.

## Features
- Detects wheel rotations using a hall effect sensor (GPIO)
- Logs temperature and humidity at each rotation
- Automatically starts and ends sessions based on activity
- Calculates average temperature and humidity per session
- Posts session data to a remote API
- Designed to run autonomously as a background service

## Project Structure
- `hamster_session.py` — Main script, runs the event loop and handles GPIO
- `sensors.py` — Utility functions for reading temperature and humidity
- `session.py` — Session management, statistics, and API posting

## Requirements
- Raspberry Pi (with GPIO and IIO sensors enabled)
- Python 3
- `requests` library (`pip install requests`)
- Hall effect sensor connected to GPIO pin 4 (BCM numbering)
- Temperature/humidity sensor available via IIO (see `/sys/bus/iio/devices/iio:device0/`)

## Running Manually
```bash
python3 hamster_session.py
```

## Running as a Service (Autonomous)
1. **Create a shell script**

   `run_hamster.sh`:
   ```bash
   #!/bin/bash
   cd /home/cmarques/projects/hamster
   /usr/bin/python3 /home/cmarques/projects/hamster/hamster_session.py
   ```
   Make it executable:
   ```bash
   chmod +x /home/cmarques/projects/hamster/run_hamster.sh
   ```

2. **Create a systemd service**

   `/etc/systemd/system/hamster.service`:
   ```ini
   [Unit]
   Description=Hamster Wheel Logger
   After=network.target

   [Service]
   ExecStart=/home/cmarques/projects/hamster/run_hamster.sh
   WorkingDirectory=/home/cmarques/projects/hamster
   StandardOutput=append:/home/cmarques/projects/hamster/hamster.log
   StandardError=append:/home/cmarques/projects/hamster/hamster_error.log
   Restart=always
   User=cmarques

   [Install]
   WantedBy=multi-user.target
   ```
   Replace `cmarques` with your actual username if different.

3. **Enable and start the service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable hamster.service
   sudo systemctl start hamster.service
   ```

4. **Check status and logs**
   ```bash
   sudo systemctl status hamster.service
   tail -f /home/cmarques/projects/hamster/hamster.log
   ```

## Troubleshooting
- Check `hamster.log` and `hamster_error.log` for output and errors.
- If you get a 400 error from the API, check the printed payload and API response for details.

## Customization
- Edit `API_URL` in `session.py` to point to your API endpoint.
- Adjust GPIO pin or sensor paths as needed for your hardware.

---

Feel free to ask for help with any of the setup steps!
