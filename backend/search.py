import chromadb


# -----------------------------------
# 1. Connect to existing ChromaDB
# -----------------------------------

client = chromadb.PersistentClient(
    path="backend/chroma_db"
)


# -----------------------------------
# 2. Get our collection
# -----------------------------------

collection = client.get_collection(
    name="portfolio_knowledge"
)


# -----------------------------------
# 3. Test semantic search
# -----------------------------------

query = "Tell me about Somya's Amazon Copilot project."


results = collection.query(
    query_texts=[query],
    n_results=3
)


# -----------------------------------
# 4. Display results
# -----------------------------------

print("\nQUERY:")
print(query)

print("\nRETRIEVED SOURCES:")

for source in results["metadatas"][0]:

    print("-", source["source"])


print("\nRETRIEVED CONTENT:")

for document in results["documents"][0]:

    print("\n---")
    print(document)
