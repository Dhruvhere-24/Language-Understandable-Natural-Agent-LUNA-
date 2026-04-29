import os
from datetime import datetime, timedelta
import pandas as pd

time_formate = "%Y-%m-%d %I:%M:%S %p"

def is_within_diff(current_time, file_time, hours=None, days=None):
    diff = current_time - file_time
    
    h = hours if hours is not None else 0
    d = days if days is not None else 0
    
    allowed = timedelta(hours=h, days=d)
    
    return diff <= allowed


# -------------------------------
# CURRENT TIME
# -------------------------------
current_time = datetime.now()
print("Current Time:", current_time.strftime(time_formate))


# -------------------------------
# UPT parsing
# -------------------------------
UPT = "5 hrs"

hours = None
days = None

if "hr" in UPT:
    hours = int(UPT.split()[0])

elif "day" in UPT:
    days = int(UPT.split()[0])


# -------------------------------
# 🔥 SCAN DOWNLOADS (RECURSIVE)
# -------------------------------
download_path = os.path.join(os.path.expanduser("~"), "Downloads")

files = []

for root, dirs, filenames in os.walk(download_path):
    for file in filenames:
        full_path = os.path.join(root, file)
        files.append(full_path)


# -------------------------------
# FILTER EXTENSIONS
# -------------------------------
allowed_ext = [".pdf", ".docx", ".pptx"]

filtered_files = [
    f for f in files
    if any(f.lower().endswith(ext) for ext in allowed_ext)
]


# -------------------------------
# SORT (LATEST FIRST)
# -------------------------------
filtered_files.sort(
    key=lambda x: os.path.getmtime(x),
    reverse=True
)


# -------------------------------
# FILTER BY TIME
# -------------------------------
ready_files = []

for f in filtered_files:
    mod_time = datetime.fromtimestamp(os.path.getmtime(f))
    
    if is_within_diff(current_time, mod_time, hours=hours, days=days):
        ready_files.append(f)
    else:
        break   # 🔥 optimization (sorted list)


# -------------------------------
# OUTPUT
# -------------------------------
print("\n📂 Ready Files:\n")

for f in ready_files:
    print(f)