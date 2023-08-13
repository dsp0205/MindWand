import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "Your-API-Key"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

CHATBOT_NAME = "MindWand"

def call_gpt_with_function(user_content, functions, function_call="auto"):
    messages = [
        {"role": "system", "content": f"You are conversing with {CHATBOT_NAME}..."},
        {"role": "user", "content": user_content},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call=function_call,
    )
    response_message = response["choices"][0]["message"]
    return response_message["content"]

@textbase.chatbot("sherlock-dumbledore-bot")
def on_message(messages: List[Message], state: dict = None):
    # Extract the user message from the last message in the list
    user_message = messages[-1].content if messages else ""

    # Extract the stage from the state dictionary
    stage = state.get("stage") if state else None
    if stage is None or stage not in ["welcome", "name", "chat", "investigation", "education", "personal_growth", "problem_solving"]:
        bot_response = f"""Welcome to a world of intellectual pursuit and sage wisdom! I am {CHATBOT_NAME}, here to assist you with investigative tasks, educational support, personal growth, and problem-solving.

May I have the honor of knowing your name, so that we may converse with a touch of personal elegance?"""
        next_stage = "name"

    elif stage == "name":
        username = user_message
        bot_response = f"Wonderful to meet you, {username}! How may I assist you today? Is there a mystery to unravel, a question to ponder, or perhaps guidance you seek on life's intricate paths?"
        next_stage = "chat"

    elif stage == "chat":
        if "investigation" in user_message or "investigate" in user_message:
            bot_response = "What would you like me to investigate? Please provide more details about the topic or mystery."
            next_stage = "investigation"
        elif "education" in user_message or "educate" in user_message or "guide" in user_message:
            bot_response = "What subject or area would you like guidance in? Please specify so I can assist you."
            next_stage = "education"
        elif "personal growth" in user_message or "grow" in user_message:
            bot_response = "In what area would you like support for personal growth? Please share more so I can provide tailored advice."
            next_stage = "personal_growth"
        elif "problem" in user_message or "solve" in user_message:
            bot_response = "Please describe the problem you'd like me to help you solve. I'm here to provide logical reasoning and creative thinking."
            next_stage = "problem_solving"
        else:
            bot_response = "Could you provide more details or specify whether you seek investigation, education, personal growth, or problem-solving?"
            next_stage = "chat"

    elif stage == "investigation":
        bot_response = call_gpt_with_function(f"I want to investigate {user_message}.", functions=[
            {
                "name": "investigate_research_topic",
                "description": "Investigate a given research topic and uncover hidden patterns.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string", "description": "The research topic to investigate."},
                    },
                    "required": ["topic"],
                },
            }
        ])
        next_stage = "chat"

    elif stage == "education":
        bot_response = call_gpt_with_function(f"I need guidance in {user_message}.", functions=[
            {
                "name": "guide_students",
                "description": "Guide students and learners with wisdom and tailored advice on a given subject.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subject": {"type": "string", "description": "The subject to guide students in."},
                    },
                    "required": ["subject"],
                },
            }
        ])
        next_stage = "chat"

    elif stage == "personal_growth":
        bot_response = call_gpt_with_function(f"I want to grow in {user_message}.", functions=[
            {
                "name": "personal_growth_advice",
                "description": "Offer motivational quotes, self-improvement tips, and spiritual reflections.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "area": {"type": "string", "description": "The area for personal growth."},
                    },
                    "required": ["area"],
                },
            }
        ])
        next_stage = "chat"

    elif stage == "problem_solving":
        bot_response = call_gpt_with_function(f"I need to solve this problem: {user_message}.", functions=[
            {
                "name": "solve_problem",
                "description": "Help users tackle complex problems with logical reasoning and creative thinking.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "problem_description": {"type": "string", "description": "The description of the problem to solve."},
                    },
                    "required": ["problem_description"],
                },
            }
        ])
        next_stage = "chat"

    else:
        bot_response = "I'm sorry, I seem to have lost track of our conversation. Could you please start again?"
        next_stage = "welcome"

    return bot_response, next_stage
