from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def find_relevant_chunks(question, chunks, top_k=2):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Support both normal text chunks and page-aware chunks
    chunk_texts = [
        chunk["text"] if isinstance(chunk, dict) else chunk
        for chunk in chunks
    ]

    chunk_embeddings = model.encode(chunk_texts)
    question_embedding = model.encode([question])

    similarities = cosine_similarity(
        question_embedding,
        chunk_embeddings
    )[0]

    ranked_indices = similarities.argsort()[::-1]

    results = []

    for index in ranked_indices[:top_k]:
        chunk = chunks[index]

        if isinstance(chunk, dict):
            results.append({
                "chunk": chunk["text"],
                "page": chunk["page"],
                "score": similarities[index]
            })
        else:
            results.append({
                "chunk": chunk,
                "page": None,
                "score": similarities[index]
            })

    return results


if __name__ == "__main__":
    from pdf_reader import extract_pages_from_pdf
    from text_chunker import chunk_pages

    pages = extract_pages_from_pdf("data/sample.pdf")
    chunks = chunk_pages(pages)

    question = "Which accommodation has the lowest rent?"

    results = find_relevant_chunks(question, chunks)

    print(f"\nQuestion: {question}")

    for number, result in enumerate(results, start=1):
        print(f"\n--- RESULT {number} ---")
        print(f"Page: {result['page']}")
        print(f"Similarity score: {result['score']:.4f}")
        print(result["chunk"])

