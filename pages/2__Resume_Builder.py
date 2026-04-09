import streamlit as st
from fpdf import FPDF # Modern fpdf2 library
import json
import os
from groq import Groq

# --- 1. INITIALIZE AI ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def ai_improve_text(text, type="experience"):
    """Uses AI to rewrite basic text into professional resume bullet points."""
    try:
        prompt = f"Rewrite the following resume {type} section into 3 high-impact, professional bullet points using action verbs and metrics. Keep it concise: {text}"
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except:
        return text

# --- 2. UNICODE-SAFE PDF CLASS ---
class ResumePDF(FPDF):
    def header(self):
        # Name
        self.set_font('helvetica', 'B', 16)
        self.cell(0, 10, self.safe_text(self.resume_name), ln=True, align='C')
        # Basic Sub-header
        self.set_font('helvetica', '', 9)
        info = f"{self.email} | {self.phone} | {self.address}"
        self.cell(0, 5, self.safe_text(info), ln=True, align='C')
        # Secondary Personal Info
        personal = f"DOB: {self.dob} | Gender: {self.gender} | Marital Status: {self.marital}"
        self.cell(0, 5, self.safe_text(personal), ln=True, align='C')
        self.ln(10)

    def safe_text(self, text):
        """Fixes the UnicodeEncodeError by swapping unknown characters."""
        return text.encode('latin-1', 'replace').decode('latin-1')

    def section_title(self, title):
        self.set_font('helvetica', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, self.safe_text(title), ln=True, fill=True)
        self.ln(3)

    def section_content(self, content):
        self.set_font('helvetica', '', 11)
        self.multi_cell(0, 6, self.safe_text(content))
        self.ln(5)

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="Pro AI Resume Builder", layout="wide")

if st.session_state.get("authentication_status") != True:
    st.error("Please login on the Home Page to use the Builder.")
    st.stop()

st.title("📝 Pro AI Resume Builder")
st.info("AI will help you refine your experience into professional bullet points.")

# Data persists even if user switches tabs temporarily
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("👤 Personal Information")
    name = st.text_input("Full Name", placeholder="Sreenandh V Nair")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    address = st.text_input("Full Address")
    
    c1, c2 = st.columns(2)
    with c1:
        dob = st.date_input("Date of Birth", value=None)
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
    with c2:
        marital = st.selectbox("Marital Status", ["Single", "Married", "Other"])

    st.subheader("💼 Work Experience")
    exp_text = st.text_area("Describe your last role (Simple words are fine)...", height=150)
    if st.button("✨ AI Improve Experience"):
        with st.spinner("Llama 3 is optimizing..."):
            improved = ai_improve_text(exp_text, "experience")
            st.session_state.improved_exp = improved
    
    final_exp = st.text_area("Final Experience Content", 
                             value=st.session_state.get('improved_exp', exp_text), height=150)

with col2:
    st.subheader("🎓 Education & Skills")
    edu = st.text_area("Education Details (e.g. B.Tech in CSE, 2025)", height=100)
    skills = st.text_area("Skills (e.g. Python, SQL, Tableau)", height=100)
    summary = st.text_area("Professional Summary (Optional)", height=100)

    # --- SAVE & GENERATE ---
    if st.button("🚀 Generate & Save Resume"):
        if not name or not email:
            st.error("Name and Email are required!")
        else:
            # Create PDF object
            pdf = ResumePDF()
            pdf.resume_name = name
            pdf.email = email
            pdf.phone = phone
            pdf.address = address
            pdf.dob = str(dob)
            pdf.gender = gender
            pdf.marital = marital
            
            pdf.add_page()
            
            if summary:
                pdf.section_title("Summary")
                pdf.section_content(summary)
            
            pdf.section_title("Professional Experience")
            pdf.section_content(final_exp)
            
            pdf.section_title("Education")
            pdf.section_content(edu)
            
            pdf.section_title("Skills")
            pdf.section_content(skills)
            
            # Save Path
            user_un = st.session_state['username']
            save_dir = f"saved_resumes/{user_un}"
            if not os.path.exists(save_dir): os.makedirs(save_dir)
            
            pdf_path = f"{save_dir}/resume.pdf"
            pdf.output(pdf_path)
            
            # Save JSON for viewing in the app
            resume_data = {
                "name": name, "email": email, "phone": phone, "address": address,
                "dob": str(dob), "gender": gender, "marital": marital,
                "exp": final_exp, "edu": edu, "skills": skills
            }
            with open(f"{save_dir}/data.json", "w") as f:
                json.dump(resume_data, f)
                
            st.success("Resume saved successfully!")
            st.download_button("📥 Download PDF", open(pdf_path, "rb"), file_name=f"{name}_Resume.pdf")

# --- 4. VIEW SAVED RESUMES ---
st.divider()
st.subheader("📂 Your Saved Resumes")
user_folder = f"saved_resumes/{st.session_state.get('username', 'guest')}"

if os.path.exists(user_folder):
    if st.button("🔍 Load My Last Saved Data"):
        with open(f"{user_folder}/data.json", "r") as f:
            saved = json.load(f)
            st.write(f"**Loaded Profile:** {saved['name']}")
            st.write(f"**Experience Sneak-Peak:** {saved['exp'][:100]}...")
            st.info("Data loaded into the input fields! You can now edit or regenerate.")
            # Note: In a real app, you'd update session_state keys here to auto-fill.
else:
    st.write("No saved resumes found yet. Generate one to see it here!")
