import streamlit as st
import pandas as pd
from interpreter import run_all

st.set_page_config(page_title="R-like Interpreter (PLY)", layout="wide")
st.title("Lexical Analyzer Development R-like Scripting")

mode = st.radio(
    "Mode input:",
    ["Upload file (.r/.txt)", "Tulis / Paste code"],
    horizontal=True
)

code = ""

if mode == "Upload file (.r/.txt)":
    uploaded = st.file_uploader("Upload file .r / .txt", type=["r", "txt"])
    if uploaded is None:
        st.info("Upload file dulu, atau pindah ke mode 'Tulis / Paste code'.")
        st.stop()

    code = uploaded.read().decode("utf-8", errors="replace")
    st.success(f"File berhasil di-load: {uploaded.name}")

    with st.expander("Preview code (.r)"):
        st.code(code, language="r")

else:
    st.info("Tulis / paste kode di bawah ini, lalu klik Run.")
    code = st.text_area(
        "Code:",
        height=300,
        placeholder='Contoh:\nprint("Hello, world!")\ncat("Thanks")'
    )

    if not code.strip():
        st.warning("Kodenya masih kosong.")
        st.stop()

run = st.button("Run")

if run:
    result = run_all(code)

    if not result["ok"]:
        st.error(result["error"])
    else:
        tab1, tab2, tab3 = st.tabs(["Tokens (Lexical)", "AST (Syntax)", "Output"])

        with tab1:
            st.dataframe(pd.DataFrame(result["tokens"]), use_container_width=True)

        with tab2:
            st.write(result["ast"])

        with tab3:
            st.code(result["output"], language="text")

