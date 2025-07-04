import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        st.button("Login", on_click=_login)
    st.markdown("""
        <style>
            .centered-title {
                text-align: center;
                padding-top: 100px;
                font-size: 45px;
                font-weight: 700;
                color: #2C3E50;
            }
            .subtitle {
                text-align: center;
                font-size: 20px;
                color: #7F8C8D;
                margin-top: 10px;
                margin-bottom: 40px;
            }
        </style>
        <div class="centered-title">Safe Shelter</div>
        <div class="subtitle">Connecting lives to a home, with dignity and care.</div>
    """, unsafe_allow_html=True)

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

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account":[home_page, logout_page],
            "Client Profile": [client_details_page, past_intervention_page, supporting_documents_page],
            "Assessment and Planning": [assessment_page, case_plan_page],
            "Collaboration": [members_page, external_correspondence_page],
            "Case Progress": [case_status_page, timeline_page]
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()