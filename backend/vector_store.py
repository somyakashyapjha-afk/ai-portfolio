import json
from pathlib import Path

import chromadb


# -----------------------------------
# 1. Paths
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent

KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"

CHROMA_DIR = BASE_DIR / "chroma_db"


# -----------------------------------
# 2. ChromaDB
# -----------------------------------

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

# -----------------------------------
# 2. Create a fresh collection
# -----------------------------------

try:
    client.delete_collection(
        name="portfolio_knowledge"
    )
    print("Old collection deleted.")
except Exception:
    pass


collection = client.create_collection(
    name="portfolio_knowledge"
)


# -----------------------------------
# 3. JSON → readable text
# -----------------------------------

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


# -----------------------------------
# 4. Create knowledge chunks
# -----------------------------------

documents = []
metadatas = []
ids = []


# ---------- Profile ----------

profile_path = KNOWLEDGE_BASE / "profile.json"

with open(profile_path, "r", encoding="utf-8") as file:

    profile = json.load(file)

documents.append(
    json_to_text(profile)
)

metadatas.append({
    "source": "profile.json",
    "type": "profile"
})

ids.append("profile_1")


# ---------- Academics ----------

academics_path = KNOWLEDGE_BASE / "academics.json"

with open(academics_path, "r", encoding="utf-8") as file:

    academics = json.load(file)

documents.append(
    json_to_text(academics)
)

metadatas.append({
    "source": "academics.json",
    "type": "academics"
})

ids.append("academics_1")


# ---------- Skills ----------

skills_path = KNOWLEDGE_BASE / "skills.json"

with open(skills_path, "r", encoding="utf-8") as file:

    skills = json.load(file)

documents.append(
    json_to_text(skills)
)

metadatas.append({
    "source": "skills.json",
    "type": "skills"
})

ids.append("skills_1")


# ---------- Projects ----------

projects_path = KNOWLEDGE_BASE / "projects.json"

with open(projects_path, "r", encoding="utf-8") as file:

    projects_data = json.load(file)


for index, project in enumerate(
    projects_data["projects"]
):

    project_text = json_to_text(project)

    documents.append(project_text)

    metadatas.append({
        "source": "projects.json",
        "type": "project",
        "project_name": project["name"]
    })

    ids.append(
        f"project_{index + 1}"
    )


# ---------- Experience ----------

experience_path = KNOWLEDGE_BASE / "experience.json"

with open(experience_path, "r", encoding="utf-8") as file:

    experience = json.load(file)

documents.append(
    json_to_text(experience)
)

metadatas.append({
    "source": "experience.json",
    "type": "experience"
})

ids.append("experience_1")


# ---------- Certifications ----------

certifications_path = (
    KNOWLEDGE_BASE / "certifications.json"
)

with open(
    certifications_path,
    "r",
    encoding="utf-8"
) as file:

    certifications = json.load(file)

documents.append(
    json_to_text(certifications)
)

metadatas.append({
    "source": "certifications.json",
    "type": "certifications"
})

ids.append("certifications_1")


# -----------------------------------
# 5. Insert into ChromaDB
# -----------------------------------

collection.upsert(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)


# -----------------------------------
# 6. Verify
# -----------------------------------

print("Knowledge ingestion completed!")

print(
    f"Documents stored: {collection.count()}"
)

print("\nStored knowledge:")

for metadata in metadatas:

    print(
        "-",
        metadata
    )