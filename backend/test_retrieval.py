from retriever import retrieve_context, detect_filter_type


queries = [
    "Tell me about Amazon Copilot",
    "What programming languages does Somya know?",
    "Where does Somya study?",
    "Tell me about Somya's background",
    "What experience does Somya have?",
    "What certifications does Somya have?"
]


for question in queries:

    detected_type = detect_filter_type(question)

    print("\n" + "=" * 60)
    print("QUESTION:", question)
    print("DETECTED TYPE:", detected_type)
    print("=" * 60)

    result = retrieve_context(
        question,
        n_results=2
    )

    print(result)