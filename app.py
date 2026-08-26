from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

import json
import os
from datetime import datetime

# ==========================
# Load Environment Variables
# ==========================

load_dotenv()

# ==========================
# Memory Setup
# ==========================

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

# ==========================
# LLM Setup
# ==========================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# ==========================
# Prompt Template
# ==========================

prompt = PromptTemplate.from_template(
    """
You are a helpful Student AI Assistant.

Question:
{question}

Answer:
"""
)

chain = prompt | llm

# ==========================
# Tools
# ==========================

def calculator_tool(expression):
    try:
        return eval(expression)
    except:
        return "Invalid Expression"

def current_time_tool():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# ==========================
# Assistant
# ==========================

print("=" * 50)
print("Student AI Copilot Started")
print("Type 'exit' to quit")
print("=" * 50)

while True:

    question = input("\nYou: ").strip()

    if question.lower() == "exit":
        print("Assistant: Goodbye!")
        break

    # Save Name

    if question.lower().startswith("my name is"):

        name = question[10:].strip()

        memory["name"] = name

        save_memory(memory)

        print(f"Assistant: Nice to meet you, {name}!")

        continue

    # Recall Name

    if "what is my name" in question.lower():

        if "name" in memory:
            print(f"Assistant: Your name is {memory['name']}")
        else:
            print("Assistant: I don't know your name yet.")

        continue

    # Time Tool

    if "time" in question.lower():

        print(
            f"Assistant: Current Time = {current_time_tool()}"
        )

        continue

    # Calculator Tool

    operators = ["+", "-", "*", "/"]

    if any(op in question for op in operators):

        expression = (
            question.lower()
            .replace("what is", "")
            .replace("calculate", "")
            .strip()
        )

        print(
            f"Assistant: {calculator_tool(expression)}"
        )

        continue

    # LLM Response

    try:

        response = chain.invoke(
            {
                "question": question
            }
        )

        print(
            f"Assistant: {response.content}"
        )

    except Exception as e:

        print(
            f"Assistant Error: {e}"
        )