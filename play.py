import streamlit as st
import replicate
import os
from llama_cpp import Llama

# App title
st.set_page_config(page_title="Psychology BOT")

# Replicate Credentials
with st.sidebar:
    st.title('PSYCHOLOGY BOT')

    replicate_api = "r8_ABxxgOip1c12YO1iEjtDOiQZrAPA2zs2gby81"
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    # if selected_model == 'Llama2-7B':
    #     llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    # elif selected_model == 'Llama2-13B':
    #     llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    llm = Llama(model_path="C:\Users\sijig\.cache\lm-studio\models\TheBloke\Llama-2-7B-Chat-GGML\llama-2-7b-chat.ggmlv3.q4_0.bin",
            n_ctx=512,
            n_batch=128)

    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=32, max_value=40000, value=20000, step=8)
    
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "psychologist", "content": "How are you doing?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "psychologist", "content": "How are you doing?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful psychologist. You have extensive knowledge of psychology, and are a experienced psychologist and you can only speak english. You always offer a compassionate ear for the patients. You know nothing and have no information other than psychology and your sole purpose is to treat patients and only focus on helping user with their mental health and well-being. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "psychologist: " + dict_message["content"] + "\n\n"
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
                           input={"prompt": f"{string_dialogue} {prompt_input} psychologist: ",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
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