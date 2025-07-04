import streamlit as st
from utils.session_manager import get_selected_user

def login():
    st.markdown("""
        <style>
        .centered {
            text-align: center;
            padding-top: 10px;
        }
        .title {
            font-size: 55px;
            font-weight: bold;
            color: #2C3E50;
        }
        .subtitle {
            font-size: 30px;
            color: #7F8C8D;
            margin-top: 10px;
        }
        </style>

        <div class="centered">
            <div class="title">Safe Shelter</div>
            <div class="subtitle">Connecting lives to a home, with dignity and care.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.header("")
    col1, col2 = st.columns([0.4, 0.5])
    with col2:
        st.button("Login", on_click=_login)

def _login():
    st.session_state.logged_in = True

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
home_page = st.Page("home.py", title="Home", icon=":material/home:", default=True)
client_details_page = st.Page("client_profile/client_details.py", title="Client Details", icon=":material/account_circle:")
past_intervention_page = st.Page("client_profile/past_intervention.py", title="Past Intervention", icon=":material/action_key:")
supporting_documents_page = st.Page("client_profile/supporting_documents.py", title="Supporting Documents", icon=":material/add_notes:")
assessment_page = st.Page("assessment_and_planning/assessment.py", title="Assessment", icon=":material/diagnosis:")
case_plan_page = st.Page("assessment_and_planning/case_plan.py", title="Case Plan", icon=":material/cases:")
members_page = st.Page("collaboration/members.py", title="Members", icon=":material/groups_2:")
external_correspondence_page = st.Page("collaboration/external_correspondence.py", title="External Correspondence", icon=":material/diversity_1:")
case_status_page = st.Page("case_progress/case_status.py", title="Case Status", icon=":material/app_badging:")
timeline_page = st.Page("case_progress/timeline.py", title="Timeline", icon=":material/timeline:")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    menu = {"Account": [home_page, logout_page]}

    selected_user = get_selected_user()
    if selected_user is not None and selected_user != "":
        menu.update({
            "Client Profile": [client_details_page, past_intervention_page, supporting_documents_page],
            "Assessment and Planning": [assessment_page, case_plan_page],
            "Collaboration": [members_page, external_correspondence_page],
            "Case Progress": [case_status_page, timeline_page]
        })
    
    pg = st.navigation(menu)
else:
    pg = st.navigation([login_page])

pg.run()