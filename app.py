%%writefile app.py
import streamlit as st
import pandas as pd
from interpreter import run_all

st.set_page_config(page_title="R-like Interpreter (4 Scripts)", layout="wide")
st.title("R-like Interpreter (PLY) — 4 Scripts dari PPT")

SCRIPTS = {
    "1) Hello": """print("Hello, world!")
cat("Thanks")
""",
    "2) Sum and Average": """num1 <- 10
num2 <- 20
num3 <- 30

sum <- num1 + num2 + num3
avg <- sum / 3

cat("Num1 is ", num1, "\\n")
cat("Num2 is ", num2, "\\n")
cat("Num3 is ", num3, "\\n")
cat("Sum 3 numbers is ", sum, "\\n")
cat("Average is ", avg, "\\n")
""",
    "3) Big Number": """num1 <- 10
num2 <- 20

if (num1 > num2) {
  bignum <- num1
  cat("Big Number is ", bignum, "\\n")
} else {
  bignum <- num2
  cat("Big Number is ", bignum, "\\n")
}
""",
    "4) List Odd Number (1-100)": """cat("List of Odd Number 1-100: \\n")

num <- 1
while (num <= 100) {
  sisa <- num %% 2
  if (sisa != 0) {
    oddnum <- num
    cat(oddnum, " ")
  }
  num <- num + 1
}
""",
}

# pilih script default dari 4
choice = st.selectbox("Pilih script contoh:", list(SCRIPTS.keys()), index=0)

uploaded = st.file_uploader("Atau upload file .r / .txt", type=["r", "txt"])

if "code" not in st.session_state:
    st.session_state.code = SCRIPTS[choice]

# kalau ganti pilihan, update code (kecuali user lagi upload)
if uploaded is None:
    st.session_state.code = SCRIPTS[choice]

if uploaded is not None:
    st.session_state.code = uploaded.read().decode("utf-8")
    st.info("File berhasil di-load dari upload.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Code")
    code = st.text_area("Kode:", value=st.session_state.code, height=420)
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
                st.dataframe(pd.DataFrame(res["tokens"]), use_container_width=True)
            with tab2:
                st.write(res["ast"])
            with tab3:
                st.code(res["output"], language="text")
