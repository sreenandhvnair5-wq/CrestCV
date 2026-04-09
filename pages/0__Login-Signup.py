import streamlit as st
import json
import os
# Temporary Debugger - Put this at the top of 0_🔐_Login.py
st.sidebar.write("### 📁 Files Found in Pages:")
if os.path.exists("pages"):
    for f in os.listdir("pages"):
        st.sidebar.code(f"pages/{f}")
# --- 1. ROBUST DATABASE LOGIC ---
DB_FILE = "users.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}}
    
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            # Ensure we always have a dictionary with a 'users' key
            if not isinstance(data, dict) or "users" not in data:
                return {"users": {}}
            return data
    except (json.JSONDecodeError, ValueError, EOFError):
        return {"users": {}}

def save_user_to_db(un, pw, name):
    db = load_db()
    
    if "users" not in db:
        db["users"] = {}
        
    if un in db["users"]:
        return False
        
    db["users"][un] = {
        "password": pw, 
        "name": name,
        "created_at": "2026-04-09"
    }
    
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)
    return True

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Member Access | CrestCV", page_icon="🔐", layout="centered")

# Initialize login states early to prevent Android refresh errors
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'display_name' not in st.session_state:
    st.session_state.display_name = ""

# --- 3. USER INTERFACE ---
st.title("🔐 Member Portal")

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Member Login", "New Account"])

    with tab1:
        with st.form("login_form"):
            u = st.text_input("Username", placeholder="Enter your username")
            p = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_login = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit_login:
                db = load_db()
                # Check if user exists and password matches
                if u in db["users"] and str(db["users"][u]["password"]) == str(p):
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.session_state.display_name = db["users"][u]["name"]
                    st.success("Login Successful!")
                    st.rerun() # Force immediate refresh to save state
                else:
                    st.error("❌ Invalid username or password.")

    with tab2:
        with st.form("signup_form"):
            new_name = st.text_input("Full Name")
            new_u = st.text_input("Choose Username")
            new_p = st.text_input("Create Password", type="password")
            submit_signup = st.form_submit_button("Create My Account", use_container_width=True)
            
            if submit_signup:
                if new_u and new_p and new_name:
                    if save_user_to_db(new_u, new_p, new_name):
                        st.success("✅ Account created! Switch to Login tab.")
                    else:
                        st.error("⚠️ Username already taken.")
                else:
                    st.warning("❗ Please fill in all details.")

else:
    # --- LOGGED IN DASHBOARD VIEW ---
    st.success(f"### Hello, {st.session_state.display_name}!")
    st.write("Welcome to your CrestCV secure profile.")
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("💡 **Ready to audit?**")
        # Ensure this filename matches your GitHub exactly
        if st.button("Open AI Analyzer", use_container_width=True):
            try:
                st.switch_page("pages/1__AI_Resume_Analyzer.py")
            except:
                st.error("Could not find Analyzer page. Check filename.")
    
    with c2:
        st.info("🛑 **Session Management**")
        if st.button("Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

    st.sidebar.success("Logged In ✅")
