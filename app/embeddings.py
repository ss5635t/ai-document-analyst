from sentence_transformers import SentenceTransformer


def create_embeddings(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(chunks)

    return embeddings


if __name__ == "__main__":
    from pdf_reader import extract_text_from_pdf
    from text_chunker import chunk_text

    text = extract_text_from_pdf("data/sample.pdf")
    chunks = chunk_text(text)

    embeddings = create_embeddings(chunks)

    print(f"Number of chunks: {len(chunks)}")
    print(f"Embedding shape: {embeddings.shape}")
    print("\nFirst 10 numbers of the first embedding:")
    print(embeddings[0][:10])