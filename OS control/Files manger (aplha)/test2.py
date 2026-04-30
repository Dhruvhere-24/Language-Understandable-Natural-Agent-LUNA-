import os
import shutil
from datetime import datetime, timedelta
from typing import List, Dict
import numpy as np
import vector_model as vm

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

    logs = []

    for path, val in file_paths.items():

        if path == "None" or val[0] == "None" or val[1] == "None":
            logs.append("⚠️ No valid files to move")
            continue

        file_name = path
        drop_path = os.path.join(base_path, str(val[1]))
        os.makedirs(drop_path, exist_ok=True)

        destination = os.path.join(drop_path, os.path.basename(file_name))

        if os.path.exists(destination):
            logs.append(f"⚠️ Already exists → {destination}")
            continue

        try:
            shutil.move(file_name, destination)
            logs.append(f"✅ Moved → {destination}")
        except Exception as e:
            logs.append(f"❌ Failed → {file_name} | {e}")

    return logs

def model_check(paths: Dict[int, str]) -> Dict[str, List[str]] :
    res = dict()
    if not paths:
        return {"None": ["None", "None"]}
        
    code2name = vm.load_code_name_mapping("subjects_Final.json")

    for key, val in paths.items():
        
        path = val # model ke leye path
        subject_code, _ = vm.predict_subject(path)
        
        subject_name = code2name.get(subject_code, "None")

        if subject_code == "None" or subject_name == "None":
            continue

        if path not in res:
            res[path] = []

        # append List
        res[path].extend([subject_code, subject_name])


    return res

if __name__ == "__main__":
    files = get_recent_files(5)
    mapping = {idx : file for idx, file in enumerate(files)}
    res = model_check(mapping) # empty ke leye mode ki output {"None" : ["None", "None"]}

    ## testing dict
    # res = {'C:\\Users\\DHRUV\\Downloads\\testing.pdf': [np.str_('BCS-DS-613'), 'Emerging Computing Technologies'], 'C:\\Users\\DHRUV\\Downloads\\testing 2.docx': [np.str_('BHM-MC-009'), 'QUANTITATIVE APTITUDE AND PERSONALITY DEVELOPMENT-III'], 'C:\\Users\\DHRUV\\Downloads\\testing.docx': [np.str_('BHM-MC-009'), 'QUANTITATIVE APTITUDE AND PERSONALITY DEVELOPMENT-III'], 'C:\\Users\\DHRUV\\Downloads\\testing.pptx': [np.str_('BCS-DS-851'), 'Reinforcement Learning Lab']}
    
    print(res)
    info = move_all_files(res, base_path=r"D:\games\AI File_manager")
    print(info)

    