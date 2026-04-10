import json
import numpy as np
from sentence_transformers import SentenceTransformer

# INPUT_FILE = "subjects_final.json" # <- I dont want to run again 😂😂
EMBEDDING_FILE = "subject_embeddings.npz"

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load subjects
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    subjects = json.load(f)

texts = []
codes = []

for subject in subjects:
    text = subject["subject_name"] + ". " + subject["description"]
    texts.append(text)
    codes.append(subject["subject_code"])

# Generate embeddings
embeddings = model.encode(texts, normalize_embeddings=True)

# Save embeddings
np.savez(EMBEDDING_FILE, embeddings=embeddings, codes=codes)

print("✅ Subject embeddings generated successfully.")


'''
BertModel LOAD REPORT from: sentence-transformers/all-MiniLM-L6-v2
Key                     | Status     |  |
------------------------+------------+--+-
embeddings.position_ids | UNEXPECTED |  |

Notes:
- UNEXPECTED    :can be ignored when loading from different task/architecture; not ok if you expect identical arch.

👉 Yes, ignore it.
👉 Your embedding file is fine.
👉 System is working.
'''