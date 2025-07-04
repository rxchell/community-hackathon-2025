import streamlit as st

def set_selected_user(user_id):
    st.session_state.selected_user_id = user_id

def get_selected_user():
    return st.session_state.get("selected_user_id", "")

def clear_selected_user():
    if "selected_user_id" in st.session_state:
        del st.session_state["selected_user_id"]
