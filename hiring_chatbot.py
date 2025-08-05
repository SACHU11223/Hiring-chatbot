import streamlit as st
import google.generativeai as genai
import json
import re

# Gemini API Setup
GOOGLE_API_KEY = "AIzaSyB-VFy57eHAJfs7uRQUOX6LbjnWxmhle2Q"  # Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Session State Initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "bot", "content": "Welcome to TalentScout Hiring Assistant! \nI'm here to assist with your initial screening.\nPlease provide your full name to begin. You can type 'exit' at any time to end the conversation."}
    ]
    st.session_state.candidate_info = {}
    st.session_state.stage = "name"
    st.session_state.questions = []
    st.session_state.current_question_index = 0
    st.session_state.qa_pairs = []
    st.session_state.chat_ended = False

# Function to Get Gemini Response
def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: Unable to process your request due to {str(e)}. Please try again."

# Validate Tech Stack using Gemini
def validate_tech_stack(tech_stack):
    prompt = f"Is the following a valid list of technologies or tech stack?\n'{tech_stack}'\nRespond with only 'Yes' or 'No'."
    validation = get_gemini_response(prompt)
    return validation.strip().lower() == "yes"

# Validate Answer Quality

def validate_answer_quality(answer):
    return len(answer.strip()) >= 10

# Function to Save Candidate Info

def save_candidate_info():
    candidate_data = st.session_state.candidate_info.copy()
    candidate_data["qa_pairs"] = st.session_state.qa_pairs
    candidate_data["rating"] = generate_performance_rating()
    with open("candidate_data.json", "a") as f:
        json.dump(candidate_data, f)
        f.write("\n")

# Generate Rating based on QA length

def generate_performance_rating():
    total_score = sum([len(pair['answer']) for pair in st.session_state.qa_pairs])
    if total_score > 800:
        return 5
    elif total_score > 600:
        return 4
    elif total_score > 400:
        return 3
    elif total_score > 200:
        return 2
    else:
        return 1

# Chatbot Logic

def chatbot_response(user_input):
    user_input = user_input.strip()

    if st.session_state.chat_ended:
        return "Chat has already ended. Click 'Start New Chat' to begin again."

    if "exit" in user_input.lower():
        st.session_state.stage = "end"
        st.session_state.chat_ended = True
        save_candidate_info()
        return f"Thank you for your time! Our HR team will contact you soon.\nRating: {generate_performance_rating()} / 5\nStay active!"

    stage = st.session_state.stage

    if stage == "name":
        if any(char.isdigit() for char in user_input) or len(user_input) < 2:
            return "Please enter a valid name (no numbers allowed)."
        st.session_state.candidate_info["full_name"] = user_input
        st.session_state.stage = "email"
        return "Thank you! Please provide your email address."

    elif stage == "email":
        if not re.match(r"[^@]+@[^@]+\.[^@]+", user_input):
            return "Please provide a valid email address (e.g., example@domain.com)."
        st.session_state.candidate_info["email"] = user_input
        st.session_state.stage = "phone"
        return "Got it! What’s your phone number?"

    elif stage == "phone":
        if not re.match(r"^[0-9\-\+\s]{8,15}$", user_input):
            if len(user_input) != 10:
                return "Please enter a valid phone number."
        st.session_state.candidate_info["phone"] = user_input
        st.session_state.stage = "experience"
        return "Thanks! How many years of experience do you have?"

    elif stage == "experience":
        try:
            years = float(user_input)
            if years < 60:
                st.session_state.candidate_info["experience"] = user_input
                st.session_state.stage = "position"
                return "Great! What position(s) are you applying for?"
            
            else:
                return "Please enter a valid number of years (e.g., 2 or 3.5)."
            
        except:
            return "Please enter a valid number of years (e.g., 2 or 3.5)."

    elif stage == "position":
        if len(user_input) < 2:
            return "Please enter a valid position."
        st.session_state.candidate_info["position"] = user_input
        st.session_state.stage = "location"
        return "Noted! What’s your current location?"

    elif stage == "location":
        if len(user_input) < 2:
            return "Please enter a valid location."
        st.session_state.candidate_info["location"] = user_input
        st.session_state.stage = "tech_stack"
        return "Thanks! Please specify your tech stack (e.g., programming languages, frameworks, databases, tools)."

    elif stage == "tech_stack":
        if not validate_tech_stack(user_input):
            return "Invalid tech stack. Please provide a valid list of technologies."
        st.session_state.candidate_info["tech_stack"] = user_input
        prompt = f"Generate exactly 5 technical questions to assess proficiency in {user_input}. List each question on a new line with no additional text or numbering."
        questions_text = get_gemini_response(prompt)
        questions = [q.strip() for q in questions_text.split("\n") if q.strip()]
        if len(questions) < 5:
            return "Sorry, I couldn’t generate enough questions. Please clarify your tech stack and try again."
        st.session_state.questions = questions[:5]
        st.session_state.stage = "asking_questions"
        st.session_state.current_question_index = 0
        return f"Great! Here’s your first technical question:\n\n{st.session_state.questions[0]}"

    elif stage == "asking_questions":
        if not validate_answer_quality(user_input):
            return "Please provide a more detailed answer to the question."
        q_index = st.session_state.current_question_index
        current_question = st.session_state.questions[q_index]
        st.session_state.qa_pairs.append({
            "question": current_question,
            "answer": user_input
        })
        st.session_state.current_question_index += 1
        if st.session_state.current_question_index < 5:
            next_q = st.session_state.questions[st.session_state.current_question_index]
            return f"Thank you! Here’s your next question:\n\n{next_q}"
        else:
            st.session_state.stage = "end"
            st.session_state.chat_ended = True
            save_candidate_info()
            return f"Thank you for your time! Our HR team will contact you soon.\nRating: {generate_performance_rating()} / 5\nStay active!"

    return "Conversation ended. Thank you!"

# UI Setup
st.set_page_config(page_title="TalentScout Assistant", layout="centered")
st.title("TalentScout Hiring Assistant")
st.write("Chat with our AI to begin your screening process.")

# Display Chat History
for message in st.session_state.chat_history:
    if message["role"] == "bot":
        st.markdown(
            f"<div style='background-color:#2B303E;padding:10px;border-radius:8px;margin-bottom:5px;'>"
            f"<b>Talent Scout Bot:</b> {message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div style='text-align:right;background-color:#2B303E;padding:10px;border-radius:8px;margin-bottom:5px;'>"
            f"<b>You:</b> {message['content']}</div>", unsafe_allow_html=True)

# Input Form (Disabled if chat ended)
if not st.session_state.chat_ended:
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area("Type your response here:", height=100)
        submitted = st.form_submit_button("Send")
    if submitted and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        bot_reply = chatbot_response(user_input)
        st.session_state.chat_history.append({"role": "bot", "content": bot_reply})
        st.rerun()
else:
    st.success("Chat ended. Click below to start a new conversation.")
    if st.button("Start New Chat"):
        for key in ["chat_history", "candidate_info", "stage", "questions", "current_question_index", "qa_pairs", "chat_ended"]:
            st.session_state.pop(key, None)
        st.rerun()
