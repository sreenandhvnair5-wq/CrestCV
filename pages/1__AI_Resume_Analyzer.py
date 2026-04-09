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
st.set_page_config(page_title="Neural Audit | CrestCV", layout="wide", page_icon="🔍")

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

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🧠 CrestCV")
    st.info("Free AI Resume Analysis. No account required.")
    
    if 'resume_text' in st.session_state:
        st.success("Resume Loaded ✅")
        if st.button("🧹 Clear Session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
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

# --- 4. MAIN UI INPUTS ---
col_in1, col_in2 = st.columns(2)
with col_in1:
    st.subheader("1. Job Requirements")
    jd_input = st.text_area("Paste Job Description...", height=200, placeholder="Paste the job requirements here...")
with col_in2:
    st.subheader("2. Your Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type="pdf")

# Extraction Logic (Hidden from UI)
if uploaded_file:
    if "last_file" not in st.session_state or st.session_state.last_file != uploaded_file.name:
        with st.spinner("Extracting Knowledge..."):
            extracted = extract_text(uploaded_file)
            st.session_state['resume_text'] = extracted
            st.session_state['last_file'] = uploaded_file.name
            st.rerun()

# --- 5. THE AUDIT BUTTON (Always Visible) ---
st.divider()
if st.button("🚀 Run Neural Audit", use_container_width=True):
    # Check for missing inputs first
    if not jd_input.strip():
        st.warning("⚠️ Please paste a Job Description to proceed.")
    elif not uploaded_file:
        st.warning("⚠️ Please upload your Resume PDF to proceed.")
    else:
        # If everything is there, run the AI
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
                st.session_state['last_analysis'] = data 
                st.rerun() # Refresh to show results
            except Exception as e:
                st.error("AI Analysis failed. Please check your API key or try again.")

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

# --- 6. CHATBOT SECTION ---
st.divider()
st.header("💬 AI Career Coach")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

if prompt := st.chat_input("Ask about your resume improvements..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    context = st.session_state.get('resume_text', '')
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = get_chatbot_response(prompt, context)
            st.write(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
