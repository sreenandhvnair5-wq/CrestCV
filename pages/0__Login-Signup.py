import streamlit as st
import json
import os

# --- 1. ROBUST DATABASE LOGIC ---
DB_FILE = "users.json"

def load_db():
    # Scenario A: File doesn't exist
    if not os.path.exists(DB_FILE):
        return {"users": {}}
    
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            # Scenario B: File exists but is empty or missing the 'users' key
            if not isinstance(data, dict) or "users" not in data:
                return {"users": {}}
            return data
    except (json.JSONDecodeError, ValueError, EOFError):
        # Scenario C: File is corrupted or unreadable
        return {"users": {}}

def save_user_to_db(un, pw, name):
    db = load_db()
    
    # Ensure the "users" key exists before we check it
    if "users" not in db:
        db["users"] = {}
        
    # Check if username already exists
    if un in db["users"]:
        return False
        
    # Add new user data
    db["users"][un] = {
        "password": pw, 
        "name": name,
        "created_at": str(st.session_state.get('login_time', '2026-04-09'))
    }
    
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)
    return True

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Member Access | CrestCV", page_icon="🔐", layout="centered")

# Initialize login states
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# --- 3. USER INTERFACE ---
st.title("🔐 Member Portal")
st.write("Join the CrestCV community to unlock advanced AI features.")

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Member Login", "New Account"])

    with tab1:
        with st.form("login_form"):
            u = st.text_input("Username", placeholder="Enter your username")
            p = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_login = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit_login:
                db = load_db()
                if u in db["users"] and db["users"][u]["password"] == p:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.session_state.display_name = db["users"][u]["name"]
                    st.success(f"Welcome back, {st.session_state.display_name}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password. Please try again.")

    with tab2:
        with st.form("signup_form"):
            new_name = st.text_input("Full Name", placeholder="e.g. Sreenandh V Nair")
            new_u = st.text_input("Choose Username", placeholder="e.g. sreenandh_dev")
            new_p = st.text_input("Create Password", type="password", placeholder="Minimum 6 characters")
            submit_signup = st.form_submit_button("Create My Account", use_container_width=True)
            
            if submit_signup:
                if new_u and new_p and new_name:
                    if save_user_to_db(new_u, new_p, new_name):
                        st.success("✅ Account created successfully! Please switch to the Login tab.")
                    else:
                        st.error("⚠️ That username is already taken. Try another one.")
                else:
                    st.warning("❗ Please fill in all the details to register.")

else:
    # --- LOGGED IN DASHBOARD VIEW ---
    st.balloons()
    st.success(f"### Hello, {st.session_state.display_name}!")
    st.write("You are now logged into your CrestCV secure profile.")
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("💡 **Ready to audit?**")
        if st.button("Open AI Analyzer", use_container_width=True):
            st.switch_page("pages/1_🔍_AI_Analyzer.py")
    
    with c2:
        st.info("🛑 **Session Management**")
        if st.button("Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

    st.sidebar.success("Logged In ✅")
    st.sidebar.write(f"Account: {st.session_state.username}")
