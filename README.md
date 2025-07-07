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
- Create a Python virtual environment and activate it.
- Install libraries: `pip install -r requirements.txt`.
- Run the app: `streamlit run app.py`

### Tech Stack
- Streamlit
- Firebase (Firestore)

### Theme Colours 
- Light pastel red: #f19484
- Dark pastel red: #b95741