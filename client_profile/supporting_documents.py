import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
import docx
import io
from openai import OpenAI

# Initialize OpenAI
client = OpenAI(api_key = st.secrets["openai"]["OPENAI_API_KEY"])

# Extract text with OCR
def extract_text(file, filetype):
    if filetype == "application/pdf":
        images = convert_from_bytes(file.read())
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)
        return text
    elif filetype.startswith("image/"):
        image = file.read()
        return pytesseract.image_to_string(io.BytesIO(image))
    elif filetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return "Unsupported file type"

# Generate summary with OpenAI LLM 
def generate_summary(text, doc_type):
    prompt = f"""
    You are an assistant for social workers at a transitional shelter.
    Summarize the following {doc_type} based on key assessment criteria including:
    - Financial eligibility (income, assets, dependents)
    - Medical or social needs
    - Relevant urgency indicators
    Provide a concise bullet-point summary that is editable by a human later.
    
    Document:
    {text}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for a transitional shelter to assess rough sleepers."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    return (response.choices[0].message.content)

left, right = st.columns([1, 2])

with left:
    st.subheader("SafeShelter AI Document Assistant")
    uploaded_file = st.file_uploader("Upload Case Document", type=["pdf", "jpg", "jpeg", "png", "docx"])
    doc_type = st.selectbox("Select Document Type", ["Medical Document", "Legal Letter", "Social Report", "Financial Document", "Others"])

with right:
    if uploaded_file and doc_type:
        filetype = uploaded_file.type
        extracted_text = extract_text(uploaded_file, filetype)
        ai_summary = generate_summary(extracted_text, doc_type)

        # Fallback to empty string to avoid NoneType
        edited_summary = st.text_area("Editable AI Summary", value=ai_summary or "", height=300)

        if edited_summary:
            st.download_button("Export", edited_summary, "summary.txt", "text/plain")
