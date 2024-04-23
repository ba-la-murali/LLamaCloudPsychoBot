import streamlit as st
import os
from ctransformers import AutoModelForCausalLM

# App title
st.set_page_config(page_title="PsychoBot")

@st.cache_resource()
def ChatModel(temperature, top_p):
    return AutoModelForCausalLM.from_pretrained(
        'C:\\Users\\sijig\\.cache\\lm-studio\\models\\TheBloke\\Llama-2-7b-Chat-GGUF\\llama-2-7b-chat.Q4_0.gguf',
        model_type='llama',
        temperature=temperature, 
        top_p = top_p)

# Replicate Credentials
with st.sidebar:
    st.title('Psychology Bot')

    st.subheader('Models and parameters')
    
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=2.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    # max_length = st.sidebar.slider('max_length', min_value=64, max_value=4096, value=512, step=8)
    chat_model =ChatModel(temperature, top_p)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "psychologist", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "psychologist", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


def generate_llama2_response(prompt_input):
    string_dialogue = "You are Joel the psychologist answering users' questions. Reply as Joel. You will ask user about his day and mood and convert his experience to a positive experience through anecdotes and conversation. If the mood of user is low, ask why he feels low and help him convert the experience to a positive experience. If user feels joyful, then ask what was the experience and tell the user how he can retain the joyful state and remind him to stay grateful for the life and experiences they got. After every 5 conversations ask the user if he wants to journal the experience of the day. If yes, then create a 100 words summary for entering in the daily journal. Remember to create the summary highlighting the positive aspects and learnings from the day. Do not ask the user to enter journal or summary before 5 conversations. Keep the conversation precise. In the summary keep user as the main character and do not use joel or psychologist as the highlight. Use lot of emojis to make the conversation interesting."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\\n\\n"
        else:
            string_dialogue += "psychologist: " + dict_message["content"] + "\\n\\n"
    output = chat_model(f"prompt {string_dialogue} {prompt_input} psychologist: ")
    return output

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from psychologist
if st.session_state.messages[-1]["role"] != "psychologist":
    with st.chat_message("psychologist"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "psychologist", "content": full_response}
    st.session_state.messages.append(message)