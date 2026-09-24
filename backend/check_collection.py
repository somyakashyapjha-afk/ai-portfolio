import chromadb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="portfolio_knowledge"
)

print("Collection:", collection.name)
print("Documents:", collection.count())

data = collection.get()

print("\nStored Metadata:")

for id_, metadata in zip(
    data["ids"],
    data["metadatas"]
):
    print("--------------------")
    print("ID:", id_)
    print("Metadata:", metadata)