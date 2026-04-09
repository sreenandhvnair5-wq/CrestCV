import streamlit as st
import os

# Page Config for SEO
st.set_page_config(
    page_title="CrestCV | AI Resume Intelligence & Builder",
    page_icon="🧠",
    layout="wide"
)

# --- 1. SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# --- 2. STYLING ---
st.markdown("""
    <style>
    .main-title { font-size: 50px; font-weight: bold; color: #1e40af; text-align: center; margin-bottom: 0px;}
    .sub-title { font-size: 20px; text-align: center; color: #64748b; margin-bottom: 30px; }
    .hero-card { padding: 30px; border-radius: 15px; background: #f8fafc; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN LOGIC (Fixed for Android) ---
def login_form():
    st.markdown('<div class="main-title">CrestCV</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Sign in to unlock AI features</div>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            with st.form("mobile_login"):
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login to Dashboard", use_container_width=True)
                if submitted:
                    if u == "admin" and p == "123": # Simple auth for now
                        st.session_state.logged_in = True
                        st.session_state.username = u
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            st.info("Demo: admin / 123")

# --- 4. MAIN PAGE CONTENT ---
if not st.session_state.logged_in:
    login_form()
else:
    st.markdown('<div class="main-title">CrestCV Dashboard</div>', unsafe_allow_html=True)
    st.write(f"Welcome back, **{st.session_state.username}**!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="hero-card">
            <h3>🚀 AI Neural Audit</h3>
            <p>Upload your resume and get a deep analysis of missing keywords and ATS scores.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Open Analyzer", use_container_width=True):
            st.switch_page("pages/1_🔍_AI_Analyzer.py")

    with col2:
        st.markdown("""<div class="hero-card">
            <h3>📝 Pro Builder</h3>
            <p>Create an advanced, Canva-style resume optimized for 2026 hiring trends.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Open Builder", use_container_width=True):
            st.switch_page("pages/2_📝_Resume_Builder.py")

    st.divider()
    st.subheader("Latest Career Insights")
    st.write("Check out our **Career Guides** in the sidebar to master the 6-second recruiter rule.")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
