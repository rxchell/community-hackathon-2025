# [Community Hackathon 2025](https://www.community-hackathon.gov.sg/)
_Streamlining Shelter Referrals with AI_

<img src="assets/SafeShelter.png"/>

## What is SafeShelter?
An AI tool that extracts and summarizes key info from uploaded documents (e.g. court, medical, social reports) to support shelter assessments

**Vision:**
- A world where no one is left without shelter because of paperwork — where social workers are empowered with smart tools to focus on people, not paperwork.

**Mission:**
- We build AI-powered tools that extract and summarise key info from uploaded documents to help social workers assess rough sleepers faster and more accurately.

**Key Features:**
- User uploads docs (financial, medical, legal, etc.)
- User selects document type
- OCR extracts text
- LLM summarises and outputs suitability, room type, financial info
- Users can edit the summary and export it
- Summary saved to individual profiles

**Inspiration:**
- UI Reference: Claude-style – editable AI output on the right
- Tech Inspiration: GovTech’s AIsay

## Developers' Guide
### Running the web app locally
- Create a Python virtual environment and activate it.
- Install libraries: `pip install -r requirements.txt`.
- Run the app: `streamlit run app.py`

### Tech Stack
#### Frontend
- **Streamlit**: Python-based web app framework for building the UI.
  - Handles file uploads, document type tagging, editable summaries, and export functionality.

#### AI / LLM Services
- **OpenAI API** (`gpt-4o-mini`):
  - Generates document summaries tailored to shelter assessment needs.
  - Used via `openai.ChatCompletion.create`.

#### Document Processing / OCR
| Task                          | Tool/Library         |
|-------------------------------|----------------------|
| OCR for scanned PDFs/images   | `pytesseract`        |
| Convert PDF pages to images   | `pdf2image`          |
| Open and decode image files   | `Pillow (PIL)`       |
| Extract text from `.docx`     | `python-docx`        |
| Handle byte streams           | `io` (standard lib)  |

#### Secrets Management
- **Streamlit Secrets (`.streamlit/secrets.toml`)**:
  - Stores API keys and service credentials securely.
  - Example keys:
    - `openai_key` for OpenAI
    - `textkey` for Firebase service account

#### Python Libraries Used
- `streamlit`
- `openai`
- `pytesseract`
- `pdf2image`
- `Pillow`
- `python-docx`
- `io` (standard library)

#### Database
- **Frebase (Firestore)**
  - To manage user data, document metadata, or storage.
  - Accessed via credentials stored in `secrets.toml`.

#### Summary
| Layer         | Tool/Library        |
|---------------|---------------------|
| Frontend      | Streamlit           |
| LLM           | OpenAI (`gpt-4o-mini`) |
| OCR/Parsing   | pytesseract, pdf2image, Pillow, python-docx |
| Secrets Mgmt  | Streamlit Secrets   |
| Cloud Backend | Firebase (optional) |

### Theme Colours 
- Light pastel red: #f19484
- Dark pastel red: #b95741