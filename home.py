import streamlit as st
from utils.firestore_client import get_all_users
from utils.session_manager import set_selected_user

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

users = get_all_users()
user_names = [u["name"] for u in users]

# Initialize session state key if missing
if "selected_client_name" not in st.session_state:
    st.session_state.selected_client_name = "-- Select --"

# Show selectbox with session state value
selected = st.selectbox("Select a client", options=["-- Select --"] + user_names, index=user_names.index(st.session_state.selected_client_name) if st.session_state.selected_client_name in user_names else 0)

if selected != "-- Select --":
    # Only update session state if selection changed
    if selected != st.session_state.selected_client_name:
        st.session_state.selected_client_name = selected
        user_id = next(u["id"] for u in users if u["name"] == selected)
        set_selected_user(user_id)
        st.rerun()
else:
    set_selected_user("")
    st.session_state.selected_client_name = "-- Select --"
    st.info("Please select a client to view the information.")