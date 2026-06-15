
import sqlite3
import streamlit as st
import hashlib

# =========================================================
# DATABASE CONNECTION
# =========================================================

conn = sqlite3.connect("users.db", check_same_thread=False)

cursor = conn.cursor()

# =========================================================
# CREATE USERS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

[data-testid="stSidebar"] {
    display: none;
}

.main {
    background: linear-gradient(to right, #0f172a, #020617);
    color: white;
}

.login-container {

    background-color: #111827;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0px 0px 20px rgba(0,255,255,0.2);
    margin-top: 50px;
}

.stTextInput>div>div>input {

    background-color: #1f2937;
    color: white;
    border-radius: 10px;
}

.stButton>button {

    width: 100%;
    background: linear-gradient(to right, #06b6d4, #3b82f6);
    color: white;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.title {

    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #38bdf8;
}

.subtitle {

    text-align: center;
    font-size: 18px;
    color: #cbd5e1;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# REGISTER USER
# =========================================================

def register_user(name, email, password):

    try:

        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (
                name,
                email,
                hashed_password
            )
        )

        conn.commit()

        return True

    except Exception as e:

        print(e)

        return False

# =========================================================
# LOGIN USER
# =========================================================

def login_user(email, password):

    hashed_password = hashlib.sha256(
        password.encode()
    ).hexdigest()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (
            email,
            hashed_password
        )
    )

    user = cursor.fetchone()

    return user

# =========================================================
# LOGIN / REGISTER UI
# =========================================================

def login_register_ui():

    st.markdown(
        "<div class='title'>🚀 AI Career Assistant</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>AI Powered ATS Resume Analyzer & Career Mentor</div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("<div class='login-container'>", unsafe_allow_html=True)

        option = st.radio(
            "Select Option",
            ["Login", "Register"],
            horizontal=True
        )

        # LOGIN
        if option == "Login":

            st.subheader("🔐 Login")

            email = st.text_input("Email")

            password = st.text_input(
                "Password",
                type="password"
            )

            if st.button("Login"):

                user = login_user(email, password)

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user_name = user[1]

                    st.success(f"Welcome {user[1]}")

                    st.rerun()

                else:

                    st.error("Invalid Email or Password")

        # REGISTER
        else:

            st.subheader("📝 Create Account")

            name = st.text_input("Full Name")

            email = st.text_input("Email Address")

            password = st.text_input(
                "Create Password",
                type="password"
            )

            if st.button("Create Account"):

                if len(password) < 8:

                    st.error(
                        "Password must contain minimum 8 characters"
                    )

                else:

                    success = register_user(
                        name,
                        email,
                        password
                    )

                    if success:

                        st.success(
                            "✅ Account Created Successfully"
                        )

                        st.info(
                            "Now Login using your credentials."
                        )

                    else:

                        st.error(
                            "⚠ Email already exists"
                        )

        st.markdown("</div>", unsafe_allow_html=True)

