import os
import streamlit as st
from openai import OpenAI


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Project Roadmap Generator",
    page_icon="🗺️",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background: #0f172a;
        color: #f8fafc;
    }

    /* Main title */
    .main-title {
        text-align: center;
        padding: 20px 0 10px 0;
    }

    .main-title h1 {
        font-size: 42px;
        margin-bottom: 8px;
        background: linear-gradient(90deg, #38bdf8, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    .main-title p {
        color: #cbd5e1;
        font-size: 17px;
    }

    /* Blue information box */
    .info-box {
        background: #075985;
        border: 1px solid #0ea5e9;
        border-radius: 14px;
        padding: 20px;
        margin: 15px 0 25px 0;
        color: white;
    }

    .info-title {
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 14px;
        color: white;
    }

    .info-step {
        margin: 8px 0;
        font-size: 15px;
        line-height: 1.6;
        color: #f8fafc;
    }

    /* Result box */
    .result-box {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 22px;
        margin-top: 15px;
        color: white;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #075985 !important;
        color: white !important;
        border-color: #0ea5e9 !important;
    }

    div[data-baseweb="select"] span {
        color: white !important;
    }

    /* Input boxes */
    div[data-baseweb="input"] > div {
        background-color: #075985 !important;
        color: white !important;
        border-color: #0ea5e9 !important;
    }

    input {
        color: white !important;
    }

    /* Text areas */
    textarea {
        background-color: #075985 !important;
        color: white !important;
        border-color: #0ea5e9 !important;
    }

    textarea::placeholder,
    input::placeholder {
        color: #cbd5e1 !important;
    }

    /* Labels */
    label {
        color: #f8fafc !important;
    }

    /* Radio buttons */
    div[role="radiogroup"] label {
        color: white !important;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: none;
        padding: 11px 18px;
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8, #8b5cf6);
        color: white;
    }

    .stButton > button:hover {
        opacity: 0.9;
    }

    /* Download button */
    .stDownloadButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 700;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background: #111827;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
    }

    div[data-testid="stMetricValue"] {
        color: white !important;
    }

    /* Markdown text */
    .stMarkdown {
        color: #f8fafc;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GROQ CLIENT
# ============================================================

def get_client():

    api_key = None

    # Streamlit Cloud Secrets
    try:
        api_key = st.secrets.get("GROK_API_KEY")
    except Exception:
        pass

    # Local environment variable
    if not api_key:
        api_key = os.getenv("GROK_API_KEY")

    if not api_key:
        return None

    return OpenAI(
        api_key=api_key.strip(),
        base_url="https://api.groq.com/openai/v1"
    )


# ============================================================
# BUILD AI PROMPT
# ============================================================

def build_prompt(
    project_type,
    topic_choice,
    topic,
    level,
    total_weeks,
    weekly_hours,
    skills,
    languages,
    technologies,
    team,
    goal
):

    skills_text = ", ".join(skills)

    if not skills_text:
        skills_text = "No specific skills selected"

    if topic_choice == "Suggest a trending topic":

        topic_instruction = """
The user does not currently have a project topic.

Suggest 5 modern and relevant project ideas that match:

- Project type
- Experience level
- Current skills
- Available time
- Team size
- Project goal

Consider areas such as:

- Generative AI
- AI Agents
- Cybersecurity
- Automation
- Education Technology
- Developer Tools
- Productivity
- Intelligent Applications
- IoT
- Data Science

Then select ONE project that fits the user's requirements.

Explain why the selected project fits the user's requirements.
Do not describe it as objectively the best project.
"""

    else:

        topic_instruction = f"""
The user already selected this project:

{topic}

Use this project as the main project.

Do not replace the user's idea.

You may improve its scope and suggest practical features.
"""

    prompt = f"""

You are an expert software architect, product manager,
technical mentor, project planner, and software development advisor.

Create a COMPLETE and REALISTIC project roadmap.

============================================================
USER INFORMATION
============================================================

Project Type:
{project_type}

Topic Choice:
{topic_choice}

Project Topic:
{topic}

Experience Level:
{level}

Total Available Time:
{total_weeks} weeks

Available Hours Per Week:
{weekly_hours}

Current Skills:
{skills_text}

Programming Languages:
{languages if languages else "Not specified"}

Preferred Technologies:
{technologies if technologies else "Not specified"}

Team Size:
{team}

Main Goal:
{goal}


============================================================
TOPIC INSTRUCTIONS
============================================================

{topic_instruction}


============================================================
IMPORTANT PLANNING RULES
============================================================

1. The complete roadmap MUST fit inside {total_weeks} weeks.

2. Consider approximately {weekly_hours} hours per week.

3. Do not create an unrealistic enterprise-level project.

4. Start with an MVP.

5. Put advanced features after the MVP.

6. Reuse the user's existing skills whenever possible.

7. Clearly identify skills that the user needs to learn.

8. Estimate hours for every major phase.

9. Include milestones.

10. Include deliverables.

11. Include dependencies.

12. Include testing.

13. Include deployment.

14. Include documentation.

15. Include final presentation and demo preparation.

16. If this is an AI project, include:
    - AI model
    - API
    - Prompt engineering
    - Evaluation
    - Safety
    - Cost/quota considerations
    - RAG/embeddings when appropriate

17. If this is an IoT project, include:
    - Hardware
    - Sensors
    - Microcontroller
    - Communication
    - Firmware
    - Backend/cloud
    - Dashboard
    - Testing

18. If this is a mobile application, include:
    - UI
    - App architecture
    - Backend/API
    - Local storage
    - Authentication when appropriate
    - Testing
    - Deployment

19. If this is a web application, include:
    - Frontend
    - Backend
    - Database
    - APIs
    - Authentication when appropriate
    - Testing
    - Deployment

20. If this is a cybersecurity project, keep it defensive,
ethical, and within authorized security testing.

21. Keep the explanation understandable for a student.

22. Avoid generic advice.

23. Make the roadmap specific to the user's skills and time.

24. Do not invent statistics or fake sources.


============================================================
OUTPUT FORMAT
============================================================

# Project Roadmap

## 1. Selected Project

Project Name:

One-line Description:

Why This Project Fits the User:


## 2. Alternative Project Ideas

Give 5 alternative project ideas.

For each include:

Project:
Description:
Why it fits:


## 3. Problem and Target Users

Problem:

Target Users:

Proposed Solution:


## 4. Project Scope

Explain:

MVP:

Advanced Version:

What NOT to build initially:


## 5. Technology Stack

Create a table:

Layer | Technology | Purpose

Include relevant:

Frontend
Backend
Database
AI/API
Authentication
Deployment
Testing
Version Control


## 6. Skills Analysis

Already Useful Skills:

Skills to Learn:

Learning Priority:

Estimated Learning Time:


## 7. Feature Priority

### Must Have

List essential features.

### Should Have

List important but non-essential features.

### Could Have

List optional advanced features.


## 8. Complete Development Phases

For every phase provide:

Phase Name:

Duration:

Estimated Hours:

Tasks:

Deliverables:

Milestone:

Dependencies:


## 9. Week-by-Week Schedule

Create a detailed schedule.

For every week include:

Week:

Goal:

Tasks:

Estimated Hours:

Deliverable:

Make sure the schedule fits the user's available time.


## 10. System Architecture

Explain the complete system flow.

Example:

User
→ Frontend
→ Backend
→ Database/API
→ AI Model
→ Response
→ User


## 11. Suggested Folder Structure

Give a realistic folder structure based on
the selected technology.


## 12. Database / Data Design

Explain the required:

Tables
Collections
Files
Data structures

Only include what the project actually needs.


## 13. Testing Plan

Include:

Unit Testing

Integration Testing

UI / Usability Testing

Security Testing

Performance Testing when relevant

Final User Testing


## 14. Deployment Plan

Explain:

What should be deployed

Where it should be deployed

How the user should deploy it

Environment variables/secrets

Production checklist


## 15. Documentation

Include:

README

Installation instructions

Configuration

API documentation

Screenshots

Architecture diagram

Testing documentation

Project report


## 16. Final Presentation

Explain what the user should demonstrate.

Include:

Problem

Solution

Features

Technology

Architecture

Demo

Results

Future Improvements


## 17. GitHub / Portfolio Presentation

Explain how to present the completed project professionally.

Include:

Repository structure

README

Screenshots

Demo link

Features

Tech stack

Future improvements


## 18. Risks and Fallbacks

List realistic project risks.

For each provide:

Risk:

Impact:

Fallback:


## 19. Final Completion Checklist

Use checkboxes.

[ ] Project idea finalized
[ ] Requirements completed
[ ] UI completed
[ ] Backend completed
[ ] Database completed
[ ] AI/API integrated
[ ] Testing completed
[ ] Deployment completed
[ ] Documentation completed
[ ] GitHub repository completed
[ ] Final demo prepared


## 20. Recommended Build Order

Give the exact order the user should follow
from Day 1 until final deployment.

Make this roadmap practical, realistic,
specific, and achievable.
"""

    return prompt


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Project Requirements")

    project_type = st.selectbox(
        "What do you want to create?",
        [
            "Web App",
            "Mobile App",
            "AI / ML Project",
            "IoT Project",
            "Cybersecurity Project",
            "Data Science Project",
            "Desktop App"
        ]
    )

    topic_choice = st.radio(
        "Do you already have a project topic?",
        [
            "Suggest a trending topic",
            "I already have a topic"
        ]
    )

    if topic_choice == "I already have a topic":

        topic = st.text_input(
            "Enter your project topic",
            placeholder="Example: AI Legal Assistant"
        )

    else:

        topic = ""

    level = st.selectbox(
        "Your experience level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    total_time = st.number_input(
        "Total project time",
        min_value=1,
        max_value=104,
        value=8,
        step=1
    )

    time_unit = st.selectbox(
        "Time unit",
        [
            "Weeks",
            "Months"
        ]
    )

    weekly_hours = st.number_input(
        "Hours available per week",
        min_value=1,
        max_value=60,
        value=8,
        step=1
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
            "Generative AI",
            "AI Agents",
            "RAG",
            "Machine Learning",
            "Data Analysis",
            "Cybersecurity",
            "UI/UX",
            "Arduino",
            "ESP32",
            "Raspberry Pi"
        ]
    )

    languages = st.text_input(
        "Other programming languages",
        placeholder="Python, JavaScript, Java..."
    )

    technologies = st.text_input(
        "Preferred technologies/tools",
        placeholder="FastAPI, Firebase, Docker..."
    )

    team = st.selectbox(
        "Team size",
        [
            "Solo",
            "2 people",
            "3–5 people",
            "6+ people"
        ]
    )

    goal = st.selectbox(
        "Main project goal",
        [
            "University project",
            "Portfolio project",
            "Final Year Project",
            "Startup / Product",
            "Hackathon",
            "Learn new skills"
        ]
    )


# ============================================================
# MAIN PAGE
# ============================================================

st.markdown(
    """
    <div class="main-title">
        <h1>🗺️ AI Project Roadmap Generator</h1>

        <p>
        Turn your skills, available time, and project idea
        into a complete development roadmap.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown(
    """
    <div class="info-box">

        <div class="info-title">
            💡 How It Works
        </div>

        <div class="info-step">
            1. Choose the type of project you want to build.
        </div>

        <div class="info-step">
            2. Enter your experience and current skills.
        </div>

        <div class="info-step">
            3. Tell the AI how much time you have.
        </div>

        <div class="info-step">
            4. Enter your own idea or let AI suggest project ideas.
        </div>

        <div class="info-step">
            5. Get a complete roadmap from idea → development → testing → deployment.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROJECT SUMMARY
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Project Type",
        project_type
    )

with col2:

    st.metric(
        "Experience",
        level
    )

with col3:

    st.metric(
        "Weekly Hours",
        f"{weekly_hours} hrs"
    )


# ============================================================
# GENERATE ROADMAP
# ============================================================

st.markdown("### 🚀 Generate Your Roadmap")

generate = st.button(
    "✨ Generate Complete Roadmap"
)


if generate:

    # --------------------------------------------------------
    # Validate topic
    # --------------------------------------------------------

    if topic_choice == "I already have a topic" and not topic.strip():

        st.warning(
            "Please enter your project topic."
        )

        st.stop()


    # --------------------------------------------------------
    # Get API client
    # --------------------------------------------------------

    client = get_client()

    if client is None:

        st.error(
            "GROK_API_KEY was not found. "
            "Please add your Groq API key to Streamlit Secrets."
        )

        st.stop()


    # --------------------------------------------------------
    # Convert time to weeks
    # --------------------------------------------------------

    if time_unit == "Weeks":

        total_weeks = total_time

    else:

        total_weeks = total_time * 4


    # --------------------------------------------------------
    # Build prompt
    # --------------------------------------------------------

    prompt = build_prompt(
        project_type=project_type,
        topic_choice=topic_choice,
        topic=topic.strip(),
        level=level,
        total_weeks=total_weeks,
        weekly_hours=weekly_hours,
        skills=skills,
        languages=languages,
        technologies=technologies,
        team=team,
        goal=goal
    )


    # --------------------------------------------------------
    # Call Groq
    # --------------------------------------------------------

    with st.spinner(
        "🤖 Groq AI is creating your personalized roadmap..."
    ):

        try:

            response = client.chat.completions.create(

                model="openai/gpt-oss-120b",

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert software project "
                            "architect and technical mentor. "
                            "Create realistic project plans that "
                            "fit the user's available time and skills."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.4,

                max_tokens=12000
            )


            # ------------------------------------------------
            # Get response
            # ------------------------------------------------

            roadmap = response.choices[0].message.content


            if not roadmap:

                st.error(
                    "The AI returned an empty response."
                )

                st.stop()


            # ------------------------------------------------
            # Save roadmap
            # ------------------------------------------------

            st.session_state["roadmap"] = roadmap


        except Exception as error:

            st.error(
                "The roadmap could not be generated."
            )

            st.code(
                str(error)
            )


# ============================================================
# DISPLAY ROADMAP
# ============================================================

if "roadmap" in st.session_state:

    st.markdown("---")

    st.markdown(
        "## 📋 Your Personalized Project Roadmap"
    )

    st.markdown(
        '<div class="result-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        st.session_state["roadmap"]
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    st.download_button(
        "⬇️ Download Roadmap",
        data=st.session_state["roadmap"],
        file_name="project_roadmap.md",
        mime="text/markdown"
    )


# ============================================================
# DEFAULT EXAMPLES
# ============================================================

else:

    st.markdown("### 💡 Example Project Ideas")

    st.markdown(
        """
        <div class="info-box">

        <div class="info-step">
        🤖 AI Study Planner
        </div>

        <div class="info-step">
        ⚖️ AI Legal Assistant
        </div>

        <div class="info-step">
        🛡️ Cybersecurity Threat Analyzer
        </div>

        <div class="info-step">
        ✉️ AI Email Generator
        </div>

        <div class="info-step">
        🏠 Smart Home IoT System
        </div>

        <div class="info-step">
        🎓 Student Complaint Management System
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )
