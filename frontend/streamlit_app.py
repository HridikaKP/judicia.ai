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
# IMPORTANT: Force backend URL inside Docker network
API_BASE = "http://backend:8000"
st.set_page_config(page_title="Judicia.ai", layout="centered")
st.title(":scales: Judicia.ai — Legal AI Assistant")
# -------------------------------------------------------------------
# Sidebar Settings
# -------------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    user_id = st.text_input("User ID (optional)", "")
# -------------------------------------------------------------------
# File Upload Section
# -------------------------------------------------------------------
st.subheader(":page_facing_up: Upload Document (PDF / TXT)")
uploaded = st.file_uploader("Choose a document to upload:", type=["pdf", "txt"])
if uploaded:
    files = {"file": (uploaded.name, uploaded.getvalue())}
    try:
        resp = requests.post(f"{API_BASE}/upload", files=files)
        if resp.ok:
            data = resp.json()
            st.success("File uploaded & processed!")
            st.text_area("Extracted Text Preview", data.get("content_preview", ""), height=200)
        else:
            st.error(f"Upload failed: {resp.text}")
    except Exception as e:
        st.error(str(e))
# -------------------------------------------------------------------
# Chat Interface
# -------------------------------------------------------------------
st.subheader(":speech_bubble: Chat with the AI")
input_msg = st.text_area("Enter your question:", height=120)
if st.button("Send Message"):
    payload = {
        "user_id": int(user_id) if user_id.strip() else None,
        "message": input_msg
    }
    try:
        resp = requests.post(f"{API_BASE}/chat", json=payload)
        if resp.ok:
            st.markdown("*Response:*")
            st.write(resp.json().get("reply"))
        else:
            st.error(resp.text)
    except Exception as e:
        st.error(str(e))
# -------------------------------------------------------------------
# Chat History Section
# -------------------------------------------------------------------
st.subheader(":scroll: Recent Chat History")
if st.button("Load History"):
    try:
        resp = requests.get(f"{API_BASE}/history")
        if resp.ok:
            for item in resp.json():
                st.write(f"*User:* {item['message']}")
                st.write(f"*Bot:* {item['response']}")
                st.write("---")
        else:
            st.error("Failed to load history.")
    except Exception as e:
        st.error(str(e))