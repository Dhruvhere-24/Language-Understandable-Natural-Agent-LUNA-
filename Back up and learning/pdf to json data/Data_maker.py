import pdfplumber
import re
import json

PDF_PATH = "syllabus.pdf"
OUTPUT_JSON = "subjects_final.json"
BRANCH = "CSE"
SEMESTER = 6


def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += "\n" + page_text
    return text


def split_subjects(full_text):
    pattern = r"\n([A-Z]{2,}-[A-Z]{2,}-\d{3}:[^\n]+)"
    matches = list(re.finditer(pattern, full_text))

    subjects = []

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        subjects.append(full_text[start:end])

    return subjects


def remove_noise(text):
    noise_patterns = [
        r"Distribution of Continuous Evaluation:.*",
        r"COURSE ARTICULATION MATRIX.*",
        r"Evaluation Tools:.*",
        r"Instructions for paper setting:.*",
        r"Text Books.*",
        r"Software required.*",
        r"Attendance.*",
        r"Batch \d{4}-\d{2}",
        r"Page \d+"
    ]

    for pattern in noise_patterns:
        text = re.sub(pattern, "", text, flags=re.DOTALL | re.IGNORECASE)

    return text


def extract_clean_keywords(text):
    lines = text.split("\n")
    keywords = []

    for line in lines:
        line = line.strip()

        # Remove numbering like 1.1 , 2.3.4
        line = re.sub(r"^\d+(\.\d+)*\s*", "", line)

        # Skip very short lines
        if len(line) < 5:
            continue

        # Skip subject code lines
        if re.match(r"[A-Z]{2,}-[A-Z]{2,}-\d{3}", line):
            continue

        # Keep important lines
        if (
            line.startswith("Unit")
            or "Course Outcomes" in line
            or "List of Practicals" in line
            or len(line.split()) > 4
        ):
            keywords.append(line)

    # Join and compress
    clean_text = ", ".join(keywords[:80])

    return clean_text


def process_subject(block):
    header_match = re.search(r"([A-Z]{2,}-[A-Z]{2,}-\d{3}):\s*(.+)", block)
    if not header_match:
        return None

    subject_code = header_match.group(1).strip()
    subject_name = header_match.group(2).strip()

    cleaned_block = remove_noise(block)
    clean_semantic = extract_clean_keywords(cleaned_block)

    return {
        "subject_code": subject_code,
        "subject_name": subject_name,
        "branch": BRANCH,
        "semester": SEMESTER,
        "raw_description": cleaned_block.strip(),
        "clean_semantic_description": clean_semantic.strip()
    }


def main():
    full_text = extract_text(PDF_PATH)
    subject_blocks = split_subjects(full_text)

    subjects = []

    for block in subject_blocks:
        subject_data = process_subject(block)
        if subject_data:
            subjects.append(subject_data)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(subjects, f, indent=4)

    print(f"Successfully generated {len(subjects)} subjects.")


if __name__ == "__main__":
    main()