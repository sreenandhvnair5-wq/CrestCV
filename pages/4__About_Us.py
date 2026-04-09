import streamlit as st

st.set_page_config(page_title="About Us | CrestCV", page_icon="👨‍💻")

st.title("👨‍💻 About CrestCV")

col1, col2 = st.columns([1, 2])

with col1:
    # You can put a link to a professional photo or use a placeholder
    st.image("https://cdn-icons-png.flaticon.com/512/6009/6009015.png", width=150)

with col2:
    st.subheader("Our Mission")
    st.write("""
    CrestCV was founded in **Kerala, India**, with a simple goal: to democratize 
    career success using Artificial Intelligence. 
    
    We believe that everyone deserves a professional-grade resume, regardless 
    of their design skills. Our tools are built to be fast, free, and effective 
    for the modern job market.
    """)

st.divider()
st.info("Built with ❤️ using Streamlit, Groq AI, and Python.")

