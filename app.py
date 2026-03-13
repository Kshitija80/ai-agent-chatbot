import streamlit as st
from groq import Groq

# ---------------------------
# API KEY
# ---------------------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

MODEL = "llama-3.1-8b-instant"


# ---------------------------
# PAGE SETTINGS
# ---------------------------

st.set_page_config(
    page_title="AI Agents Chatbot",
    page_icon="🤖",
    layout="wide"
)


# ---------------------------
# CUSTOM UI
# ---------------------------

st.markdown("""
<style>

.stApp{
    background-color:#0E1117;
}

.chat-user{
    background-color:#1f77ff;
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
}

.chat-bot{
    background-color:#262730;
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------
# SIDEBAR
# ---------------------------

st.sidebar.title("⚙ AI Agent Pipeline")

st.sidebar.write("Agent 1 → Question Analyzer")
st.sidebar.write("Agent 2 → Topic Detector")
st.sidebar.write("Agent 3 → Explanation Generator")
st.sidebar.write("Agent 4 → Code Example Generator")
st.sidebar.write("Agent 5 → Response Formatter")


# ---------------------------
# CHAT HISTORY
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------
# AGENT 1
# ---------------------------

def agent1(question):

    prompt = f"""
Understand the user's question and rewrite it clearly.

Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL,
       messages = st.session_state.messages + [{"role": "user", "content": prompt}])


    return response.choices[0].message.content


# ---------------------------
# AGENT 2
# ---------------------------

def agent2(text):

    prompt = f"""
Identify the main topic from this question:

{text}

Return only the topic.
"""

    response = client.chat.completions.create(
        model=MODEL,
       messages = st.session_state.messages + [{"role": "user", "content": prompt}])


    return response.choices[0].message.content


# ---------------------------
# AGENT 3
# ---------------------------

def agent3(topic):

    prompt = f"""
Explain the topic '{topic}' for a beginner IT student.

Include:
1. Introduction
2. Key Concepts
3. Real-world example
4. Why it is important
"""

    response = client.chat.completions.create(
        model=MODEL,
       messages = st.session_state.messages + [{"role": "user", "content": prompt}])


    return response.choices[0].message.content


# ---------------------------
# AGENT 4
# ---------------------------

def agent4(topic):

    prompt = f"""
Give a simple programming example related to '{topic}'.
Use Python if possible.
"""

    response = client.chat.completions.create(
        model=MODEL,
      messages = st.session_state.messages + [{"role": "user", "content": prompt}] )

    

    return response.choices[0].message.content


# ---------------------------
# AGENT 5
# ---------------------------

def agent5(explanation, code):

    prompt = f"""
Format this explanation nicely for a chatbot response.

Explanation:
{explanation}

Code Example:
{code}

Structure:

Introduction
Key Points
Example Code
Conclusion
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages = st.session_state.messages + [{"role": "user", "content": prompt}]

    )
    return response.choices[0].message.content


# ---------------------------
# MAIN UI
# ---------------------------
st.title("🤖 AI Agents Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# Chat input
user_input = st.chat_input("Ask your question")

if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append(
    {"role": "user", "content": user_input}
)


    thinking_box = st.empty()

    thinking_box.write("🧠 Agent 1: Understanding question...")
    step1 = agent1(user_input)

    thinking_box.write("🔍 Agent 2: Detecting topic...")
    step2 = agent2(step1)

    thinking_box.write("📚 Agent 3: Generating explanation...")
    step3 = agent3(step2)

    thinking_box.write("💻 Agent 4: Generating code example...")
    step4 = agent4(step2)

    thinking_box.write("✨ Agent 5: Formatting response...")
    final_answer = agent5(step3, step4)

    thinking_box.empty()

    with st.chat_message("assistant"):
        st.write(final_answer)

    st.session_state.messages.append(
    {"role": "assistant", "content": final_answer}
)
