import os
import sys

# Allow the test file to import modules from the app folder
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "app"
        )
    )
)

from table_reader import (
    extract_property_rows_from_text,
    structure_property_rows,
    find_rent_extreme,
    extract_dashboard_metrics
)


PDF_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "sample.pdf"
    )
)


def test_dashboard_metrics():
    """Check that dashboard statistics are extracted correctly."""

    metrics = extract_dashboard_metrics(PDF_PATH)

    assert metrics["students"] == 9
    assert metrics["properties"] == 50
    assert metrics["appointments"] == 8
    assert metrics["landlords"] == 50


def test_highest_rent_property():
    """Check that the highest-rent property is identified correctly."""

    rows = extract_property_rows_from_text(PDF_PATH)
    properties = structure_property_rows(rows)

    highest = find_rent_extreme(
        properties,
        "highest"
    )

    assert highest["id"] == "R04342"
    assert highest["address"] == "3 Egremont Road"
    assert highest["rent"] == "£40.00"


def test_lowest_rent_property():
    """Check that the lowest-rent property is identified correctly."""

    rows = extract_property_rows_from_text(PDF_PATH)
    properties = structure_property_rows(rows)

    lowest = find_rent_extreme(
        properties,
        "lowest"
    )

    assert lowest["id"] == "T04101"
    assert lowest["address"] == "12 Fenton Street"
    assert lowest["rent"] == "£35.00"