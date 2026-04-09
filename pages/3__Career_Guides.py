import streamlit as st

st.set_page_config(page_title="Career Guides | CrestCV", page_icon="📚")

st.title("📚 Career Success Guides")
st.write("Expert advice to help you land your dream job in 2026.")

tab1, tab2, tab3 = st.tabs(["ATS Secrets", "Interview Tips", "LinkedIn Growth"])

with tab1:
    st.header("How to Beat the ATS")
    st.write("""
    **What is an ATS?**
    The Applicant Tracking System is a robot that reads your resume before a human does.
    
    **3 Tips to Pass:**
    1. **Use Standard Headings:** Stick to 'Work Experience' and 'Education'.
    2. **Avoid Graphics:** Don't put important info inside tables or images; the robot can't read them.
    3. **Keyword Matching:** If the job description says 'Python', make sure 'Python' is in your resume!
    """)

with tab2:
    st.header("Mastering the 2026 Interview")
    st.write("""
    Most interviews now happen over video calls. 
    - **The Lighting:** Face a window so your face is clear.
    - **The Background:** Keep it professional and clutter-free.
    - **The STAR Method:** Answer questions by explaining the **S**ituation, **T**ask, **A**ction, and **R**esult.
    """)

with tab3:
    st.header("Optimizing your LinkedIn")
    st.write("Your LinkedIn is your digital resume. Ensure your 'Headline' includes keywords like 'Full Stack Developer' or 'Data Scientist'.")
