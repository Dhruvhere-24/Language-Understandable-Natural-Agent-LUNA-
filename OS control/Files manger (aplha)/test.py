import os
import shutil
from datetime import datetime, timedelta
from typing import List, Dict

def get_recent_files(hours: int = 0, days: int = 0) -> List[str]:
    """
    Returns list of file paths from Downloads (including subfolders)
    filtered by given time range and allowed extensions.
    """
    allowed_ext = [".pdf", ".docx", ".pptx"]
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")

    current_time = datetime.now()
    allowed_time = timedelta(hours=hours, days=days)

    all_files = []

    for root, _, files in os.walk(download_path):
        for file in files:
            full_path = os.path.join(root, file)

            if any(file.lower().endswith(ext) for ext in allowed_ext):
                all_files.append(full_path)

    all_files.sort(
        key=lambda x: os.path.getmtime(x),
        reverse=True
    )

    result = []

    for f in all_files:
        mod_time = datetime.fromtimestamp(os.path.getmtime(f))

        if (current_time - mod_time) <= allowed_time:
            result.append(f)
        else:
            break  # 🔥 optimization

    return result

def move_all_files(file_paths: Dict[str, List[str]], base_path: str):

    for path, val in file_paths.items():
        file_name = path

        # create folder path
        drop_path = os.path.join(base_path, val[1])

        # 🔥 ensure folder exists
        os.makedirs(drop_path, exist_ok=True)

        # final destination (include file name)
        destination = os.path.join(drop_path, os.path.basename(file_name))

        shutil.move(file_name, destination)

        print(f"Moved → {destination}")

def Dummy_model(paths: Dict[int, str]) -> Dict[str, List[str]] :
    res = dict()

    for key, val in paths.items():

        # Vector model area {
        subject_code = "xxx0z"
        subject_name = "File_testing"
        path = val
        # }

        if subject_code == "None" or subject_name == "None":
            continue

        if path not in res:
            res[path] = []

        # append tuple
        res[path].extend([subject_code, subject_name])


    return res



files = get_recent_files(1)
mapping = {idx : file for idx, file in enumerate(files)}
res = Dummy_model(mapping)
print(res)
# move_all_files(res, base_path=r"D:\games")

# print(mapping)



# if __name__ == "__main__":
#     files = get_recent_files(hours=4)
#     print(files)
#     print("total files are :",len(files))

    