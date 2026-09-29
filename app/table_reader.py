import pymupdf
import re


def extract_property_rows_from_text(pdf_path):
    """Extract property records from the text of a PDF."""
    document = pymupdf.open(pdf_path)
    property_rows = []

    pattern = re.compile(
        r"^([A-Z]\d+)\s*$\n"
        r"^(.+?)\s*$\n"
        r"^(Room|House)\s*$\n"
        r"^(£[\d.]+)\s*$\n"
        r"^([\d.]+mi)\s*$",
        re.MULTILINE
    )

    for page in document:
        page_text = page.get_text()
        matches = pattern.findall(page_text)

        for match in matches:
            property_row = " ".join(match)

            if property_row not in property_rows:
                property_rows.append(property_row)

    document.close()

    return property_rows


def structure_property_rows(property_rows):
    """Convert extracted property rows into structured dictionaries."""
    structured_properties = []

    pattern = (
        r"^(\w+)\s+(.+?)\s+(Room|House)"
        r"\s+(£[\d.]+)\s+([\d.]+mi)$"
    )

    for row in property_rows:
        match = re.match(pattern, row)

        if match:
            property_record = {
                "id": match.group(1),
                "address": match.group(2),
                "type": match.group(3),
                "rent": match.group(4),
                "distance": match.group(5)
            }

            structured_properties.append(property_record)

    return structured_properties


def find_rent_extreme(properties, mode="highest"):
    """Return the property with the highest or lowest rent."""
    if mode == "highest":
        return max(
            properties,
            key=lambda item: float(
                item["rent"].replace("£", "")
            )
        )

    if mode == "lowest":
        return min(
            properties,
            key=lambda item: float(
                item["rent"].replace("£", "")
            )
        )

    raise ValueError("Mode must be 'highest' or 'lowest'.")


def extract_dashboard_metrics(pdf_path):
    """Extract overview statistics from the dashboard."""
    document = pymupdf.open(pdf_path)

    full_text = ""

    for page in document:
        full_text += page.get_text()

    document.close()

    metrics = {}

    pattern = re.compile(
        r"Overview\s+"
        r"(\d+)\s+.*?Students\s+"
        r"(\d+)\s+.*?Properties\s+"
        r"(\d+)\s+.*?Appointments\s+"
        r"(\d+)\s+.*?Landlords",
        re.IGNORECASE | re.DOTALL
    )

    match = pattern.search(full_text)

    if match:
        metrics = {
            "students": int(match.group(1)),
            "properties": int(match.group(2)),
            "appointments": int(match.group(3)),
            "landlords": int(match.group(4))
        }

    return metrics


if __name__ == "__main__":
    rows = extract_property_rows_from_text("data/sample.pdf")
    properties = structure_property_rows(rows)

    print("\n--- STRUCTURED PROPERTIES ---")

    for property_record in properties:
        print(property_record)

    highest_property = find_rent_extreme(properties, "highest")
    lowest_property = find_rent_extreme(properties, "lowest")

    print("\n--- HIGHEST RENT PROPERTY ---")
    print(highest_property)

    print("\n--- LOWEST RENT PROPERTY ---")
    print(lowest_property)

    dashboard_metrics = extract_dashboard_metrics("data/sample.pdf")

    print("\n--- DASHBOARD METRICS ---")
    print(dashboard_metrics)


    

