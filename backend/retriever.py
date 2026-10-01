import chromadb
from pathlib import Path


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# 2. CHROMADB
# ============================================================

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="portfolio_knowledge"
)


# ============================================================
# 3. CHROMA DEBUG
# ============================================================

print("\n==============================")
print("CHROMA DEBUG")
print("Chroma DB path:", CHROMA_DIR)
print("Collection:", collection.name)
print("Number of documents:", collection.count())

sample = collection.get(
    limit=10,
    include=["metadatas", "documents"]
)

print("\nMETADATA IN CHROMADB:")
print(sample["metadatas"])

print("\nDOCUMENTS IN CHROMADB:")
print(sample["documents"])

print("==============================\n")


# ============================================================
# 4. DETECT QUESTION CATEGORY
# ============================================================

def detect_filter_type(query):

    query = query.lower()


    # ---------------- PROJECTS ----------------

    if any(word in query for word in [
        "project",
        "projects",
        "amazon copilot",
        "gridlock",
        "sustainability",
        "dashboard"
    ]):
        return "projects"


    # ---------------- SKILLS ----------------

    if any(word in query for word in [
        "skill",
        "skills",
        "programming language",
        "technology",
        "technologies",
        "tech stack"
    ]):
        return "skills"


    # ---------------- ACADEMICS ----------------

    if any(word in query for word in [
        "college",
        "university",
        "degree",
        "cgpa",
        "education",
        "study",
        "academic"
    ]):
        return "academics"


    # ---------------- EXPERIENCE ----------------

    if any(word in query for word in [
        "experience",
        "internship",
        "intern",
        "work"
    ]):
        return "experience"


    # ---------------- CERTIFICATIONS ----------------

    if any(word in query for word in [
        "certificate",
        "certification",
        "certifications"
    ]):
        return "certifications"


    # ---------------- PROFILE ----------------

    if any(word in query for word in [
        "background",
        "about somya",
        "who is somya",
        "profile"
    ]):
        return "profile"


    # ---------------- NO FILTER ----------------

    return None


# ============================================================
# 5. FORMAT DOCUMENT
# ============================================================

def format_document(document, metadata):

    document_type = metadata.get(
        "type",
        "unknown"
    )

    source = metadata.get(
        "source",
        "unknown"
    )

    project_name = metadata.get(
        "project_name"
    )

    formatted = f"""
SOURCE TYPE: {document_type}
SOURCE FILE: {source}
"""


    if project_name:

        formatted += f"""
PROJECT: {project_name}
"""


    formatted += f"""
CONTENT:
{document}
"""


    return formatted.strip()


# ============================================================
# 6. RETRIEVE CONTEXT
# ============================================================

def retrieve_context(
    query,
    n_results=2,
    filter_type=None
):

    # --------------------------------------------------------
    # Detect category automatically
    # --------------------------------------------------------

    if filter_type is None:

        filter_type = detect_filter_type(
            query
        )


    # --------------------------------------------------------
    # Build ChromaDB query
    # --------------------------------------------------------

    query_args = {

        "query_texts": [query],

        "n_results": n_results

    }


    # --------------------------------------------------------
    # Apply metadata filter
    # --------------------------------------------------------

    if filter_type:

        query_args["where"] = {

            "type": filter_type

        }


    # --------------------------------------------------------
    # Query ChromaDB
    # --------------------------------------------------------

    results = collection.query(
        **query_args
    )


    # --------------------------------------------------------
    # Extract results
    # --------------------------------------------------------

    documents = results.get(
        "documents",
        [[]]
    )[0]


    distances = results.get(
        "distances",
        [[]]
    )[0]


    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]


    # --------------------------------------------------------
    # No results
    # --------------------------------------------------------

    if not documents:

        return {

            "context":
                "No relevant portfolio information was found.",

            "filter_type":
                filter_type,

            "documents": [],

            "distances": [],

            "metadatas": [],

            "sources": []

        }


    # ========================================================
    # DAY 13 — FORMAT RETRIEVED DOCUMENTS
    # ========================================================

    formatted_documents = []


    for document, metadata in zip(
        documents,
        metadatas
    ):

        formatted_document = format_document(
            document,
            metadata
        )

        formatted_documents.append(
            formatted_document
        )


    # ========================================================
    # COMBINE FORMATTED DOCUMENTS
    # ========================================================

    context = "\n\n---\n\n".join(
        formatted_documents
    )


    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {

        "context":
            context,

        "filter_type":
            filter_type,

        "documents":
            documents,

        "distances":
            distances,

        "metadatas":
            metadatas,

        "sources":
            metadatas

    }