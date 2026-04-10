import json

INPUT_FILE = "subjects_v3.json"
OUTPUT_FILE = "subjects_v4.json"

def normalize_description(subject):
    name = subject["subject_name"]
    desc = subject["description"]

    # Remove code-like prefixes
    prefixes = ["PROJ CS", "BHM MC", "BCS DS"]
    for p in prefixes:
        desc = desc.replace(p, "")

    # Remove accidental duplicate subject name
    if desc.startswith(name + " " + name):
        desc = name + desc[len(name)*2 + 1:]

    # Remove extra spaces
    desc = " ".join(desc.split())

    subject["description"] = desc.strip()
    return subject


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    unique_subjects = {}

    for subject in data:
        code = subject["subject_code"]

        # Deduplicate by subject_code
        if code not in unique_subjects:
            subject = normalize_description(subject)
            unique_subjects[code] = subject

    final_data = list(unique_subjects.values())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4)

    print("✅ Final cleaned JSON generated successfully!")


if __name__ == "__main__":
    main()