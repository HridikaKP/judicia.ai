# import streamlit as st
# import os
# import requests
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# API_BASE = os.getenv("API_BASE_URL", "http://backend:8000")
# # API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")


# st.set_page_config(page_title="Judicia.ai", layout="centered")

# st.title("⚖️ Judicia.ai — Legal AI Assistant")

# # -------------------------------------------------------------------
# # Sidebar Settings
# # -------------------------------------------------------------------
# with st.sidebar:
#     st.header("Settings")
#     user_id = st.text_input("User ID (optional)", "")

# # -------------------------------------------------------------------
# # File Upload Section
# # -------------------------------------------------------------------
# st.subheader("📄 Upload Document (PDF / TXT)")

# uploaded = st.file_uploader("Choose a document to upload:", type=["pdf", "txt"])
# if uploaded:
#     files = {"file": (uploaded.name, uploaded.getvalue())}

#     try:
#         resp = requests.post(f"{API_BASE}/upload", files=files)
#         if resp.ok:
#             data = resp.json()
#             st.success("File uploaded & processed!")
#             st.text_area("Extracted Text Preview", data.get("content_preview", ""), height=200)
#         else:
#             st.error(f"Upload failed: {resp.text}")
#     except Exception as e:
#         st.error(str(e))

# # -------------------------------------------------------------------
# # Chat Interface
# # -------------------------------------------------------------------
# st.subheader("💬 Chat with the AI")

# input_msg = st.text_area("Enter your question:", height=120)

# if st.button("Send Message"):
#     payload = {
#         "user_id": int(user_id) if user_id.strip() != "" else None,
#         "message": input_msg
#     }

#     try:
#         resp = requests.post(f"{API_BASE}/chat", json=payload)
#         if resp.ok:
#             st.markdown("**Response:**")
#             st.write(resp.json().get("reply"))
#         else:
#             st.error(resp.text)
#     except Exception as e:
#         st.error(str(e))

# # -------------------------------------------------------------------
# # Chat History Section
# # -------------------------------------------------------------------
# st.subheader("📜 Recent Chat History")

# if st.button("Load History"):
#     try:
#         resp = requests.get(f"{API_BASE}/history")
#         if resp.ok:
#             for item in resp.json():
#                 st.write(f"**User:** {item['message']}")
#                 st.write(f"**Bot:** {item['response']}")
#                 st.write("---")
#         else:
#             st.error("Failed to load history.")
#     except Exception as e:
#         st.error(str(e))




import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# IMPORTANT: Use localhost for local development
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Judicia.ai - Legal AI Assistant", layout="wide")

def local_css():
    st.markdown(
        """
        <style>
        * { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .app-header { display:flex; align-items:center; gap:16px; padding: 12px 0; border-bottom: 2px solid #e5e7eb; }
        .title { font-size:32px; font-weight:800; color: #1f2937; }
        .subtitle { color: #6b7280; margin-top: 4px; font-size: 14px; font-weight: 500; }
        .chat-container { background: linear-gradient(to bottom, #f9fafb, #f3f4f6); padding: 16px; border-radius: 12px; height: 60vh; overflow: auto; border: 1px solid #e5e7eb; }
        .user-bubble { background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; padding: 12px 16px; border-radius: 18px; margin: 8px 0; max-width: 75%; margin-left: auto; box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2); }
        .bot-bubble { background: white; color: #1f2937; padding: 12px 16px; border-radius: 18px; margin: 8px 0; max-width: 75%; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); }
        .meta { font-size: 11px; color: #9ca3af; margin-top: 4px; font-weight: 500; }
        h3 { color: #1f2937; font-weight: 700; }
        .stButton>button { background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border: none; border-radius: 6px; font-weight: 600; padding: 8px 16px; }
        .stButton>button:hover { background: linear-gradient(135deg, #1d4ed8, #1e40af); }
        .stTextArea textarea { border-radius: 8px; border: 1px solid #d1d5db; }
        .stFileUploader { border-radius: 8px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


local_css()

cols = st.columns([3, 1])
with cols[0]:
    st.markdown('<div class="app-header"><div class="title">⚖️ Judicia.ai</div><div class="subtitle">AI-Powered Legal Research & Document Analysis Platform</div></div>', unsafe_allow_html=True)
with cols[1]:
    st.image("https://raw.githubusercontent.com/hridikakp/judicia.ai/main/docs/logo.png" if os.path.exists("docs/logo.png") else "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Scale_of_justice.svg/1024px-Scale_of_justice.svg.png", width=72)

# Sidebar Settings
with st.sidebar:
    st.header("⚙️ Settings & Controls")
    user_id = st.text_input("User ID (optional)", placeholder="Enter your ID")
    show_history = st.checkbox("Save chat history", value=False)
    if st.button("🗑️ Clear Conversation"):
        st.session_state["messages"] = []
        st.rerun()
    st.markdown("---")
    st.markdown("### 💡 Example Queries")
    if st.button("📜 Contract Liability Analysis"):
        st.session_state.setdefault("messages", []).append({"role": "user", "text": "What are the key liabilities in contract breach?"})
        st.rerun()
    if st.button("✉️ Rental Notice Draft"):
        st.session_state.setdefault("messages", []).append({"role": "user", "text": "Draft a professional notice for unpaid rent."})

# Initialize session storage for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []


def send_to_backend(message_text):
    payload = {"user_id": int(user_id) if user_id.strip() else None, "message": message_text}
    try:
        resp = requests.post(f"{API_BASE}/chat", json=payload, timeout=30)
        if resp.ok:
            return resp.json().get("reply")
        else:
            return f"[Error] {resp.status_code}: {resp.text}"
    except Exception as e:
        return f"[Exception] {e}"


# Layout: left = chat, right = upload & doc preview
left, right = st.columns([3, 1])

with right:
    st.markdown("### 📄 Document Upload")
    st.caption("Attach PDFs or text files for AI analysis")
    uploaded = st.file_uploader("Drop files here", type=["pdf", "txt"], key="uploader")
    if uploaded is not None:
        with st.spinner("⏳ Processing document..."):
            files = {"file": (uploaded.name, uploaded.getvalue())}
            try:
                resp = requests.post(f"{API_BASE}/upload", files=files, timeout=60)
                if resp.ok:
                    data = resp.json()
                    st.success("✅ Document processed successfully")
                    preview = data.get("content_preview") or data.get("content") or "(No preview available)"
                    st.text_area("📋 Extracted Content", preview, height=220, disabled=True)
                else:
                    st.error(f"❌ Upload failed: {resp.text}")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    st.markdown("---")
    st.markdown("### 📚 Best Practices")
    st.caption(
        "• Use specific, legal queries\n"
        "• Reference uploaded documents\n"
        "• Ask follow-up questions\n"
        "• Review AI responses carefully"
    )

with left:
    st.markdown("### 💬 Conversation")
    chat_box = st.container()
    with chat_box:
        st.markdown('<div class="chat-container" id="chat">', unsafe_allow_html=True)
        for msg in st.session_state["messages"]:
            if msg["role"] == "user":
                st.markdown(f'<div style="display:flex; justify-content:flex-end"><div class="user-bubble">{msg["text"]}<div class="meta">You • Just now</div></div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="display:flex; justify-content:flex-start"><div class="bot-bubble">{msg["text"]}<div class="meta">Judicia.ai • AI Response</div></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Input area
    st.markdown("---")
    st.markdown("### Ask a Question")
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area("Enter your legal query here...", height=100, key="input_msg", placeholder="E.g., 'What is the statute of limitations for contract disputes?'")
        col1, col2, col3 = st.columns([1, 1, 8])
        with col1:
            send = st.form_submit_button("📤 Send", use_container_width=True)
        with col2:
            if st.form_submit_button("💡 Example", use_container_width=True):
                st.session_state.setdefault("messages", []).append({"role": "user", "text": "What are the key liabilities in contract breach?"})
                reply = send_to_backend("What are the key liabilities in contract breach?")
                st.session_state.setdefault("messages", []).append({"role": "bot", "text": reply})
                st.rerun()

    if send and user_input.strip():
        st.session_state.setdefault("messages", []).append({"role": "user", "text": user_input})
        with st.spinner("🔍 Analyzing your query..."):
            reply = send_to_backend(user_input)
        st.session_state.setdefault("messages", []).append({"role": "bot", "text": reply})
        st.rerun()

    # Load history button
    st.markdown("---")
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        if st.button("📜 Load Chat History", use_container_width=True):
            with st.spinner("Loading..."):
                try:
                    resp = requests.get(f"{API_BASE}/history", timeout=10)
                    if resp.ok:
                        data = resp.json()
                        st.session_state["messages"] = []
                        for item in data:
                            st.session_state["messages"].append({"role": "user", "text": item.get("message")})
                            st.session_state["messages"].append({"role": "bot", "text": item.get("response")})
                        st.success("✅ History loaded")
                        st.rerun()
                    else:
                        st.error("❌ Failed to load history")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    with col_h2:
        st.caption("💡 Requires database connection")
