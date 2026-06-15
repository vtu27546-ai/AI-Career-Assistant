
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os
from PyPDF2 import PdfReader
from docx import Document
from reportlab.pdfgen import canvas
import pyttsx3
import threading

# AUTH IMPORT
from auth import login_register_ui

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================================================
# LOGIN CHECK
# =========================================================

if not st.session_state.logged_in:

    login_register_ui()

    st.stop()

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# =========================================================
# VOICE ASSISTANT
# =========================================================

def speak(text):

    def run_voice():

        try:

            engine = pyttsx3.init()

            voices = engine.getProperty('voices')

            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id)

            engine.setProperty('rate', 155)

            engine.setProperty('volume', 0.9)

            engine.say(text)

            engine.runAndWait()

            engine.stop()

        except Exception as e:

            print(e)

    threading.Thread(target=run_voice).start()

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Career Assistant Platform",
    page_icon="🚀",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.stButton>button {
    background-color: #00ADB5;
    color: white;
    border-radius: 12px;
    height: 50px;
    width: 250px;
    font-size: 18px;
    border: none;
    font-weight: bold;
}

.skill-box {
    background-color: #1F2937;
    padding: 15px;
    border-radius: 12px;
    margin: 5px;
    font-size: 18px;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGOUT BUTTON
# =========================================================

col1, col2 = st.columns([8,1])

with col2:

    if st.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()

# =========================================================
# TITLE
# =========================================================

st.title("🚀 AI Career Assistant Platform")

st.success(
    f"Welcome {st.session_state.user_name}"
)

st.info(
    "ATS Analyzer + Resume Builder + AI Interview Coach + AI Career Mentor"
)

# =========================================================
# WELCOME VOICE
# =========================================================

if "welcome_done" not in st.session_state:

    speak(
        "Welcome to the AI Career Assistant Platform"
    )

    st.session_state.welcome_done = True

# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf", "docx"]
)

# =========================================================
# JOB DESCRIPTION
# =========================================================

job_description = st.text_area(
    "📋 Paste Job Description",
    height=250
)

# =========================================================
# EXTRACT RESUME TEXT
# =========================================================

resume_text = ""

if uploaded_file:

    if uploaded_file.name.endswith(".pdf"):

        pdf_reader = PdfReader(uploaded_file)

        for page in pdf_reader.pages:

            text = page.extract_text()

            if text:
                resume_text += text

    elif uploaded_file.name.endswith(".docx"):

        doc = Document(uploaded_file)

        for para in doc.paragraphs:
            resume_text += para.text + "\n"

# =========================================================
# USER NAME
# =========================================================

user_name = st.session_state.user_name

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 ATS Analysis",
    "📄 Modified Resume",
    "🎤 Interview Questions",
    "🤖 Personal AI Assistant",
    "📄 Cover Letter Generator"
])

# =========================================================
# ATS ANALYSIS
# =========================================================

with tab1:

    if st.button("Analyze Resume"):

        if uploaded_file and job_description:

            try:

                with st.spinner("Analyzing Resume..."):

                    skills_database = [
                        "python",
                        "sql",
                        "machine learning",
                        "data analysis",
                        "communication",
                        "problem solving",
                        "docker",
                        "aws",
                        "kubernetes",
                        "flask",
                        "django",
                        "react",
                        "streamlit",
                        "openai",
                        "api",
                        "html",
                        "css",
                        "javascript",
                        "git",
                        "github",
                        "pandas",
                        "numpy",
                        "tensorflow",
                        "deep learning",
                        "nlp",
                        "power bi",
                        "excel",
                        "java",
                        "c++",
                        "mongodb"
                    ]

                    resume_lower = resume_text.lower()
                    jd_lower = job_description.lower()

                    matching_skills = []
                    missing_skills = []

                    for skill in skills_database:

                        if skill in resume_lower and skill in jd_lower:
                            matching_skills.append(skill.title())

                        elif skill in jd_lower and skill not in resume_lower:
                            missing_skills.append(skill.title())

                    total_required = len(matching_skills) + len(missing_skills)

                    if total_required > 0:

                        ats_score = int(
                            (len(matching_skills) / total_required) * 100
                        )

                    else:

                        ats_score = 50

                    prompt = f"""
                    Analyze the resume professionally.

                    Resume:
                    {resume_text}

                    Job Description:
                    {job_description}
                    """

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a professional ATS resume expert."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    result = response.choices[0].message.content

                st.subheader("📊 ATS Score")

                st.progress(ats_score / 100)

                st.success(f"ATS Score: {ats_score}%")

                st.subheader("✅ Matching Skills")

                for skill in matching_skills:
                    st.success(skill)

                st.subheader("❌ Missing Skills")

                for skill in missing_skills:
                    st.error(skill)

                st.subheader("📋 AI Suggestions")

                st.write(result)

            except Exception as e:

                st.error(f"Error: {e}")

        else:

            st.error(
                "Please upload resume and paste job description."
            )

