import streamlit as st
from utils.firestore_client import get_user_data, get_user_doc

user_data = get_user_data("mdQpw2iiKZlQ6WhK4sn3")
doc_ref = get_user_doc("mdQpw2iiKZlQ6WhK4sn3")

# Row with Edit Toggle
header_col1, header_col2 = st.columns([0.8, 0.2])

with header_col1:
    st.title("Client Details")

with header_col2:
    edit_mode = st.toggle("Edit Mode", value=False)

# Two Columns for Profile Fields
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name", user_data.get("Name", ""), disabled=not edit_mode)
    nric = st.text_input("NRIC", user_data.get("NRIC", ""), disabled=not edit_mode)
    dob = st.text_input("Date of Birth", user_data.get("Date of Birth", ""), disabled=not edit_mode)
    gender = st.text_input("Gender", user_data.get("Gender", ""), disabled=not edit_mode)
    race = st.text_input("Race", user_data.get("Race", ""), disabled=not edit_mode)
    religion = st.text_input("Religion", user_data.get("Religion", ""), disabled=not edit_mode)
    language = st.text_input("Language", user_data.get("Language", ""), disabled=not edit_mode)

with col2:
    citizenship = st.text_input("Citizenship", user_data.get("Citizenship", ""), disabled=not edit_mode)
    marital = st.text_input("Marital Status", user_data.get("MaritalStatus", ""), disabled=not edit_mode)
    contact = st.text_input("Contact", str(user_data.get("Contact", "")), disabled=not edit_mode)
    salary = st.text_input("Monthly Salary", user_data.get("MonthlySalary", ""), disabled=not edit_mode)
    education = st.text_input("Education", user_data.get("Education", ""), disabled=not edit_mode)
    occupation = st.text_input("Occupation", user_data.get("Occupation", ""), disabled=not edit_mode)
    employment = st.text_input("Employment Status", user_data.get("EmploymentStatus", ""), disabled=not edit_mode)

# --- Save button ---
if edit_mode and st.button("Save Changes"):
    updated_data = {
        "Name": name,
        "NRIC": nric,
        "Date of Birth": dob,
        "Gender": gender,
        "Race": race,
        "Religion": religion,
        "Language": language,
        "Citizenship": citizenship,
        "MaritalStatus": marital,
        "Contact": contact,
        "MonthlySalary": salary,
        "Education": education,
        "Occupation": occupation,
        "EmploymentStatus": employment,
    }
    doc_ref.set(updated_data, merge=True)
    st.success("Profile updated!")

# Upload documents
st.subheader("")
st.markdown("### Supporting Documents")

# Load previously uploaded files from Firestore
existing_files = doc_ref.get().to_dict().get("UploadedFiles", [])

# Show existing uploaded files with delete buttons
if existing_files:
    st.write("##### Previously Uploaded Documents:")
    for file in existing_files:
        cols = st.columns([0.8, 0.2])
        with cols[0]:
            st.write(file)
        with cols[1]:
            if st.button("Delete", key=file):
                # Remove from Firestore
                updated_files = [f for f in existing_files if f != file]
                doc_ref.set({"UploadedFiles": updated_files}, merge=True)
                st.rerun()
else:
    st.info("No documents uploaded yet.")

# Initialize upload key
if "upload_key" not in st.session_state:
    st.session_state.upload_key = 0

st.write("##### Upload New Documents:")
uploaded_files = st.file_uploader(
    "Upload any supporting documents",
    type=["pdf", "docx", "png", "jpg"],
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.upload_key}"  # dynamic key
)

if uploaded_files:
    new_files = [file.name for file in uploaded_files]

    # Merge with existing files and update Firestore
    all_files = list(set(existing_files + new_files))
    doc_ref.set({"UploadedFiles": all_files}, merge=True)

    st.success(f"Uploaded {len(new_files)} new file(s).")

    # Increment key to reset uploader
    st.session_state.upload_key += 1

    # Rerun after changing key
    st.rerun()