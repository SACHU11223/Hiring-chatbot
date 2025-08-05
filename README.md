# Hiring Chatbot 🤖 – TalentScout AI Assistant

An intelligent AI-based hiring assistant chatbot built using **Streamlit** and **Gemini LLM**, designed to simulate the initial screening round of a job interview for technical candidates.



---

## 📌 Features

- 🌐 Interactive chatbot with clean UI using Streamlit
- 📥 Collects candidate details: Name, Email, Phone, Experience, Location, Position
- 🧠 Dynamically generates **tech-specific questions** using Gemini AI based on candidate's declared tech stack
- 🎯 Context-aware chat with error handling and fallback prompts
- ✅ Validates inputs and gives **performance rating** out of 5
- 🛑 Ends session gracefully and allows "Start New Chat"
- 🔒 Secure API key handling (see below)

---

## 🚀 Getting Started

### 🔧 Installation

```bash
# Clone the repo or download ZIP
cd Hiring-Chatbot

# Create virtual environment (optional but recommended)
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🔐 Setup Your Gemini API Key

Follow these steps:

1. Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_actual_google_generative_ai_key
```

2. Make sure you have `python-dotenv` installed:
```bash
pip install python-dotenv
```

3. Your code should use:
```python
from dotenv import load_dotenv
import os
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
```

## 🧪 Run the Application

```bash
streamlit run app.py
```

Then open the provided localhost link in your browser to start chatting with the AI.

---

## 📄 Files Included

|         File            |                 Description            |
|-------------------------|----------------------------------------|
|   `app.py`              | Main Streamlit app file                |
|   `.env`                | (User-created) for storing API key     |
|   `requirements.txt`    | Python package dependencies            |
|  `candidate_data.json`  |Stores candidate conversations locally  |

---

## 📦 Tech Stack

- Python 🐍
- Streamlit 📺
- Google Gemini API 🧠
- Regex for validation
- JSON for local storage

---

## 📝 Prompt Engineering

Carefully designed prompts instruct Gemini to:
- Generate role-specific technical questions
- Validate tech stack input
- Provide fallback messages for wrong input

---

## 📈 Evaluation Metrics

Each candidate's performance is scored based on the **length and quality of responses**, resulting in a rating out of 5 at the end of the conversation.

---

---
---

## 📬 Contact

**Sachin Sharma**  
Email: sachin.s9792@gmail.com  
GitHub: [github.com/SACHU11223/Hiring-chatbot]  
