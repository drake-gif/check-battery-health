import glob
import os
import platform
import re
import subprocess
import tempfile
import time
from datetime import datetime

import psutil


def format_time(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes = remainder // 60
    return f"{hours}h {minutes}m"


def get_battery_health():
    """Return battery health as a percentage (full capacity vs. original
    design capacity), or None if it can't be determined."""
    system = platform.system()

    try:
        if system == "Windows":
            # Windows generates a battery report; we read capacities from it.
            path = os.path.join(tempfile.gettempdir(), "battery_report.xml")
            subprocess.run(
                ["powercfg", "/batteryreport", "/output", path, "/xml"],
                capture_output=True, check=True,
            )
            with open(path, encoding="utf-8", errors="ignore") as f:
                xml = f.read()
            design = re.search(r"<DesignCapacity>(\d+)</DesignCapacity>", xml)
            full = re.search(r"<FullChargeCapacity>(\d+)</FullChargeCapacity>", xml)
            if design and full:
                return int(full.group(1)) / int(design.group(1)) * 100

        elif system == "Darwin":  # macOS
            out = subprocess.run(
                ["system_profiler", "SPPowerDataType"],
                capture_output=True, text=True, check=True,
            ).stdout
            match = re.search(r"Maximum Capacity:\s*(\d+)%", out)
            if match:
                return float(match.group(1))

        elif system == "Linux":
            for bat in glob.glob("/sys/class/power_supply/BAT*"):
                for full_name, design_name in [
                    ("energy_full", "energy_full_design"),
                    ("charge_full", "charge_full_design"),
                ]:
                    full_file = os.path.join(bat, full_name)
                    design_file = os.path.join(bat, design_name)
                    if os.path.exists(full_file) and os.path.exists(design_file):
                        with open(full_file) as f:
                            full = int(f.read())
                        with open(design_file) as f:
                            design = int(f.read())
                        return full / design * 100
    except Exception:
        pass

    return None


def describe_health(percent):
    if percent >= 80:
        return "Good"
    if percent >= 60:
        return "Fair (battery is wearing out)"
    return "Poor (consider replacing the battery)"


def get_uptime():
    """Return how long the PC has been on since it last started."""
    seconds = int(time.time() - psutil.boot_time())
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes = remainder // 60
    return days, hours, minutes


battery = psutil.sensors_battery()

if battery is None:
    print("No battery detected (this may be a desktop PC).")
else:
    print(f"Battery percentage: {battery.percent:.0f}%")

    if battery.power_plugged:
        print("Status: Charging / plugged in")
    else:
        print("Status: Not charging (running on battery)")

    if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
        print("Time remaining: N/A (plugged in)")
    elif battery.secsleft == psutil.POWER_TIME_UNKNOWN:
        print("Time remaining: Unknown (still calculating)")
    else:
        print(f"Time remaining: {format_time(battery.secsleft)}")

    health = get_battery_health()
    if health is None:
        print("Battery health: Could not be determined on this system")
    else:
        print(f"Battery health: {health:.0f}% - {describe_health(health)}")

# Uptime works on every PC, with or without a battery
days, hours, minutes = get_uptime()
boot = datetime.fromtimestamp(psutil.boot_time()).strftime("%a %d %b, %H:%M")
print(f"PC on for: {days}d {hours}h {minutes}m (started {boot})")
