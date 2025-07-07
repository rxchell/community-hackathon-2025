import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
import docx
import io
from openai import OpenAI
from PIL import Image
import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import html
import re

# Page config
st.set_page_config(
    page_title="SafeShelter AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for SafeShelter theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main .block-container {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
    }
    
    .main-header h1 {
        color: #b95741;
        font-weight: 700;
    }
    
    .main-header p {
        color: #6b7280;
        font-size: 1.1em;
    }
    
    .upload-section {
        background: linear-gradient(135deg, #fef7f5 0%, #fdf2f0 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 2px dashed #f19484;
        text-align: center;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #b95741;
        background: linear-gradient(135deg, #fdf2f0 0%, #fcebe8 100%);
    }
    
    /* Custom text area styling */
    .stTextArea > div > div > textarea {
        border: 3px solid #f19484 !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95em !important;
        line-height: 1.6 !important;
        background: #fefefe !important;
        padding: 1rem !important;
        resize: vertical !important;
        min-height: 400px !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #b95741 !important;
        box-shadow: 0 0 0 3px rgba(241, 148, 132, 0.1) !important;
        outline: none !important;
    }
    
    .stTextArea > label {
        font-weight: 600 !important;
        color: #b95741 !important;
        margin-bottom: 0.5rem !important;
        font-size: 1.1em !important;
    }
    
    .summary-container {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(185, 87, 65, 0.08);
        border: 2px solid #f19484;
        margin-bottom: 1.5rem;
    }
    
    .summary-header {
        background: #f19484;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1em;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .stButton > button {
        background: #f19484;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(185, 87, 65, 0.3);
    }
    
    .stDownloadButton > button {
        background: #b95741;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(185, 87, 65, 0.3);
    }
    
    .extraction-preview {
        background: #fef7f5;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #f19484;
        margin: 1rem 0;
        max-height: 200px;
        overflow-y: auto;
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 0.9em;
        line-height: 1.5;
    }
    
    .welcome-state {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #fef7f5 0%, #fdf2f0 100%);
        border-radius: 16px;
        border: 2px solid #f19484;
        margin: 2rem 0;
        height: 60vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .welcome-state h3 {
        color: #b95741;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .welcome-state p {
        color: #6b7280;
        margin-bottom: 1rem;
    }
    
    .welcome-state ul {
        text-align: left;
        display: inline-block;
        margin-top: 1rem;
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #f19484;
    }
    
    .stats-container {
        background: #fef7f5;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border: 1px solid #f19484;
        font-size: 0.9em;
    }
    
    .footer {
        margin-top: 4rem;
        padding: 2rem;
        text-align: center;
        color: #6b7280;
        border-top: 2px solid #f19484;
        background: linear-gradient(135deg, #fef7f5 0%, #fdf2f0 100%);
    }
    
    .action-buttons {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .action-buttons button {
        flex: 1;
    }
    
    .edit-info {
        background: #e8f4fd;
        border: 1px solid #b3d9ff;
        color: #1e40af;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI
if "openai" in st.secrets:
    client = OpenAI(api_key=st.secrets["openai"]["OPENAI_API_KEY"])
else:
    st.error("OpenAI API key not found in secrets. Please configure your secrets.toml file.")
    st.stop()

# Initialize session state
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""
if 'ai_summary' not in st.session_state:
    st.session_state.ai_summary = ""
if 'original_summary' not in st.session_state:
    st.session_state.original_summary = ""
if 'current_summary' not in st.session_state:
    st.session_state.current_summary = ""
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Extract text with OCR
def extract_text(file, filetype):
    try:
        if filetype == "application/pdf":
            images = convert_from_bytes(file.read())
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img) + "\n"
            return text.strip()
        elif filetype.startswith("image/"):
            image_bytes = file.read()
            pil_image = Image.open(io.BytesIO(image_bytes))
            return pytesseract.image_to_string(pil_image).strip()
        elif filetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(file)
            return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        else:
            return "Unsupported file type"
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# Generate summary with OpenAI LLM 
def generate_summary(text, doc_type):
    prompt = f"""
    You are an assistant for social workers at a transitional shelter.
    Summarize the following {doc_type} based on key assessment criteria including:
    
    • Financial eligibility (income, assets, dependents)
    • Medical or social needs  
    • Relevant urgency indicators
    • Key dates and deadlines
    
    Provide a concise, well-structured summary with bullet points that is easily editable by a human later.
    Focus on actionable information that will help case workers make informed decisions.
    Format the response as plain text with clear headings and bullet points (no HTML tags).
    
    Document Content:
    {text}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a transitional shelter to assess clients. Provide clear, structured summaries focused on key eligibility and need indicators. Format responses as plain text with clear headings and bullet points."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Clean HTML from text for PDF generation
def clean_html_for_pdf(html_content):
    # Remove HTML tags and convert to plain text
    clean_content = re.sub(r'<[^>]+>', '', html_content)
    clean_content = html.unescape(clean_content)
    return clean_content

# Generate PDF from content
def generate_pdf(content, doc_type):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        spaceAfter=20,
        textColor='#b95741'
    )
    story.append(Paragraph("SafeShelter AI - Document Summary", title_style))
    story.append(Spacer(1, 12))
    
    # Document type
    story.append(Paragraph(f"<b>Document Type:</b> {doc_type}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Clean content and convert to PDF
    clean_content = clean_html_for_pdf(content)
    
    # Split into paragraphs and add to story
    paragraphs = clean_content.split('\n')
    for para in paragraphs:
        if para.strip():
            story.append(Paragraph(para.strip(), styles['Normal']))
            story.append(Spacer(1, 6))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# Header
st.markdown('<div class="main-header">', unsafe_allow_html=True)
col_logo, col_title = st.columns([1, 8])
with col_logo:
    try:
        st.image("assets/SafeShelter.png", width=120)
    except:
        st.markdown("🏠", unsafe_allow_html=True)
with col_title:
    st.markdown("""
    <h1>SafeShelter AI</h1>
    <p>Document Assistant for Social Workers</p>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### Document Upload")
    
    # Upload section
    uploaded_file = st.file_uploader(
        "Choose a file to analyse",
        type=["pdf", "jpg", "jpeg", "png", "docx"],
        help="Upload PDF, image, or Word document for analysis"
    )
    
    # Document type selector
    doc_type = st.selectbox(
        "Document Type",
        ["Medical Document", "Legal Letter", "Social Report", "Financial Document", "Housing Application", "Benefits Letter", "Other"],
        help="Select the type of document to optimize the summary"
    )
    
    # Process button
    if uploaded_file:
        if st.button("🔍  Analyse Document", type="primary", use_container_width=True):
            st.session_state.processing = True
            st.rerun()
    
    # Processing indicator
    if st.session_state.processing and uploaded_file:
        with st.spinner("Processing document..."):
            # Extract text
            st.info("📖 Extracting text from document...")
            filetype = uploaded_file.type
            extracted_text = extract_text(uploaded_file, filetype)
            st.session_state.extracted_text = extracted_text
            
            # Generate summary
            st.info("🤖 Generating AI summary...")
            ai_summary = generate_summary(extracted_text, doc_type)
            st.session_state.ai_summary = ai_summary
            st.session_state.original_summary = ai_summary
            st.session_state.current_summary = ai_summary
            
            st.session_state.processing = False
            st.success("✅ Document processed successfully!")
            time.sleep(1)
            st.rerun()
    
    # Show extracted text preview if available
    if st.session_state.extracted_text:
        st.markdown("### Extracted Text Preview")
        with st.expander("View extracted text", expanded=False):
            st.markdown(f'<div class="extraction-preview">{st.session_state.extracted_text[:500]}{"..." if len(st.session_state.extracted_text) > 500 else ""}</div>', unsafe_allow_html=True)

with col2:
    if st.session_state.ai_summary:
        # Summary header
        st.markdown('<div class="summary-header">AI Generated Summary</div>', unsafe_allow_html=True)
        
        # Editable summary in text area with custom styling
        edited_summary = st.text_area(
            "Edit the summary below:",
            value=st.session_state.current_summary,
            height=400,
            key="summary_editor",
            label_visibility="collapsed"
        )
        
        # Update current summary when edited
        if edited_summary != st.session_state.current_summary:
            st.session_state.current_summary = edited_summary
        
        # Info about editing
        st.markdown("""
        <div class="edit-info">
        💡 <strong>Tip:</strong> You can edit the summary above directly. Changes are automatically saved.
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
        # col_a, col_b, col_c = st.columns(3)
        
        # with col_a:
        #     if st.button("🔄 Revert to Original", use_container_width=True):
        #         st.session_state.current_summary = st.session_state.original_summary
        #         st.rerun()
        
        # with col_b:
        #     # Download as TXT
        #     st.download_button(
        #         "📄 Download TXT",
        #         st.session_state.current_summary,
        #         f"summary_{doc_type.lower().replace(' ', '_')}.txt",
        #         "text/plain",
        #         use_container_width=True
        #     )
        
        # PDF download
        if st.session_state.current_summary:
            pdf_buffer = generate_pdf(st.session_state.current_summary, doc_type)
            st.download_button(
                "📄 Download PDF",
                pdf_buffer,
                f"summary_{doc_type.lower().replace(' ', '_')}.pdf",
                "application/pdf",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Statistics
        if st.session_state.current_summary:
            word_count = len(st.session_state.current_summary.split())
            char_count = len(st.session_state.current_summary)
            st.markdown(f'<div class="stats-container">📊 {word_count} words, {char_count} characters</div>', unsafe_allow_html=True)
    
    else:
        # Welcome state
        st.markdown("""
        <div class="welcome-state">
            <h3>👋 Welcome to SafeShelter AI</h3>
            <p>Upload a document to get started with AI-powered case analysis.</p>
            <p>The system will extract text and generate a structured summary focusing on:</p>
            <ul>
                <li>Financial eligibility criteria</li>
                <li>Medical and social needs</li>
                <li>Urgency indicators</li>
                <li>Key dates and deadlines</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p><strong>SafeShelter AI</strong> - Empowering social workers with intelligent document analysis</p>
    <p style="font-size: 0.9em; margin-top: 0.5rem;">Secure • Efficient • Compassionate</p>
</div>
""", unsafe_allow_html=True)