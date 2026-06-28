import streamlit as st
from engine import process_pdfs, ask_question

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ CUSTOM STYLING (CSS) ------------------ #
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    html, body, [data-testid="stSidebar"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Modern Headers */
    .main-title {
        font-size: 2.25rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.25rem;
        letter-spacing: -0.025em;
    }
    .subtitle {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    
    /* Custom Info & Stats Cards */
    .meta-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .meta-title {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748B;
        margin-bottom: 0.5rem;
        letter-spacing: 0.05em;
    }
    .meta-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
    }
    
    /* Feature & Setup Cards */
    .feature-card {
        background-color: #FFFFFF;
        border: 1px solid #F1F5F9;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        height: 100%;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.05);
    }
    
    /* Source Snippets */
    .source-box {
        background-color: #F8FAFC;
        border-left: 4px solid #2563EB;
        border-radius: 4px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    .source-page {
        font-weight: 600;
        color: #2563EB;
        font-size: 0.85rem;
        margin-bottom: 0.25rem;
    }
    
    /* Pills & Badges */
    .pill {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1E40AF;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid #BFDBFE;
    }
    .pill-green {
        background-color: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
    }
    
    /* Adjust spacing */
    .block-container {
        padding-top: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------ #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

# ------------------ SIDEBAR ------------------ #

with st.sidebar:
    st.markdown("<h2 style='margin-bottom:0px; font-weight:700;'>📄 DocuMind</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size:0.9rem; margin-bottom:1.5rem;'>RAG-Powered Chat Assistant</p>", unsafe_allow_html=True)
    
    st.subheader("Upload Document")
    uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True,  # Allow multiple files
    label_visibility="collapsed"
)


    if uploaded_files:
        if st.session_state.vector_db is None:
            with st.spinner("Analyzing documents..."):
                st.session_state.vector_db = process_pdfs(uploaded_files)
        
        file_names = ", ".join([f.name for f in uploaded_files])
        total_size = sum([f.size for f in uploaded_files])
        
        st.markdown(f"""
        <div class="meta-card">
            <div class="meta-title">Status</div>
            <div class="meta-value" style="color: #10B981; display: flex; align-items: center; gap: 6px;">
                <span class="pill pill-green" style="margin: 0;">{len(uploaded_files)} Files Loaded</span>
            </div>
            <div class="meta-title" style="margin-top: 1rem;">Document(s)</div>
            <div class="meta-value" style="font-size: 0.95rem; word-break: break-all;">{file_names}</div>
            <div class="meta-title" style="margin-top: 1rem;">Total Size</div>
            <div class="meta-value" style="font-size: 0.95rem;">{round(total_size/1024, 2)} KB</div>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("System Architecture")
        st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <div style="font-size: 0.85rem; margin-bottom: 0.25rem; font-weight:500; color:#475569;">Large Language Model</div>
            <span class="pill">Llama 3.3 70B</span>
            <div style="font-size: 0.85rem; margin-top: 0.5rem; margin-bottom: 0.25rem; font-weight:500; color:#475569;">Embeddings</div>
            <span class="pill">MiniLM-L6-v2</span>
            <div style="font-size: 0.85rem; margin-top: 0.5rem; margin-bottom: 0.25rem; font-weight:500; color:#475569;">Vector Index</div>
            <span class="pill">FAISS</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# ------------------ MAIN PAGE ------------------ #

st.markdown("<div class='main-title'>💬 Chat with your Documents</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ask questions from your uploaded PDFs using Retrieval-Augmented Generation (RAG).</div>", unsafe_allow_html=True)

# ------------------ WELCOME CARD ------------------ #

if len(st.session_state.messages) == 0:
    st.markdown("### Get Started")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4 style="margin-top:0; color:#0F172A; font-weight: 600;">👋 Welcome to DocuMind</h4>
            <p style="color:#475569; font-size:0.95rem; line-height: 1.5;">
                Upload one or multiple PDF documents using the sidebar. Once uploaded, the engine will split, embed, and store all documents' context for rapid semantic query answering.
            </p>
            <h5 style="color:#0F172A; font-weight: 600; margin-bottom: 0.5rem;">Suggested Queries:</h5>
            <ul style="color:#475569; font-size:0.9rem; padding-left: 1.2rem;">
                <li style="margin-bottom:0.25rem;">What are the core concepts covered?</li>
                <li style="margin-bottom:0.25rem;">Explain the main architecture or flow.</li>
                <li style="margin-bottom:0.25rem;">Summarize the key findings.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4 style="margin-top:0; color:#0F172A; font-weight: 600;">🚀 Technical Details</h4>
            <p style="color:#475569; font-size:0.95rem; line-height: 1.5;">
                This RAG pipeline leverages local semantic processing and cloud-hosted LLM execution:
            </p>
            <div style="margin-top: 1rem;">
                <span class="pill">RecursiveCharacterTextSplitter</span>
                <span class="pill">HuggingFace Embeddings</span>
                <span class="pill">FAISS Indexing</span>
                <span class="pill">Groq Cloud Inference API</span>
                <span class="pill">Llama 3.3 LLM</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------- CHAT HISTORY ---------------- #

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT & PROCESSING ---------------- #

question = st.chat_input("Ask something about your PDF...")

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching document references and synthesizing response..."):
            if st.session_state.vector_db is None:
                st.warning("Please upload a PDF document in the sidebar to begin.")
                st.stop()

            answer, sources = ask_question(
                st.session_state.vector_db,
                question
            )
            
            st.markdown(answer)
            
            # Render sources beautifully
            if sources:
                with st.expander("🔍 View Retrieved Sources & Context", expanded=False):
                    for source in sources:
                        st.markdown(f"""
                        <div class="source-box">
                            <div class="source-page">{source.get('source', 'Unknown File')} — Page {source['page']}</div>
                            <div style="color: #334155; font-size: 0.9rem; line-height: 1.4;">"{source['content']}..."</div>
                        </div>
                        """, unsafe_allow_html=True)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
