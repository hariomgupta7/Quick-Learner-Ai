import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Load API Key First ---
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Old SDK Configuration ---
# This is the old way to configure, which matches the
# broken library stuck on your machine.
if API_KEY:
    try:
        genai.configure(
            api_key=API_KEY,
            # This is the old, deprecated way to set the server.
            # This is the fix.
            client_options={"api_endpoint": "generativelanguage.googleapis.com"}
        )
    except Exception as e:
        st.error(f"Error configuring API: {e}")
else:
    st.error("Google API Key not found. Please check your .env file.")

# --- Function to get response ---
def get_gemini_response(prompt):
    try:
        # We use the stable 'gemini-1.0-pro' model
        model = genai.GenerativeModel('gemini-1.0-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # This will catch the 404 error if it still happens
        st.error(f"Error generating content: {e}")
        st.info("This can happen if the 'GenerGative Language API' is not enabled in your Google Cloud project.")
        return None

# --- Streamlit App Interface ---
st.set_page_config(page_title="QuickLearnerAI", page_icon="⚡", layout="centered")
st.title("⚡ QuickLearnerAI")
st.write("Your personal AI tutor. Enter any topic and get a concise study guide.")

# User input
topic = st.text_input("Enter a topic:", placeholder="e.g., 'Binary Search Trees', 'Newton's First Law', 'Logic Gates'")

# Generate button
if st.button("Generate Study Guide"):
    if not API_KEY:
        st.warning("API Key not found. Cannot proceed.")
    elif topic:
        with st.spinner(f"QuickLearnerAI is generating your guide for '{topic}'..."):
            
            prompt_template = f"""
            You are an expert educator and study assistant. Your task is to generate a clear, concise, and easy-to-understand study guide on the topic: "{topic}".

            The guide must be structured with the following sections:
            1.  **Core Concept:** A brief, simple explanation.
            2.  **Key Points (Bulleted):** A list of the 3-5 most critical facts.
            3.  **Simple Example:** A clear, practical example.
            4.  **Practice Questions:** Two or three simple questions with answers.
            Format the entire output clearly using markdown.
            """
            
            response_text = get_gemini_response(prompt_template)
            
            if response_text:
                st.subheader(f"Study Guide for: {topic}")
                st.markdown(response_text)
    else:
        st.warning("Please enter a topic to generate a guide.")