import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"

CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# 2. KNOWLEDGE-BASE FILES
# ============================================================

files = [
    "profile.json",
    "academics.json",
    "skills.json",
    "projects.json",
    "experience.json",
    "certifications.json"
]


# ============================================================
# 3. JSON → SEARCHABLE TEXT
# ============================================================

def json_to_text(data):

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


# ============================================================
# 4. LOAD KNOWLEDGE BASE
# ============================================================

documents = []
metadatas = []

for filename in files:

    file_path = KNOWLEDGE_BASE / filename

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    text = json_to_text(data)

    documents.append(text)

    # Determine category from filename
    document_type = filename.replace(
        ".json",
        ""
    )

    metadatas.append({
        "source": filename,
        "type": document_type
    })


print(
    f"Loaded {len(documents)} knowledge-base files."
)


# ============================================================
# 5. PRINT DOCUMENTS FOR DEBUGGING
# ============================================================

print("\n==============================")
print("KNOWLEDGE BASE DOCUMENTS")
print("==============================")

for i, document in enumerate(documents):

    print(f"\nDocument {i + 1}:")
    print(document)

print("\n==============================\n")


# ============================================================
# 6. LOAD EMBEDDING MODEL
# ============================================================

print(
    "Loading embedding model..."
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ============================================================
# 7. GENERATE EMBEDDINGS
# ============================================================

print(
    "Generating embeddings..."
)

embeddings = model.encode(
    documents,
    convert_to_numpy=True
)


# ============================================================
# 8. CONNECT TO CHROMADB
# ============================================================

print(
    "Connecting to ChromaDB..."
)

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)


# ============================================================
# 9. RECREATE COLLECTION
# ============================================================

collection_name = "portfolio_knowledge"

try:

    client.delete_collection(
        name=collection_name
    )

    print(
        "Existing collection deleted."
    )

except Exception:

    print(
        "No existing collection found."
    )


collection = client.create_collection(
    name=collection_name
)


# ============================================================
# 10. ADD DOCUMENTS TO CHROMADB
# ============================================================

print(
    "Adding documents to ChromaDB..."
)

ids = [
    f"document_{i}"
    for i in range(len(documents))
]


collection.add(

    ids=ids,

    documents=documents,

    embeddings=embeddings.tolist(),

    metadatas=metadatas

)


# ============================================================
# 11. VERIFY COLLECTION
# ============================================================

print()
print(
    f"ChromaDB collection contains "
    f"{collection.count()} documents."
)


# ============================================================
# 12. SHOW STORED DOCUMENTS
# ============================================================

print("\n==============================")
print("CHROMADB VERIFICATION")
print("==============================")

stored = collection.get()

for i, document in enumerate(
    stored["documents"]
):

    print(f"\nDocument {i + 1}:")
    print(document)

print("\n==============================\n")


print(
    "Embedding + ChromaDB pipeline completed successfully!"
)