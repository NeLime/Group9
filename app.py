import streamlit as st
import pandas as pd
from interpreter import run_all

st.set_page_config(page_title="R-like Interpreter", layout="wide")
st.title("Lexical Analyzer Development R-like Scripting")

# Upload file (optional)
uploaded = st.file_uploader(
    "Upload file .r / .txt",
    type=["r", "txt"]
)

# Init session state
if "code" not in st.session_state:
    st.session_state.code = ""

# Jika upload file, isi editor dengan isi file
if uploaded is not None:
    st.session_state.code = uploaded.read().decode("utf-8", errors="replace")
    st.success(f"File berhasil di-load: {uploaded.name}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Code")
    code = st.text_area(
        "Kode R-like:",
        value=st.session_state.code,
        height=420,
        placeholder='Contoh:\nprint("Hello, world!")\ncat("Thanks")'
    )
    run = st.button("Run")

with col2:
    st.subheader("Hasil")
    tab1, tab2, tab3 = st.tabs(["Tokens (Lexical)", "AST (Syntax)", "Output"])

    if run:
        res = run_all(code)

        if not res["ok"]:
            st.error(res["error"])
        else:
            with tab1:
                st.dataframe(
                    pd.DataFrame(res["tokens"]),
                    use_container_width=True
                )
            with tab2:
                st.write(res["ast"])
            with tab3:
                st.code(res["output"], language="text")
