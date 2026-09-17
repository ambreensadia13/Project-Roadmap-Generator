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

    /* ======================================================
       APP BACKGROUND
       ====================================================== */

    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }


    /* ======================================================
       INPUT BOXES
       ====================================================== */

    div[data-baseweb="select"] > div {
        background-color: #075985 !important;
        border: 1px solid #0ea5e9 !important;
        color: white !important;
    }

    div[data-baseweb="select"] span {
        color: white !important;
    }

    div[data-baseweb="input"] > div {
        background-color: #075985 !important;
        border: 1px solid #0ea5e9 !important;
        color: white !important;
    }

    input {
        color: white !important;
    }

    textarea {
        background-color: #075985 !important;
        color: white !important;
        border: 1px solid #0ea5e9 !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #cbd5e1 !important;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 10px;
        border: none;
        font-weight: 700;
        color: white;
        background: linear-gradient(
            90deg,
            #38bdf8,
            #8b5cf6
        );
    }

    .stButton > button:hover {
        opacity: 0.9;
    }


    /* ======================================================
       DOWNLOAD BUTTON
       ====================================================== */

    .stDownloadButton > button {
        width: 100%;
        min-height: 45px;
        border-radius: 10px;
        font-weight: 700;
    }


    /* ======================================================
       METRIC BOXES
       ====================================================== */

    div[data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 15px;
    }

    div[data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
    }

    div[data-testid="stMetricValue"] {
        color: white !important;
    }


    /* ======================================================
       RADIO BUTTONS
       ====================================================== */

    div[role="radiogroup"] label {
        color: white !important;
    }


    /* ======================================================
       GENERAL TEXT
       ====================================================== */

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

    # --------------------------------------------------------
    # Streamlit Cloud Secrets
    # --------------------------------------------------------

    try:
        api_key = st.secrets.get("GROK_API_KEY")
    except Exception:
        pass

    # --------------------------------------------------------
    # Local environment variable
    # --------------------------------------------------------

    if not api_key:
        api_key = os.getenv("GROK_API_KEY")

    # --------------------------------------------------------
    # No key
    # --------------------------------------------------------

    if not api_key:
        return None

    # --------------------------------------------------------
    # Groq client
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    if skills:

        skills_text = ", ".join(skills)

    else:

        skills_text = "No specific skills selected"


    # --------------------------------------------------------
    # Topic instruction
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Full prompt
    # --------------------------------------------------------

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
{topic if topic else "No topic provided"}

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

4. Start with a realistic MVP.

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
    - Cost and quota considerations
    - RAG and embeddings when appropriate

17. If this is an IoT project, include:

    - Hardware
    - Sensors
    - Microcontroller
    - Communication
    - Firmware
    - Backend or cloud
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

Environment variables and secrets

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

    # --------------------------------------------------------
    # Project type
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Topic choice
    # --------------------------------------------------------

    topic_choice = st.radio(
        "Do you already have a project topic?",
        [
            "Suggest a trending topic",
            "I already have a topic"
        ]
    )


    # --------------------------------------------------------
    # Topic input
    # --------------------------------------------------------

    if topic_choice == "I already have a topic":

        topic = st.text_input(
            "Enter your project topic",
            placeholder="Example: AI Legal Assistant"
        )

    else:

        topic = ""


    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    level = st.selectbox(
        "Your experience level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


    # --------------------------------------------------------
    # Total time
    # --------------------------------------------------------

    total_time = st.number_input(
        "Total project time",
        min_value=1,
        max_value=104,
        value=8,
        step=1
    )


    # --------------------------------------------------------
    # Time unit
    # --------------------------------------------------------

    time_unit = st.selectbox(
        "Time unit",
        [
            "Weeks",
            "Months"
        ]
    )


    # --------------------------------------------------------
    # Weekly hours
    # --------------------------------------------------------

    weekly_hours = st.number_input(
        "Hours available per week",
        min_value=1,
        max_value=60,
        value=8,
        step=1
    )


    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Other languages
    # --------------------------------------------------------

    languages = st.text_input(
        "Other programming languages",
        placeholder="Python, JavaScript, Java..."
    )


    # --------------------------------------------------------
    # Technologies
    # --------------------------------------------------------

    technologies = st.text_input(
        "Preferred technologies/tools",
        placeholder="FastAPI, Firebase, Docker..."
    )


    # --------------------------------------------------------
    # Team
    # --------------------------------------------------------

    team = st.selectbox(
        "Team size",
        [
            "Solo",
            "2 people",
            "3–5 people",
            "6+ people"
        ]
    )


    # --------------------------------------------------------
    # Goal
    # --------------------------------------------------------

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
# MAIN TITLE
# ============================================================

st.title("🗺️ AI Project Roadmap Generator")

st.write(
    "Turn your skills, available time, and project idea "
    "into a complete development roadmap."
)


# ============================================================
# HOW IT WORKS
# ============================================================

st.info(
    """
    💡 **How It Works**

    **1.** Choose the type of project you want to build.

    **2.** Enter your experience and current skills.

    **3.** Tell the AI how much time you have.

    **4.** Enter your own idea or let AI suggest project ideas.

    **5.** Get a complete roadmap from idea → development → testing → deployment.
    """
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
# GENERATE SECTION
# ============================================================

st.subheader("🚀 Generate Your Roadmap")


generate = st.button(
    "✨ Generate Complete Roadmap"
)


# ============================================================
# GENERATION
# ============================================================

if generate:

    # --------------------------------------------------------
    # Validate topic
    # --------------------------------------------------------

    if topic_choice == "I already have a topic":

        if not topic.strip():

            st.warning(
                "Please enter your project topic."
            )

            st.stop()


    # --------------------------------------------------------
    # Get Groq client
    # --------------------------------------------------------

    client = get_client()


    if client is None:

        st.error(
            "GROK_API_KEY was not found."
        )

        st.info(
            "Add your Groq API key to Streamlit Secrets "
            "using the name GROK_API_KEY."
        )

        st.stop()


    # --------------------------------------------------------
    # Convert months to weeks
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
            # Extract response
            # ------------------------------------------------

            roadmap = response.choices[0].message.content


            if not roadmap:

                st.error(
                    "The AI returned an empty response."
                )

                st.stop()


            # ------------------------------------------------
            # Save response
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

    st.divider()

    st.subheader(
        "📋 Your Personalized Project Roadmap"
    )

    st.markdown(
        st.session_state["roadmap"]
    )


    # --------------------------------------------------------
    # Download roadmap
    # --------------------------------------------------------

    st.download_button(
        label="⬇️ Download Roadmap",
        data=st.session_state["roadmap"],
        file_name="project_roadmap.md",
        mime="text/markdown"
    )


# ============================================================
# EXAMPLE PROJECTS
# ============================================================

else:

    st.subheader("💡 Example Project Ideas")

    example_projects = [
        "🤖 AI Study Planner",
        "⚖️ AI Legal Assistant",
        "🛡️ Cybersecurity Threat Analyzer",
        "✉️ AI Email Generator",
        "🏠 Smart Home IoT System",
        "🎓 Student Complaint Management System"
    ]

    for project in example_projects:

        st.write(project)
