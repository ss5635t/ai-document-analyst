import os
import tempfile

import streamlit as st

from rag import answer_question


st.set_page_config(
    page_title="AI Document Analyst",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Document Analyst")

st.write(
    "Upload a PDF document and ask questions about its contents."
)

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

question = st.text_input(
    "Ask a question about your document"
)

ask_button = st.button(
    "Ask Question",
    type="primary"
)

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

if uploaded_file is not None and question and ask_button:
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temporary_file:
        temporary_file.write(uploaded_file.getvalue())
        pdf_path = temporary_file.name

    try:
        with st.spinner("Analysing document..."):
            result = answer_question(
                question,
                pdf_path
            )

        st.subheader("Answer")
        st.write(result["answer"])

        st.caption(
            f"Analysis method: {result['method']}"
        )

        with st.expander("View retrieved evidence"):
            evidence = result["evidence"]

            if isinstance(evidence, list):
                for number, source in enumerate(evidence, start=1):
                    st.markdown(
                        f"**Source {number} — Page {source['page']}**"
                    )

                    st.caption(
                        f"Similarity score: {source['score']:.4f}"
                    )

                    st.text(source["text"])

                    if number < len(evidence):
                        st.divider()

            else:
                st.text(evidence)

    except Exception as error:
        st.error(
            "Something went wrong while analysing the document."
        )
        st.exception(error)

    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
