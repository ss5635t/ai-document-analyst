def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def chunk_pages(pages, chunk_size=1000, overlap=200):
    """Create text chunks while preserving their page numbers."""
    chunks = []

    for page_data in pages:
        page_number = page_data["page"]
        text = page_data["text"]
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]

            chunks.append({
                "page": page_number,
                "text": chunk
            })

            start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    from pdf_reader import extract_text_from_pdf

    text = extract_text_from_pdf("data/sample.pdf")
    chunks = chunk_text(text)

    print(f"Total characters: {len(text)}")
    print(f"Number of chunks: {len(chunks)}")

    print("\n--- CHUNK 1 ---")
    print(chunks[0])

    print("\n--- CHUNK 2 ---")
    print(chunks[1])

