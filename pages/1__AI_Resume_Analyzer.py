import streamlit as st
import fitz  # PyMuPDF
from groq import Groq
import re
import json
import os

# --- 1. CORE AI FUNCTIONS ---
# Initialize Groq client using secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = " ".join([page.get_text() for page in doc])
    return text.lower()

def get_chatbot_response(user_query, resume_context):
    try:
        context_snippet = resume_context[:2000] if resume_context else "No resume uploaded yet."
        system_prompt = f"You are a career coach. Base your answers on this resume context: {context_snippet}"
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- 2. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="CrestCV | AI Resume Intelligence", layout="wide", page_icon="🧠")

# Security Guard: Ensures user came from the Home page login
if not st.session_state.get('logged_in', False):
    st.warning("⚠️ Please login on the Home page to access the Neural Audit.")
    st.page_link("Home.py", label="Go to Login", icon="🏠")
    st.stop()

st.markdown("""
    <style>
    .stApp { background: transparent; }
    .header-box {
        display: flex; align-items: center; gap: 20px; padding: 20px;
        background: rgba(59, 130, 246, 0.1); border-radius: 15px; margin-bottom: 30px;
    }
    .res-card {
        background-color: rgba(120, 120, 120, 0.05); border-left: 5px solid #2563eb;
        padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        animation: fadeIn 0.8s ease-out;
    }
    .card-title { color: #1e40af; font-weight: 700; text-transform: uppercase; }
    .metric-value { font-size: 2.2rem; font-weight: 900; color: #2563eb; }
    @keyframes fadeIn {
      0% { opacity: 0; transform: translateY(20px); }
      100% { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (CLEANED) ---
with st.sidebar:
    st.title("🧠 CrestCV Dashboard")
    st.write(f"User: **{st.session_state.get('username', 'Guest')}**")
    
    if 'resume_text' in st.session_state:
        if st.button("💾 Save to Profile"):
            if not os.path.exists("saved_data"): 
                os.makedirs("saved_data")
            un = st.session_state.get('username', 'user')
            with open(f"saved_data/{un}_resume.txt", "w", encoding="utf-8") as f:
                f.write(st.session_state['resume_text'])
            st.success("Saved to server!")
    
    st.divider()
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- 4. MAIN UI ---
logo_url = "https://cdn-icons-png.flaticon.com/512/2103/2103633.png" 
st.markdown(f"""
    <div class="header-box">
        <img src="{logo_url}" width="60">
        <div>
            <h1 style='margin:0; padding:0; color:#1e40af;'>CrestCV</h1>
            <p style='margin:0; font-size:0.9rem; color:grey;'>Advanced AI Career Analytics</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

col_in1, col_in2 = st.columns(2)
with col_in1:
    st.subheader("1. Job Requirements")
    jd_input = st.text_area("Paste Job Description...", height=200)
with col_in2:
    st.subheader("2. Your Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type="pdf")

# Process File Upload
if uploaded_file and jd_input:
    if "last_file" not in st.session_state or st.session_state.last_file != uploaded_file.name:
        with st.spinner("Extracting Knowledge..."):
            extracted = extract_text(uploaded_file)
            st.session_state['resume_text'] = extracted
            st.session_state['last_file'] = uploaded_file.name
            st.rerun()

    if st.button("🚀 Run Neural Audit", use_container_width=True):
        with st.spinner("🧠 Deep AI Audit in progress..."):
            current_res = st.session_state.get('resume_text', '')
            analysis_prompt = f"""
            Analyze this Resume for a professional role.
            Resume: {current_res[:2000]}
            JD: {jd_input[:2000]}
            Return ONLY JSON:
            {{ "score": 85, "tech_fit": [], "soft_skills": [], "formatting": [], "missing_keywords": [] }}
            """
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": analysis_prompt}],
                    response_format={ "type": "json_object" } 
                )
                data = json.loads(response.choices[0].message.content)
                st.session_state['last_analysis'] = data # Store for persistence
            except Exception as e:
                st.error("AI Analysis failed.")

# --- 5. DISPLAY RESULTS ---
if 'last_analysis' in st.session_state:
    data = st.session_state['last_analysis']
    st.divider()
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f'<div class="res-card"><div class="card-title">ATS Score</div><div class="metric-value">{data.get("score", 0)}%</div></div>', unsafe_allow_html=True)
    with c2:
        keywords = data.get("missing_keywords", [])
        st.markdown(f'<div class="res-card"><div class="card-title">⚠️ Missing Keywords</div><p>{" • ".join(keywords) if keywords else "None detected"}</p></div>', unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown('<div class="res-card"><div class="card-title">💻 Technical</div>', unsafe_allow_html=True)
        for p in data.get("tech_fit", []): st.write(f"🔹 {p}")
        st.markdown('</div>', unsafe_allow_html=True)
    with t2:
        st.markdown('<div class="res-card"><div class="card-title">🤝 Soft Skills</div>', unsafe_allow_html=True)
        for p in data.get("soft_skills", []): st.write(f"🔹 {p}")
        st.markdown('</div>', unsafe_allow_html=True)
    with t3:
        st.markdown('<div class="res-card"><div class="card-title">📄 Formatting</div>', unsafe_allow_html=True)
        for p in data.get("formatting", []): st.write(f"🔹 {p}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. MOBILE FIXED CHATBOT ---
st.divider()
st.header("💬 AI Career Coach")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show previous messages
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

if prompt := st.chat_input("Ask NeuralCV about your resume..."):
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generate AI Response safely
    context = st.session_state.get('resume_text', '')
    with st.chat_message("assistant"):
        with st.spinner("NeuralCV is thinking..."):
            answer = get_chatbot_response(prompt, context)
            st.write(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
