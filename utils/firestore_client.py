import json
from google.cloud import firestore
from google.oauth2 import service_account
import streamlit as st

def get_firestore_client():
    if "firestore_client" not in st.session_state:
        key_dict = json.loads(st.secrets["textkey"])
        creds = service_account.Credentials.from_service_account_info(key_dict)
        st.session_state.firestore_client = firestore.Client(credentials=creds, project="community-hackathon-2025")
    return st.session_state.firestore_client

def get_all_users():
    db = get_firestore_client()
    users = db.collection("client_profile").stream()
    user_list = []
    for doc in users:
        data = doc.to_dict()
        user_list.append({"id": doc.id, "name": data.get("Name", "No Name")})
    return user_list

def get_user_data(user_id):
    db = get_firestore_client()
    doc = db.collection("client_profile").document(user_id).get()
    if doc.exists:
        return doc.to_dict()
    return None

def get_user_doc(user_id):
    db = get_firestore_client()
    doc = db.collection("client_profile").document(user_id)
    return doc
