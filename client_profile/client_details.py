import streamlit as st
import json
from google.cloud import firestore
from google.oauth2 import service_account

# Load credentials and initialise Forestore
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="community-hackathon-2025")

# Fetch client profile
doc_ref = db.collection("client_profile").document("mdQpw2iiKZlQ6WhK4sn3")
doc = doc_ref.get()

if doc.exists:
    user_data = doc.to_dict()
    st.title("Client Details")

    # Display each field
    st.text_input("Name", user_data.get("Name", ""), disabled=True)
    st.text_input("NRIC", user_data.get("NRIC", ""), disabled=True)
    st.text_input("Date of Birth", user_data.get("Date of Birth", ""), disabled=True)
    st.text_input("Citizenship", user_data.get("Citizenship", ""), disabled=True)
    st.text_input("Gender", user_data.get("Gender", ""), disabled=True)
    st.text_input("Race", user_data.get("Race", ""), disabled=True)
    st.text_input("Religion", user_data.get("Religion", ""), disabled=True)
    st.text_input("Language", user_data.get("Language", ""), disabled=True)
    st.text_input("Marital Status", user_data.get("MaritalStatus", ""), disabled=True)
    st.text_input("Contact", str(user_data.get("Contact", "")), disabled=True)
    st.text_input("Monthly Salary", user_data.get("MonthlySalary", ""), disabled=True)
    st.text_input("Education", user_data.get("Education", ""), disabled=True)
    st.text_input("Occupation", user_data.get("Occupation", ""), disabled=True)
    st.text_input("Employment Status", user_data.get("EmploymentStatus", ""), disabled=True)
else:
    st.error("User profile not found.")