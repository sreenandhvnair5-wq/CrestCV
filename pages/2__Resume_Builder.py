import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# 1. MUST BE THE ABSOLUTE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Advanced Builder | CrestCV", page_icon="📝", layout="wide")

# 2. SESSION STATE INITIALIZATION
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 3. ACCESS GUARD (With Path Error Handling)
if not st.session_state.logged_in:
    st.warning("⚠️ Access Denied. Please log in first.")
    
    # We try different possible filenames to prevent the PageNotFoundError
    try:
        # Try the version with the emoji first
        st.page_link("pages/0_🔐_Login.py", label="Go to Login Page", icon="🔐")
    except:
        try:
            # Fallback if you renamed it to simple text
            st.page_link("pages/0_Login.py", label="Go to Login Page", icon="🔐")
        except:
            st.info("Please use the sidebar to navigate to the Login page.")
            
    st.stop() # Stops the builder from loading for unauthenticated users

# 4. SETUP STORAGE
SAVED_DIR = "saved_resumes"
if not os.path.exists(SAVED_DIR):
    os.makedirs(SAVED_DIR)

# --- UI LAYOUT ---
st.title("📝 Advanced Resume Builder")

tab1, tab2 = st.tabs(["✨ Create New", "📂 Saved Resumes"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", "Sreenandh V Nair")
        email = st.text_input("Email", placeholder="example@mail.com")
        phone = st.text_input("Phone", placeholder="+91 ...")
    with col2:
        job_title = st.text_input("Professional Title", placeholder="e.g. Java Developer")
        location = st.text_input("Location", placeholder="e.g. Kochi, Kerala")
    
    skills = st.text_area("Skills (use commas)", placeholder="Java, Python, SQL...")
    experience = st.text_area("Experience (use dashes -)", placeholder="- Developed AI features\n- Optimized database...")
    
    theme_color = st.sidebar.color_picker("Theme Color", "#007bff")

    # --- PDF GENERATION FUNCTION ---
    def generate_and_save():
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Simple Header using theme color
            r, g, b = tuple(int(theme_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            pdf.set_fill_color(r, g, b)
            pdf.rect(0, 0, 210, 40, 'F')
            
            pdf.set_font("Arial", 'B', 24)
            pdf.set_text_color(255, 255, 255)
            # Encode to latin-1 to avoid emoji/special character crashes
            pdf.text(20, 25, name.encode('latin-1', 'ignore').decode('latin-1'))
            
            # Content
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", 'B', 12)
            pdf.set_xy(20, 50)
            pdf.cell(0, 10, "CONTACT INFO", ln=True)
            pdf.set_font("Arial", '', 10)
            contact_text = f"Email: {email}\nPhone: {phone}\nLocation: {location}"
            pdf.multi_cell(0, 7, contact_text.encode('latin-1', 'ignore').decode('latin-1'))
            
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "PROFESSIONAL EXPERIENCE", ln=True)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 7, experience.encode('latin-1', 'ignore').decode('latin-1'))

            # Save to folder with unique name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = name.replace(' ', '_')
            filename = f"{safe_name}_{timestamp}.pdf"
            filepath = os.path.join(SAVED_DIR, filename)
            
            pdf.output(filepath)
            return filepath
        except Exception as e:
            st.error(f"Generation Error: {e}")
            return None

    if st.button("🚀 Generate & Save Resume", use_container_width=True):
        if not email or not phone:
            st.warning("Please fill in your contact details first.")
        else:
            path = generate_and_save()
            if path:
                st.success(f"Resume saved successfully!")
                with open(path, "rb") as f:
                    st.download_button(
                        label="📥 Download Now", 
                        data=f, 
                        file_name=os.path.basename(path),
                        mime="application/pdf"
                    )

# --- SECTION TO SHOW SAVED FILES ---
with tab2:
    st.header("Your Saved Documents")
    if os.path.exists(SAVED_DIR):
        files = os.listdir(SAVED_DIR)
        
        if not files:
            st.info("No saved resumes yet. Create one in the first tab!")
        else:
            # Sort by newest first
            files.sort(reverse=True)
            for file in files:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"📄 {file}")
                with col_b:
                    file_path = os.path.join(SAVED_DIR, file)
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="Download", 
                            data=f, 
                            file_name=file, 
                            key=f"dl_{file}" # Unique key prevents errors
                        )
    else:
        st.info("Storage directory not found.")
