import streamlit as st

st.set_page_config(
    page_title="Medical Health Assistant",
    page_icon="🏥",
    layout="centered"
)

with st.sidebar:
    st.markdown("## About")
    st.markdown("This app uses **LLaMA 3** powered by Groq to answer general health questions.")
    st.markdown("---")
    st.markdown("### ⚠️ Disclaimer")
    st.markdown("This is not a substitute for professional medical advice. Always consult a qualified doctor.")
    st.markdown("---")
    st.markdown("### 🔒 Safety")
    st.markdown("Questions involving self-harm or emergencies are automatically flagged.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


system_prompt = """You are a friendly and helpful medical assistant. 
You answer general health questions in simple, clear language.
You never diagnose diseases or prescribe medications.
If a question is too serious or life threatening, always advise the user to see a real doctor immediately.
Never give specific dosage advice."""

#safety check
dangerous_keywords = ['suicide', 'overdose', 'kill myself', 'self harm', 'how to die']
def safety_check(question):
    for keyword in dangerous_keywords:
        if keyword.lower() in question.lower():
            return True
    return False
def ask_health_questions(question):
  response = client.chat.completions.create(
    model="llama-3.1-8b-instant"
,
    messages=[
       {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
  )
  
  #safety chek
  if(safety_check(question)):
    return "I'm sorry, this question involves a serious concern." \
    " Please contact a healthcare professional or call emergency services immediately."
  else:
   return response.choices[0].message.content

#GUI
# st.title("🏥Medical Health Assistant")
# st.write("Ask me any general health question." \
# " I am not a doctor but I can help with general health information.")

# question = st.text_input("Enter yout health question here : ")

# if st.button("Ask"):
#    if question:
#       with st.spinner("Thinking........"):
#          response = ask_health_questions(question)
#       st.write(response)
#    else:
#       st.warning("Please enter a question first")

st.title("🏥 Medical Health Assistant")
st.markdown("---")
st.markdown("### Ask me any general health question")
st.markdown("*I provide general health information only. Always consult a real doctor for medical advice.*")

st.markdown("---")

# Chat input
if question := st.chat_input("Ask a health question..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask_health_questions(question)
        st.write(response)
    
    # Add response to history
    st.session_state.messages.append({"role": "assistant", "content": response})