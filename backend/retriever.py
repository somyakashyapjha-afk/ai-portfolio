import chromadb
from pathlib import Path


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# 2. RETRIEVAL SETTINGS
# ============================================================

# ChromaDB returns a distance value.
# Smaller distance = more similar.
#
# For questions with a detected category, metadata filtering
# has already narrowed the search to a specific portfolio area,
# so we allow a slightly larger distance.
#
# These values are initial thresholds and can be tuned later
# using retrieval tests.

GENERAL_MAX_DISTANCE = 1.35
CATEGORY_MAX_DISTANCE = 1.80


# ============================================================
# 3. CHROMADB
# ============================================================

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="portfolio_knowledge"
)


# ============================================================
# 4. QUESTION CATEGORY DETECTION
# ============================================================

def detect_filter_type(query: str):

    query = query.lower().strip()

    categories = {

        "projects": [
            "project",
            "projects",
            "amazon copilot",
            "gridlock",
            "sustainability",
            "dashboard"
        ],

        "skills": [
            "skill",
            "skills",
            "programming language",
            "technology",
            "technologies",
            "tech stack"
        ],

        "academics": [
            "college",
            "university",
            "degree",
            "cgpa",
            "education",
            "study",
            "academic"
        ],

        "experience": [
            "experience",
            "internship",
            "intern",
            "work experience"
        ],

        "certifications": [
            "certificate",
            "certification",
            "certifications"
        ],

        "profile": [
            "background",
            "about somya",
            "who is somya",
            "profile"
        ]
    }


    for category, keywords in categories.items():

        for keyword in keywords:

            if keyword in query:
                return category


    return None


# ============================================================
# 5. FORMAT DOCUMENT
# ============================================================

def format_document(document, metadata):

    metadata = metadata or {}

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


    formatted = [
        f"SOURCE TYPE: {document_type}",
        f"SOURCE FILE: {source}"
    ]


    if project_name:

        formatted.append(
            f"PROJECT: {project_name}"
        )


    formatted.append(
        f"CONTENT:\n{document}"
    )


    return "\n".join(formatted)


# ============================================================
# 6. EMPTY RESULT HELPER
# ============================================================

def empty_result(filter_type=None):

    return {

        "context": "",

        "filter_type": filter_type,

        "documents": [],

        "distances": [],

        "metadatas": [],

        "sources": []

    }


# ============================================================
# 7. RETRIEVE CONTEXT
# ============================================================

def retrieve_context(
    query: str,
    n_results: int = 2,
    filter_type: str | None = None
):

    query = query.strip()


    # --------------------------------------------------------
    # VALIDATE QUERY
    # --------------------------------------------------------

    if not query:

        return empty_result()


    # --------------------------------------------------------
    # DETECT CATEGORY
    # --------------------------------------------------------

    if filter_type is None:

        filter_type = detect_filter_type(
            query
        )


    # --------------------------------------------------------
    # BUILD CHROMADB QUERY
    # --------------------------------------------------------

    query_args = {

        "query_texts": [query],

        "n_results": n_results,

        "include": [
            "documents",
            "metadatas",
            "distances"
        ]

    }


    # --------------------------------------------------------
    # APPLY METADATA FILTER
    # --------------------------------------------------------

    if filter_type:

        query_args["where"] = {
            "type": filter_type
        }


    # --------------------------------------------------------
    # QUERY CHROMADB
    # --------------------------------------------------------

    results = collection.query(
        **query_args
    )


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
    # NO DOCUMENTS
    # --------------------------------------------------------

    if not documents:

        return empty_result(
            filter_type
        )


    # ========================================================
    # APPLY DISTANCE FILTER
    # ========================================================

    if filter_type:

        max_distance = CATEGORY_MAX_DISTANCE

    else:

        max_distance = GENERAL_MAX_DISTANCE


    filtered_documents = []

    filtered_distances = []

    filtered_metadatas = []


    for document, distance, metadata in zip(
        documents,
        distances,
        metadatas
    ):

        metadata = metadata or {}


        if distance <= max_distance:

            filtered_documents.append(
                document
            )

            filtered_distances.append(
                distance
            )

            filtered_metadatas.append(
                metadata
            )


    # --------------------------------------------------------
    # NO RELEVANT DOCUMENTS
    # --------------------------------------------------------

    if not filtered_documents:

        return empty_result(
            filter_type
        )


    # ========================================================
    # FORMAT CONTEXT
    # ========================================================

    formatted_documents = []


    for document, metadata in zip(
        filtered_documents,
        filtered_metadatas
    ):

        formatted_documents.append(
            format_document(
                document,
                metadata
            )
        )


    context = "\n\n---\n\n".join(
        formatted_documents
    )


    # ========================================================
    # CLEAN SOURCE METADATA
    # ========================================================

    sources = []


    for metadata in filtered_metadatas:

        sources.append({

            "source": metadata.get(
                "source",
                "unknown"
            ),

            "type": metadata.get(
                "type",
                "unknown"
            )

        })


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "context": context,

        "filter_type": filter_type,

        "documents": filtered_documents,

        "distances": filtered_distances,

        "metadatas": filtered_metadatas,

        "sources": sources

    }