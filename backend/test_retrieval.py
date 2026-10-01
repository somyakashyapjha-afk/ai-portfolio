from retriever import retrieve_context


# ============================================================
# DAY 19 — RETRIEVAL QUALITY TEST
# ============================================================

test_questions = [
    "What are Somya's technical skills?",
    "Tell me about Amazon Copilot",
    "What experience does Somya have?",
    "Tell me about her education",
    "What is Somya's favorite food?",
    "Explain quantum mechanics",
]


print("\n==============================")
print("DAY 19 — RETRIEVAL TEST")
print("==============================")


for question in test_questions:

    result = retrieve_context(
        question,
        n_results=2
    )

    print("\nQUESTION:")
    print(question)

    print("\nFILTER:")
    print(result["filter_type"])

    print("\nDISTANCES:")
    print(result["distances"])

    print("\nSOURCES:")
    print(result["sources"])

    print("\nCONTEXT FOUND:")
    print("YES" if result["context"] else "NO")

    print("\n------------------------------")


print("\n==============================")
print("TEST COMPLETED")
print("==============================")