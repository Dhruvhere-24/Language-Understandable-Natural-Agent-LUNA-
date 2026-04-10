import json

INPUT_FILE = "subjects_v2.json"
OUTPUT_FILE = "subjects_v3.json"

def fix_description(subject_name, description):
    subject_name = subject_name.strip()
    description = description.strip()

    if description.startswith(subject_name + " "):
        return description

    if description.startswith(subject_name):
        remaining = description[len(subject_name):].lstrip()
        return subject_name + " " + remaining

    return subject_name + " " + description


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for subject in data:
        subject["description"] = fix_description(
            subject["subject_name"],
            subject["description"]
        )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Formatting fixed successfully.")


if __name__ == "__main__":
    main()