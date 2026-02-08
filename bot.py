#Streamlit for Chatbot UI
import os
import streamlit as st
from huggingface_hub import InferenceClient

#Chatbot color changing Title
st.markdown("""
<style>
@keyframes rainbow {
  0% {color: red;}
  20% {color: orange;}
  40% {color: yellow;}
  60% {color: green;}
  80% {color: cyan;}
  100% {color: violet;}
}
.animated-title {
  font-size: 50px;
  font-weight: bold;    
  animation: rainbow 10s infinite;
}
</style>
<h1 class="animated-title">QueryMate</h1>
""", unsafe_allow_html=True)


#Description and image
st.title("Your AI-Powered Query Assistant")
st.image("https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif", width=100)


# Customize Streamlit app background color and style
st.markdown("""
<style>
/* Main app background */
[data-testid="stAppViewContainer"] {
    background-color: #3E2F2F;  /* dark brown */
    background-image: radial-gradient(circle, #4B3621 0%, #3E2F2F 100%);
    color: #FFFFF;
}
</style>
""", unsafe_allow_html=True)



# Streamlit-friendly response generator
def response_generator(user_prompt):
    # Read HF API token from environment variable
    hf_token = os.environ.get("HF_API_TOKEN")
    if not hf_token:
        raise ValueError("Please set the HF_API_TOKEN environment variable!")

    client = InferenceClient(
        "openai/gpt-oss-120b:groq",
        token=hf_token
    )

    stream = client.chat.completions.create(
        model="openai/gpt-oss-120b:groq",
        messages=[{"role": "user", "content": user_prompt}],
        stream=True,
    )

    # Use a placeholder in Streamlit to update text live
    placeholder = st.empty()
    bot_response = ""

    for chunk in stream:
        if chunk.choices[0].delta.content:
            bot_response += chunk.choices[0].delta.content
            placeholder.markdown(bot_response)  # live update in chat

    return bot_response
    


#setup state message variable for bot to store all prompts of the session
if "messages" not in st.session_state:
    st.session_state.messages = []

#display all the messages in the session state variable
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

#input field to pass the prompt
user_prompt = st.chat_input("How can I help you today 😊")

#display user prompt on hit enter
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    #store the user prompt in the session state variable
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    #display the response from the model 
    with st.chat_message("bot", avatar="assistant"):
        bot_response = response_generator(user_prompt)
    #store the bot response in the session state variable
    st.session_state.messages.append({"role": "bot", "content": bot_response, "avatar": "assistant"})


