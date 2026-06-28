import streamlit as st

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="📄",
    layout="wide",
)

# ------------------ SESSION ------------------ #

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ SIDEBAR ------------------ #

with st.sidebar:

    st.title("📄 AI Document Assistant")

    st.caption("Retrieval Augmented Generation")

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success("✅ PDF Uploaded")

        st.info(f"""
📄 **Name**

{uploaded_file.name}

📦 **Size**

{round(uploaded_file.size/1024,2)} KB
""")

    st.divider()

    st.subheader("⚙ Model")

    st.write("**LLM**")
    st.code("Llama 3.3 70B")

    st.write("**Embeddings**")
    st.code("MiniLM-L6-v2")

    st.write("**Vector DB**")
    st.code("FAISS")

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages=[]

        st.rerun()

# ------------------ MAIN PAGE ------------------ #

st.title("💬 Chat with your Documents")

st.caption("Ask questions from your uploaded PDFs using Retrieval-Augmented Generation (RAG).")

st.divider()

# ------------------ WELCOME CARD ------------------ #

if len(st.session_state.messages)==0:

    st.info("""
### 👋 Welcome

Upload one or more PDF documents from the sidebar.

Then ask questions like:

• What is Normalization?

• Explain DBMS Architecture

• What is Deadlock?

• Summarize Chapter 5

---

### Features

✅ RAG

✅ Semantic Search

✅ FAISS Vector Database

✅ HuggingFace Embeddings

✅ Groq LLM

""")

# ---------------- CHAT ---------------- #

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# ---------------- INPUT ---------------- #

question = st.chat_input("Ask something about your PDF...")

if question:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Searching document..."):

            # TEMP RESPONSE
            answer = """
This is where the RAG engine response will appear.

---

### 📄 Sources

DBMS.pdf

Page 96

Similarity : 97%
"""

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )