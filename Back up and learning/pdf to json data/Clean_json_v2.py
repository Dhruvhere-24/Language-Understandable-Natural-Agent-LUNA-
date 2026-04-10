import json

INPUT_FILE = "subjects_refined.json"
OUTPUT_FILE = "subjects_v2.json"

def clean_description(text):
    # Remove common leftover noise words
    noise_words = ["BCS DS", "CSE", "L T P", " L T ", " P "]
    for word in noise_words:
        text = text.replace(word, "")

    # Remove extra spaces
    text = " ".join(text.split())

    return text.strip()


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    unique = {}

    for subject in data:
        code = subject["subject_code"]

        if code not in unique:
            subject["description"] = clean_description(subject["raw_description"])
            del subject["raw_description"]
            del subject["clean_semantic_description"]
            unique[code] = subject

    final_data = list(unique.values())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4)

    print("Final cleaned file generated.")


if __name__ == "__main__":
    main()