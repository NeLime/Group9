import streamlit as st
import pandas as pd
from interpreter import run_all

st.set_page_config(page_title="R-like Interpreter (Upload Only)", layout="wide")
st.title("R-like Interpreter (PLY) — Upload .r")

uploaded = st.file_uploader("Upload file .r / .txt", type=["r", "txt"])

if uploaded is None:
    st.info("Silakan upload file .r terlebih dahulu.")
    st.stop()

code = uploaded.read().decode("utf-8", errors="replace")

st.success(f"File berhasil di-load: {uploaded.name}")

run = st.button("Run")

if run:
    result = run_all(code)

    if not result["ok"]:
        st.error(result["error"])
    else:
        tab1, tab2, tab3 = st.tabs([
            "Tokens (Lexical)",
            "AST (Syntax)",
            "Output"
        ])

        with tab1:
            st.dataframe(
                pd.DataFrame(result["tokens"]),
                use_container_width=True
            )

        with tab2:
            st.write(result["ast"])

        with tab3:
            st.code(result["output"], language="text")

