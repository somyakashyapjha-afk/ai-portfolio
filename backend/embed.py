import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
import numpy as np


# -----------------------------------
# 1. Paths
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"

OUTPUT_DIR = BASE_DIR / "embeddings"
OUTPUT_DIR.mkdir(exist_ok=True)


# -----------------------------------
# 2. Knowledge-base files
# -----------------------------------

files = [
    "profile.json",
    "academics.json",
    "skills.json",
    "projects.json",
    "experience.json",
    "certifications.json"
]


# -----------------------------------
# 3. Load JSON data
# -----------------------------------

documents = []

for filename in files:

    file_path = KNOWLEDGE_BASE / filename

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    documents.append({
        "source": filename,
        "content": data
    })


print(f"Loaded {len(documents)} knowledge-base files.")


# -----------------------------------
# 4. Convert JSON → searchable text
# -----------------------------------

def json_to_text(data):
    """
    Recursively converts structured JSON
    into readable text.
    """

    if isinstance(data, dict):

        parts = []

        for key, value in data.items():

            readable_key = key.replace("_", " ")

            parts.append(
                f"{readable_key}: {json_to_text(value)}"
            )

        return ". ".join(parts)

    elif isinstance(data, list):

        return ", ".join(
            json_to_text(item)
            for item in data
        )

    else:

        return str(data)


texts = []

metadata = []


for document in documents:

    text = json_to_text(document["content"])

    texts.append(text)

    metadata.append({
        "source": document["source"]
    })


# -----------------------------------
# 5. Load embedding model
# -----------------------------------

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -----------------------------------
# 6. Generate embeddings
# -----------------------------------

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True
)


# -----------------------------------
# 7. Save embeddings
# -----------------------------------

embedding_path = OUTPUT_DIR / "embeddings.npy"

np.save(
    embedding_path,
    embeddings
)


# -----------------------------------
# 8. Save metadata
# -----------------------------------

metadata_path = OUTPUT_DIR / "metadata.json"

with open(
    metadata_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        metadata,
        file,
        indent=2
    )


# -----------------------------------
# 9. Finished
# -----------------------------------

print()
print("Embedding pipeline completed successfully!")
print(f"Embeddings shape: {embeddings.shape}")
print(f"Saved to: {embedding_path}")
print(f"Metadata saved to: {metadata_path}")