Battery Checker

A simple Python script that reports your laptop's battery information and how long your PC has been on, right from the terminal.

Features

- Battery percentage: current charge level
- Charging status: whether the laptop is plugged in or running on battery
- Time remaining: estimated battery life left till power off (when unplugged)
- Battery health: how much charge the battery can hold compared to when it was new
- Uptime: how long the PC has been on since it last started

Requirements

- Python 3.7 or newer
- The `psutil` library/ not a must
- Windows, macOS or Linux

Setup and Running

Option 1: Terminal

1. Put `battery_status.py` in a folder, e.g. `battery-project`.
2. Open a terminal in that folder.
3. Install the dependency:
   ```
   pip install psutil
   ```
4. Run the script:
   ```
   python battery_status.py
   ```
   On macOS/Linux, use `pip3` and `python3` if the commands above don't work.

Option 2: VS Code

1. Install [VS Code](https://code.visualstudio.com) and the Python extension (by Microsoft).
2. Go to File → Open Folder and select your project folder.
3. Open `battery_status.py`.
4. Open terminal and run `pip install psutil`. 
5. Click the Run button at the top right, or run `python battery_status.py` in the terminal.


