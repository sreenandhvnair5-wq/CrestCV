import streamlit as st

st.set_page_config(page_title="CrestCV | Professional AI Career Tools", page_icon="🏠", layout="wide")

# Custom CSS for a clean look
st.markdown("""
    <style>
    .main-title { font-size: 50px; font-weight: bold; color: #007bff; text-align: center; }
    .sub-title { font-size: 24px; text-align: center; color: #555; margin-bottom: 30px; }
    .article-box { padding: 20px; border-radius: 10px; background-color: #f9f9f9; border-left: 5px solid #007bff; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="main-title">CrestCV</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Master Your Career with AI-Powered Precision</div>', unsafe_allow_html=True)

st.image("https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&q=80&w=1000", use_container_width=True)

st.divider()

# Main Content - Two Column Articles
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="article-box">', unsafe_allow_html=True)
    st.subheader("🚀 The 6-Second Rule")
    st.write("""
    Did you know recruiters spend an average of **6 seconds** looking at a resume before deciding to keep it or toss it? 
    In 2026, the competition is even higher. CrestCV helps you optimize your layout to ensure your most important skills 
    hit the recruiter's eye instantly.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="article-box">', unsafe_allow_html=True)
    st.subheader("💡 Why ATS Matters")
    st.write("""
    75% of resumes are rejected by **Applicant Tracking Systems (ATS)** before a human even sees them. 
    Our AI Resume Analyzer scans your document for the exact keywords top firms are looking for, 
    giving you the "inside edge" on the algorithm.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.subheader("Available Tools")
    st.info("👈 Use the sidebar to navigate between our tools!")
    
    with st.expander("🔍 AI Resume Analyzer"):
        st.write("Upload your PDF and get an instant score, keyword analysis, and improvement tips.")
        
    with st.expander("📝 Pro Resume Builder"):
        st.write("Enter your details and generate a clean, modern, ATS-friendly PDF resume in seconds.")

st.divider()

# Bottom Content for AdSense (SEO)
st.header("Career Growth Tips for 2026")
st.write("""
Landing a dream job in the modern market requires more than just a list of past roles. It requires a 
**Personal Brand**. At CrestCV, we believe that your resume should be a living document that evolves 
with the industry. Whether you are a developer in Kerala or a designer in London, your story needs 
to be told with clarity and data-driven results.
""")

st.caption("© 2026 CrestCV - All Rights Reserved.")
st.write("---")
col_a, col_b = st.columns([2, 1])
with col_a:
    st.subheader("Want to save your progress?")
    st.write("Create a free account to store your AI audits and generated resumes.")
with col_b:
    st.page_link("pages/0__Login-Signup.py", label="Login / Sign Up", icon="🔐", use_container_width=True)
