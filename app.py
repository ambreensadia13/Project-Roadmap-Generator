import os
import re
import streamlit as st
from openai import OpenAI

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Project Roadmap Generator",
    page_icon="🗺️",
    layout="wide",
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #0f172a;
        color: #f8fafc;
    }

    .main-title {
        text-align: center;
        padding: 20px 0 5px 0;
    }

    .main-title h1 {
        font-size: 42px;
        margin-bottom: 5px;
        background: linear-gradient(90deg, #38bdf8, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .main-title p {
        color: #cbd5e1;
        font-size: 17px;
    }

    .info-box {
        background: #075985;
        border: 1px solid #0ea5e9;
        border-radius: 14px;
        padding: 16px;
        margin: 10px 0 18px 0;
    }

    .roadmap-card {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 20px;
        margin: 12px 0;
    }

    .step {
        background: #0b2940;
        border-left: 4px solid #38bdf8;
        border-radius: 8px;
        padding: 12px 15px;
        margin: 8px 0;
    }

    .small-note {
        color: #94a3b8;
        font-size: 13px;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    textarea {
        background-color: #075985 !important;
        color: white !important;
    }

    div[data-baseweb="select"] span {
        color: white !important;
    }

    label, .stMarkdown, .stTextInput label, .stSelectbox label,
    .stNumberInput label, .stMultiSelect label, .stTextArea label {
        color: #f8fafc !important;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 0;
        padding: 10px 18px;
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8, #8b5cf6);
        color: white;
    }

    .stDownloadButton > button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# GROK CLIENT
# ============================================================

def get_client():
    api_key = None

    # Streamlit Cloud: add GROK_API_KEY in Secrets.
    try:
        api_key = st.secrets.get("GROK_API_KEY")
    except Exception:
        pass

    # Local fallback.
    api_key = api_key or os.getenv("GROK_API_KEY")

    if not api_key:
        return None

    return OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
    )


def clean_markdown(text):
    """Keep the generated roadmap readable in Streamlit."""
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\r\n", "\n")
    return text.strip()


# ============================================================
# PROMPT
# ============================================================

def build_prompt(data):
    skills = ", ".join(data["skills"]) if data["skills"] else "Not specified"

    return f"""
You are an expert software project architect, product strategist,
technical mentor, and project manager.

Create a realistic, detailed project roadmap for a student/developer.

USER PROFILE
------------
Project type: {data["project_type"]}
Preferred domain/topic: {data["topic"]}
Experience level: {data["level"]}
Available time: {data["time_value"]} {data["time_unit"]}
Weekly hours: {data["weekly_hours"]}
Current skills: {skills}
Programming languages: {data["languages"]}
Preferred technologies: {data["technologies"]}
Team: {data["team"]}
Goal: {data["goal"]}

IMPORTANT REQUIREMENTS
----------------------
1. If the user selected "Suggest a trending topic", first suggest 5
   current project ideas relevant to the selected project type, skills,
   and experience. Then choose ONE suitable idea and explain why it
   fits the user's constraints. Do not claim an idea is objectively
   "the best"; explain the fit.
2. If the user entered a preferred topic, use it as the main project.
3. Do not create a plan that obviously exceeds the user's available time.
4. Prioritize an MVP first, then optional advanced features.
5. Use the user's existing skills where possible, and identify only the
   additional skills they need to learn.
6. Give a practical week-by-week or phase-by-phase schedule.
7. Include estimated hours for each phase and keep the total realistic.
8. Include milestones, deliverables, dependencies, testing, deployment,
   documentation, and final presentation/demo preparation.
9. Include a technology stack with frontend, backend, database,
   APIs/AI, deployment, testing, and version control where relevant.
10. For AI projects, include model/API, prompting, RAG/embeddings,
    evaluation, safety, and cost/quota considerations where relevant.
11. For IoT projects, include hardware, sensors, communication protocol,
    firmware, backend/cloud, dashboard, and testing where relevant.
12. For mobile projects, include UI, app architecture, API/backend,
    local storage, testing, and deployment.
13. For web apps, include UI, frontend, backend, database/API,
    authentication if relevant, testing, and deployment.
14. Include a realistic folder/project structure.
15. Include a feature priority table:
    Must Have / Should Have / Could Have.
16. Include risks and fallback alternatives.
17. Include a "What to learn" section ordered by priority.
18. Include a final completion checklist.
19. Keep the language clear and practical for a student.
20. Do not use fake sources, fake statistics, or unsupported claims.

OUTPUT FORMAT
-------------
# Project Roadmap

## 1. Project Selected
Name:
One-line description:
Why it fits the user's time and skills:

## 2. Alternative Topic Ideas
Give 5 alternatives with one-line descriptions.

## 3. Project Scope
Problem:
Target users:
Core solution:
MVP:
Advanced version:

## 4. Technology Stack
Use a table.

## 5. Skills Gap
Already useful skills:
Skills to learn:
Priority order:

## 6. Features
Use Must Have / Should Have / Could Have.

## 7. Complete Roadmap
Create sequential phases.
For each phase include:
- Duration
- Estimated hours
- Tasks
- Deliverables
- Milestone

## 8. Detailed Weekly Schedule
Create a realistic schedule based on the user's total time
and weekly hours.

## 9. Project Architecture
Explain the system flow simply.

## 10. Suggested Folder Structure
Give a clean code/project structure.

## 11. Testing Plan
Unit testing, integration testing, usability testing,
security/testing relevant to the project.

## 12. Deployment Plan
Explain exactly what should be deployed and where,
using practical student-friendly options.

## 13. Documentation & Presentation
README, screenshots, demo, report, presentation, and portfolio.

## 14. Risks & Fallbacks
List major risks and practical alternatives.

## 15. Final Checklist
A concise checkbox-style list.

Make the plan specific rather than generic.
"""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("⚙️ Project Inputs")

    project_type = st.selectbox(
        "What do you want to create?",
        [
            "Web App",
            "Mobile App",
            "AI / ML Project",
            "IoT Project",
            "Desktop App",
            "Cybersecurity Project",
            "Data Science Project",
        ],
    )

    topic_choice = st.radio(
        "Project topic",
        [
            "Suggest a trending topic",
            "I already have a topic",
        ],
    )

    if topic_choice == "I already have a topic":
        topic = st.text_input(
            "Enter your project idea",
            placeholder="e.g. AI legal assistant",
        )
    else:
        topic = "Suggest a trending topic"

    level = st.selectbox(
        "Experience level",
        ["Beginner", "Intermediate", "Advanced"],
    )

    time_value = st.number_input(
        "How much total time do you have?",
        min_value=1,
        max_value=104,
        value=8,
        step=1,
    )

    time_unit = st.selectbox(
        "Time unit",
        ["Weeks", "Months"],
    )

    weekly_hours = st.number_input(
        "Hours available per week",
        min_value=1,
        max_value=60,
        value=8,
        step=1,
    )

    skills = st.multiselect(
        "Your current skills",
        [
            "Python",
            "C++",
            "Java",
            "JavaScript",
            "HTML",
            "CSS",
            "React",
            "Node.js",
            "Streamlit",
            "FastAPI",
            "Flask",
            "Django",
            "SQL",
            "MongoDB",
            "Firebase",
            "Git / GitHub",
            "AI / Generative AI",
            "RAG",
            "Machine Learning",
            "Data Analysis",
            "Cybersecurity",
            "UI/UX",
            "Arduino",
            "ESP32",
            "Raspberry Pi",
        ],
    )

    languages = st.text_input(
        "Other programming languages",
        placeholder="e.g. Python, JavaScript",
    )

    technologies = st.text_input(
        "Preferred technologies/tools",
        placeholder="e.g. Streamlit, FastAPI, Firebase",
    )

    team = st.selectbox(
        "Team size",
        ["Solo", "2 people", "3–5 people", "6+ people"],
    )

    goal = st.selectbox(
        "Main goal",
        [
            "University project",
            "Portfolio project",
            "Final Year Project",
            "Startup / product idea",
            "Hackathon",
            "Learn new skills",
        ],
    )

# ============================================================
# MAIN UI
# ============================================================

st.markdown(
    """
    <div class="main-title">
        <h1>🗺️ Project Roadmap Generator</h1>
        <p>Answer a few questions and generate a realistic project plan
        around your time, skills, and goals.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="info-box">
        <b>How it works:</b><br>
        1. Choose what you want to build.<br>
        2. Tell the app your skills and available time.<br>
        3. Let AI suggest a project topic or enter your own.<br>
        4. Get a complete roadmap from idea → development → testing → deployment → presentation.
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Project Type", project_type)

with col2:
    st.metric("Experience", level)

with col3:
    st.metric("Weekly Hours", f"{weekly_hours}h")

st.markdown("### 🚀 Generate Your Roadmap")

generate = st.button("✨ Generate Complete Roadmap")

if generate:
    if topic_choice == "I already have a topic" and not topic.strip():
        st.warning("Please enter your project idea.")
        st.stop()

    client = get_client()

    if client is None:
        st.error(
            "Grok API key not found. Add GROK_API_KEY to Streamlit "
            "Secrets or set it as an environment variable."
        )
        st.stop()

    total_weeks = (
        time_value
        if time_unit == "Weeks"
        else time_value * 4
    )

    data = {
        "project_type": project_type,
        "topic": topic.strip(),
        "level": level,
        "time_value": total_weeks,
        "time_unit": "Weeks",
        "weekly_hours": weekly_hours,
        "skills": skills,
        "languages": languages or "Not specified",
        "technologies": technologies or "Not specified",
        "team": team,
        "goal": goal,
    }

    prompt = build_prompt(data)

    with st.spinner("Building your personalized roadmap..."):
        try:
            response = client.chat.completions.create(
                model="grok-4-fast",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You create realistic software project "
                            "roadmaps. Be practical, specific, and "
                            "time-aware."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.5,
                max_tokens=7000,
            )

            roadmap = response.choices[0].message.content
            roadmap = clean_markdown(roadmap)

            st.session_state["roadmap"] = roadmap
            st.session_state["project_type"] = project_type

        except Exception as e:
            st.error(
                "Could not generate the roadmap. Check your Grok API key, "
                "model name, quota, and connection."
            )
            st.code(str(e))

# ============================================================
# ROADMAP OUTPUT
# ============================================================

if "roadmap" in st.session_state:
    st.markdown("---")
    st.markdown("## 📋 Your Personalized Roadmap")

    st.markdown(
        '<div class="roadmap-card">',
        unsafe_allow_html=True,
    )

    st.markdown(st.session_state["roadmap"])

    st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        "⬇️ Download Roadmap as TXT",
        data=st.session_state["roadmap"],
        file_name="project_roadmap.txt",
        mime="text/plain",
    )

    st.markdown(
        '<p class="small-note">'
        "Tip: Build the MVP first. Treat advanced features as optional "
        "until the core project works."
        "</p>",
        unsafe_allow_html=True,
    )
else:
    st.markdown("### 💡 Example Inputs")
    st.write(
        "AI legal assistant • Cybersecurity threat analyzer • "
        "AI study planner • Smart home IoT system • "
        "AI email generator • Health/fitness tracker • "
        "Student complaint management system"
    )
