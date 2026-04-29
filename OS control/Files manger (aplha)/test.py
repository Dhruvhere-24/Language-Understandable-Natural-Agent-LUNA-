import os
from datetime import datetime, timedelta
from typing import List

def get_recent_files(hours: int = 0, days: int = 0) -> List[str]:
    """
    Returns list of file paths from Downloads (including subfolders)
    filtered by given time range and allowed extensions.
    """

    # -------------------------------
    # CONFIG
    # -------------------------------
    allowed_ext = [".pdf", ".docx", ".pptx"]
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")

    current_time = datetime.now()
    allowed_time = timedelta(hours=hours, days=days)

    # -------------------------------
    # COLLECT FILES (RECURSIVE)
    # -------------------------------
    all_files = []

    for root, _, files in os.walk(download_path):
        for file in files:
            full_path = os.path.join(root, file)

            if any(file.lower().endswith(ext) for ext in allowed_ext):
                all_files.append(full_path)

    # -------------------------------
    # SORT (LATEST FIRST)
    # -------------------------------
    all_files.sort(
        key=lambda x: os.path.getmtime(x),
        reverse=True
    )

    # -------------------------------
    # FILTER BY TIME
    # -------------------------------
    result = []

    for f in all_files:
        mod_time = datetime.fromtimestamp(os.path.getmtime(f))

        if (current_time - mod_time) <= allowed_time:
            result.append(f)
        else:
            break  # 🔥 optimization

    return result

if __name__ == "__main__":
    files = get_recent_files(hours=4)
    print(files)
    print("total files are :",len(files))