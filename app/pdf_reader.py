import pymupdf


def extract_text_from_pdf(pdf_path):
    document = pymupdf.open(pdf_path)
    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_pages_from_pdf(pdf_path):
    """Extract text from a PDF while preserving page numbers."""
    document = pymupdf.open(pdf_path)
    pages = []

    for page_number, page in enumerate(document, start=1):
        pages.append({
            "page": page_number,
            "text": page.get_text()
        })

    document.close()

    return pages

if __name__ == "__main__":
    pdf_text = extract_text_from_pdf("data/sample.pdf")
    print(pdf_text[:2000])


