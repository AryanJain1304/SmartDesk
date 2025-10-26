# SmartDesk (Semantic KB)

An autonomous support agent built with **Streamlit**, capable of handling repetitive support tickets like password resets, billing queries, plan upgrades, and more. The agent uses **semantic search** with **SentenceTransformers + FAISS** to retrieve relevant knowledge base articles and can escalate tickets if it cannot resolve them.

## Features
- **Input:** Ticket title + description + user ID.
- **Smart KB Retrieval:** Semantic search for FAQ/KB articles using embeddings.
- **Mock APIs:**  
  - **Status/Config API:** Read/write account settings.  
  - **Email/Reply Draft API:** Draft replies to users.  
  - **Escalation Logger:** Log tickets that need human intervention.  
- **Agent Loop:**  
  1. Parse ticket  
  2. Plan steps  
  3. Call tools  
  4. Check outcome  
  5. Finalize reply or escalate
- **Outputs:**  
  - Solved → Draft reply + logs  
  - Escalated → Escalation note + logs


## Tech Stack

- [Streamlit](https://streamlit.io/) — UI and interaction  
- [SentenceTransformers](https://www.sbert.net/) — Text embeddings (`all-MiniLM-L6-v2`)  
- [FAISS](https://faiss.ai/) — Vector similarity search  

## Requirements

- **Python 3.10+**
- **Streamlit**
- **FAISS**
- **SentenceTransformers**

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/AryanJain1304/SmartDesk.git
cd SmartDesk
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
## Folder Structure
```bash
rag-smart-assistant/
│
├─ app.py                  # Main Streamlit app
├─ requirements.txt        # Python dependencies
└─ README.md
```

## Usage
- Once setup is complete, launch the Streamlit app:
```bash
streamlit run app.py
```
- Enter the ticket details:
  - User ID
  - Ticket Title
  - Ticket Description
- Click Submit Ticket.
- The agent will:
  - Retrieve KB articles (semantic search)
  - Call mock APIs if needed
  - Propose a draft reply or escalate
- View tool logs for all actions taken by the agent.