import ollama

from pdf_reader import extract_pages_from_pdf
from text_chunker import chunk_pages
from retriever import find_relevant_chunks
from table_reader import (
    extract_property_rows_from_text,
    structure_property_rows,
    find_rent_extreme,
    extract_dashboard_metrics
)


def generate_answer(question, context):
    """Generate an answer using the local Ollama language model."""

    prompt = f"""
You are an AI document assistant.

Answer the question using ONLY the context provided below.

Rules:
1. Answer using ONLY information explicitly stated in the context.
2. Do not use outside knowledge.
3. Do not guess, infer, or invent details that are not supported by the context.
4. Prefer the document's own names, titles, labels, and terminology.
5. Use verified calculation results when they are provided.
6. When answering a question about a property, include the property ID,
   address, and rent when these details are available.
7. If the question asks what the document is about, identify the document
   using its title, headings, and clearly stated content.
8. Before saying that the answer cannot be found, check the entire context
   carefully for an explicit name, title, organisation, university, person,
   date, number, or other fact that directly answers the question.
9. If the answer cannot be determined from the context, say:
   "I cannot find the answer in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def answer_question(question, pdf_path):
    """Route a question through structured analysis or semantic RAG."""

    question_lower = question.lower()

    # Extract structured property information
    property_rows = extract_property_rows_from_text(pdf_path)
    properties = structure_property_rows(property_rows)

    # Extract structured dashboard information
    dashboard_metrics = extract_dashboard_metrics(pdf_path)

    metric_keywords = {
        "students": ["student", "students"],
        "properties": ["property", "properties"],
        "appointments": ["appointment", "appointments"],
        "landlords": ["landlord", "landlords"]
    }

    # Recognise different ways of asking for a count
    count_phrases = [
        "how many",
        "number of",
        "total number of",
        "count of",
        "total"
    ]

    # Route dashboard-count questions through Python
    for metric, keywords in metric_keywords.items():
        asks_for_count = any(
            phrase in question_lower
            for phrase in count_phrases
        )

        mentions_metric = any(
            keyword in question_lower
            for keyword in keywords
        )

        if (
            asks_for_count
            and mentions_metric
            and metric in dashboard_metrics
        ):
            value = dashboard_metrics[metric]

            context = (
                "Verified dashboard metric.\n\n"
                f"{metric.title()}: {value}"
            )

            return {
                "answer": f"There are {value} {metric} shown in the dashboard.",
                "evidence": context,
                "method": "Structured Python analysis"
            }

    # Route highest-rent questions through Python
    if (
        properties
        and "highest" in question_lower
        and "rent" in question_lower
    ):
        property_result = find_rent_extreme(
            properties,
            "highest"
        )

        context = (
            "Verified calculation: this property has the highest rent.\n\n"
            f"ID: {property_result['id']}\n"
            f"Address: {property_result['address']}\n"
            f"Type: {property_result['type']}\n"
            f"Rent: {property_result['rent']}\n"
            f"Distance: {property_result['distance']}"
        )

        answer = generate_answer(
            question,
            context
        )

        return {
            "answer": answer,
            "evidence": context,
            "method": "Structured Python analysis"
        }

    # Route lowest-rent questions through Python
    if (
        properties
        and "lowest" in question_lower
        and "rent" in question_lower
    ):
        property_result = find_rent_extreme(
            properties,
            "lowest"
        )

        context = (
            "Verified calculation: this property has the lowest rent.\n\n"
            f"ID: {property_result['id']}\n"
            f"Address: {property_result['address']}\n"
            f"Type: {property_result['type']}\n"
            f"Rent: {property_result['rent']}\n"
            f"Distance: {property_result['distance']}"
        )

        answer = generate_answer(
            question,
            context
        )

        return {
            "answer": answer,
            "evidence": context,
            "method": "Structured Python analysis"
        }

    # Use page-aware semantic RAG for normal document questions
    pages = extract_pages_from_pdf(pdf_path)
    chunks = chunk_pages(pages)

    results = find_relevant_chunks(
        question,
        chunks,
        top_k=2
    )

    context = "\n\n".join(
        result["chunk"]
        for result in results
    )

    answer = generate_answer(
        question,
        context
    )

    return {
        "answer": answer,
        "evidence": [
            {
                "page": result["page"],
                "text": result["chunk"],
                "score": float(result["score"])
            }
            for result in results
        ],
        "method": "Semantic retrieval (RAG)"
    }

