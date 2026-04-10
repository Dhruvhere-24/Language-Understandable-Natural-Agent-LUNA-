import json
import re

INPUT_FILE = "subjects.json"
OUTPUT_FILE = "subjects_refined.json"


def clean_text(text, subject_code):
    # Remove evaluation / structural noise
    noise_patterns = [
        r"Periods/week.*",
        r"Continuous Evaluation.*",
        r"Duration of Exam.*",
        r"End Term Examination.*",
        r"End Sem Examination.*",
        r"Course Outcomes.*",
        r"Pre-Requisite.*",
        r"Course Type.*",
        r"NOTE:.*",
        r"List of Practicals:?", # <- why this ye tho lab seen hai
        r"PART\s*[-–]?\s*[A-Z]?",
        r"Unit[-\s]?\d+.*", # <- 🤔
    ]

    for pattern in noise_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    # Remove subject code references like BCS-DS-611.1
    text = re.sub(rf"{subject_code}\.\d+", "", text)

    # Remove numbering like 1.1 , 2.3.4
    text = re.sub(r"\b\d+(\.\d+)*\b", "", text)

    # Remove URLs
    text = re.sub(r"http\S+", "", text)

    # Remove extra punctuation
    text = re.sub(r"[^\w\s,]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def compress_keywords(text):
    # Split into phrases
    parts = [p.strip() for p in text.split(",")]

    # Remove very short fragments
    parts = [p for p in parts if len(p.split()) > 2]

    # Remove duplicates
    parts = list(dict.fromkeys(parts))

    # Join back
    return ", ".join(parts[:80]) # <- why not full list koi dikat hai kya


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for subject in data:
        code = subject["subject_code"]

        # Clean raw
        subject["raw_description"] = clean_text(
            subject["raw_description"], code
        )

        # Clean semantic
        cleaned = clean_text(
            subject["clean_semantic_description"], code
        )

        subject["clean_semantic_description"] = compress_keywords(cleaned)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Refined JSON generated successfully!")


if __name__ == "__main__":
    main()