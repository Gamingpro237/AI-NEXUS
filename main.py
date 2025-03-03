import os
import json
import threading
import streamlit as st
import requests
import openai
import PyPDF2

openai.api_key = "your_openai_api_key_here"
anthropic_api_key = "your_anthropic_api_key_here"
gemini_api_key = "your_gemini_api_key_here"
llama_endpoint = "http://your_llama_api_endpoint_here"
ollama_endpoint = "http://localhost:11434/v1/chat/completions"

pause_event = threading.Event()
TOGGLE_KEY = "space" 


def extract_resume_data(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        resume_text = ""
        for page in reader.pages:
            resume_text += page.extract_text() or ""
    return resume_text

def get_response(prompt, resume_context, selected_model):
    if selected_model == "OpenAI GPT-4":
        return get_response_from_openai(prompt, resume_context)
    elif selected_model == "Google Gemini":
        return get_response_from_google(prompt, resume_context)
    elif selected_model == "Meta LLaMA":
        return get_response_from_meta(prompt, resume_context)
    elif selected_model == "Anthropic Claude":
        return get_response_from_anthropic(prompt, resume_context)
    elif selected_model == "Ollama":
        return get_response_from_ollama(prompt, resume_context)
    else:
        return "Selected model is not available."


def get_response_from_openai(prompt, resume_context):
    full_prompt = f"Respond as if you were me:\n{prompt}\n\nResume Information: {resume_context}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": full_prompt}],
            max_tokens=70,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI Error: {e}"


def get_response_from_google(prompt, resume_context):
    try:
        headers = {"Authorization": f"Bearer {gemini_api_key}"}
        data = {"prompt": f"{prompt}\n\nResume: {resume_context}"}
        response = requests.post("https://gemini-api.google.com/v1/generate", headers=headers, json=data)
        response.raise_for_status()
        return response.json().get("text", "Error: No response.")
    except Exception as e:
        return f"Gemini Error: {e}"


def get_response_from_meta(prompt, resume_context):
    try:
        headers = {"Content-Type": "application/json"}
        data = {"prompt": f"{prompt}\n\nResume: {resume_context}"}
        response = requests.post(llama_endpoint, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get("generated_text", "Error: No response.")
    except Exception as e:
        return f"LLaMA Error: {e}"


def get_response_from_anthropic(prompt, resume_context):
    try:
        headers = {"x-api-key": anthropic_api_key}
        data = {"prompt": f"{prompt}\n\nResume: {resume_context}", "max_tokens_to_sample": 150}
        response = requests.post("https://api.anthropic.com/v1/complete", headers=headers, json=data)
        response.raise_for_status()
        return response.json().get("completion", "Error: No response.")
    except Exception as e:
        return f"Anthropic Error: {e}"


def get_response_from_ollama(prompt, resume_context):
    try:
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "llama-7b",
            "prompt": f"{prompt}\n\nResume: {resume_context}",
            "max_tokens": 70,
            "temperature": 0.7,
        }
        response = requests.post(ollama_endpoint, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("text", "Error: No response.")
    except Exception as e:
        return f"Ollama Error: {e}"


def main():
    st.title("🧠 AI Nexus: Advanced AI Interview Assistant")
    st.sidebar.header("Configuration")

    # Model Selection
    selected_model = st.sidebar.selectbox(
        "Choose AI Model", ["OpenAI GPT-4", "Google Gemini", "Meta LLaMA", "Anthropic Claude", "Ollama"]
    )

    # Resume Upload
    uploaded_file = st.sidebar.file_uploader("Upload Your Resume (PDF)", type="pdf")
    resume_text = ""
    if uploaded_file:
        st.sidebar.success("Resume Uploaded Successfully!")
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            resume_text += page.extract_text() or ""

    # Text Input
    st.write("### 🗣️ Ask Your Question")
    question = st.text_input("Type your question below:")

    # Get AI Response
    if question:
        st.info("🤖 Generating Response...")
        response = get_response(question, resume_text, selected_model)
        st.success("### 📝 AI Response")
        st.write(response)

    # Pause/Resume
    if st.sidebar.button("🛑 Pause/Resume"):
        if pause_event.is_set():
            pause_event.clear()
            st.sidebar.success("Resumed")
        else:
            pause_event.set()
            st.sidebar.warning("Paused")

if __name__ == "__main__":
    # Start Streamlit App
    main()