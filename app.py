import streamlit as st
import pandas as pd
from interpreter import run_all

st.set_page_config(page_title="R-like Interpreter (Upload Only)", layout="wide")
st.title("R-like Interpreter (PLY) — Upload .r")

uploaded = st.file_uploader("Upload file .r / .txt", type=["r", "txt"])

if uploaded is None:
    st.info("Silakan upload file .r dulu untuk menjalankan interpreter.")
    st.stop()

code = uploaded.read().decode("utf-8", errors="replace")

st.success(f"File loaded: {uploaded.name}")

# optional: tampilkan isi file (kalau kamu mau benar-benar dihapus, hapus blok ini)
with st.expander("Lihat isi file (optional)"):
    st.code(code, language="r")

run = st.button("Run")

if run:
    res = run_all(code)
    if not res["ok"]:
        st.error(res["error"])
    else:
        tab1, tab2, tab3 = st.tabs(["Tokens (Lexical)", "AST (Syntax)", "Output"])

        with tab1:
            st.dataframe(pd.DataFrame(res["tokens"]), use_container_width=True)

        with tab2:
            st.write(res["ast"])

        with tab3:
            st.code(res["output"], language="text")
"text")
