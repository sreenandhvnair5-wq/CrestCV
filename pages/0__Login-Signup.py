import streamlit as st
import json
import os

# --- 1. DATABASE LOGIC ---
DB_FILE = "users.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_user_to_db(un, pw, name):
    db = load_db()
    if un in db["users"]:
        return False
    db["users"][un] = {"password": pw, "name": name}
    with open(DB_FILE, "w") as f:
        json.dump(db, f)
    return True

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Login | CrestCV", page_icon="🔐")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- 3. UI ---
st.title("🔐 Member Access")

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:
        with st.form("login_form"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                db = load_db()
                if u in db["users"] and db["users"][u]["password"] == p:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.session_state.display_name = db["users"][u]["name"]
                    st.success(f"Welcome back, {st.session_state.display_name}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

    with tab2:
        with st.form("signup_form"):
            new_name = st.text_input("Full Name")
            new_u = st.text_input("Choose Username")
            new_p = st.text_input("Choose Password", type="password")
            if st.form_submit_button("Register", use_container_width=True):
                if new_u and new_p and new_name:
                    if save_user_to_db(new_u, new_p, new_name):
                        st.success("Account created! You can now login.")
                    else:
                        st.error("Username already exists.")
                else:
                    st.warning("Please fill all fields.")
else:
    # LOGGED IN STATE
    st.success(f"Successfully logged in as **{st.session_state.display_name}**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Go to AI Analyzer", use_container_width=True):
            st.switch_page("pages/1_🔍_AI_Analyzer.py")
    with col2:
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

    st.divider()
    st.info("Your resume data and history are now being synced to your profile.")
