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
def detect_filter_type(query):

    query = query.lower()

    if any(word in query for word in [
        "project",
        "amazon copilot",
        "gridlock",
        "sustainability",
        "dashboard",
        "portfolio"
    ]):
        return "project"

    if any(word in query for word in [
        "skill",
        "skills",
        "programming language",
        "technology",
        "technologies",
        "know"
    ]):
        return "skills"

    if any(word in query for word in [
        "college",
        "university",
        "degree",
        "cgpa",
        "education",
        "study"
    ]):
        return "academics"

    if any(word in query for word in [
        "experience",
        "internship",
        "work"
    ]):
        return "experience"

    if any(word in query for word in [
        "certificate",
        "certification"
    ]):
        return "certifications"

    if any(word in query for word in [
        "background",
        "about somya",
        "who is somya",
        "profile"
    ]):
        return "profile"

    return None


def retrieve_context(query, n_results=2, filter_type=None):

    if filter_type is None:
        filter_type = detect_filter_type(query)

    query_args = {
        "query_texts": [query],
        "n_results": n_results
    }

    if filter_type:
        query_args["where"] = {
            "type": filter_type
        }

    results = collection.query(**query_args)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return {
            "context": "No relevant portfolio information was found.",
            "filter_type": filter_type,
            "sources": []
        }

    context = "\n\n".join(documents)

    return {
        "context": context,
        "filter_type": filter_type,
        "sources": metadatas
    }