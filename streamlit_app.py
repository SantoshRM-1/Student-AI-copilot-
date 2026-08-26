import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import json
import os
from datetime import datetime

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Student AI Copilot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

# ==================================================
# CSS
# ==================================================

st.markdown("""
<style>

.stApp {
    background-color: #050B1F;
}

section[data-testid="stSidebar"] {
    background-color: #08142E;
}

.hero {
    background: linear-gradient(135deg,#2B3CFF,#8A3FFC);
    padding: 35px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}

.feature-card {
    background: #0D162D;
    padding: 20px;
    border-radius: 15px;
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
}

.welcome {
    background: #101B35;
    padding: 25px;
    border-radius: 15px;
    color: white;
    text-align: center;
}

.footer {
    text-align:center;
    color:gray;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# MEMORY
# ==================================================

MEMORY_FILE = "memory.json"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({}, f)

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

memory = load_memory()

# ==================================================
# SESSION
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================================================
# LLM
# ==================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

prompt = PromptTemplate.from_template("""
You are a helpful Student AI Copilot.

Question: {question}

Answer:
""")

chain = prompt | llm

# ==================================================
# TOOLS
# ==================================================

def calculator_tool(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid Expression"

def current_time_tool():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🎓 Student AI Copilot")

    st.markdown("---")

    st.subheader("Features")

    st.write("💬 AI Chat")
    st.write("🧮 Calculator")
    st.write("🕒 Time Tool")
    st.write("🧠 Memory")

    st.markdown("---")

    st.subheader("Tech Stack")

    st.write("🔗 LangChain")
    st.write("🚀 Groq")
    st.write("⚡ Streamlit")

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ==================================================
# HERO
# ==================================================

st.markdown("""
<div class="hero">
<h1>🎓 Student AI Copilot</h1>
<p>LangChain + Groq + Streamlit</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# FEATURE CARDS
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
    <h3>🤖 AI Chat</h3>
    Ask questions using Groq LLM.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
    <h3>🧠 Memory</h3>
    Remembers your name.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
    <h3>🛠 Tools</h3>
    Calculator + Time Tool
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==================================================
# WELCOME
# ==================================================

if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="welcome">
    <h2>Welcome</h2>

    Try:
    <br><br>
    What is AI?
    <br><br>
    What is 45 * 12?
    <br><br>
    What time is it?
    <br><br>
    My name is Santosh
    <br><br>
    What is my name?
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# CHAT HISTORY
# ==================================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==================================================
# INPUT
# ==================================================

question = st.chat_input("Ask me anything...")

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    if question.lower().startswith("my name is"):

        name = question[10:].strip()

        memory["name"] = name

        save_memory(memory)

        answer = f"Nice to meet you, {name}!"

    elif "what is my name" in question.lower():

        if "name" in memory:
            answer = f"Your name is {memory['name']}"
        else:
            answer = "I don't know your name yet."

    elif "time" in question.lower():

        answer = f"Current Time: {current_time_tool()}"

    elif any(op in question for op in ["+", "-", "*", "/"]):

        expression = (
            question.lower()
            .replace("what is", "")
            .replace("calculate", "")
            .strip()
        )

        answer = calculator_tool(expression)

    else:

        try:

            with st.spinner("AI is thinking..."):

                response = chain.invoke(
                    {
                        "question": question
                    }
                )

                answer = response.content

        except Exception as e:

            answer = f"Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# ==================================================
# FOOTER
# ==================================================

st.markdown("""
<div class="footer">
Student AI Copilot • LangChain • Groq • Streamlit
</div>
""", unsafe_allow_html=True)