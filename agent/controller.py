
# import os

# from dotenv import load_dotenv
# from langchain.agents import create_agent
# from langchain_google_genai import ChatGoogleGenerativeAI

# from agent.tools_registry import TOOLS

# load_dotenv()

# MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

# SYSTEM_PROMPT = """
# You are an AI assistant with weather and stock-price tools.

# Rules:
# 1. Use weather_tool for current weather questions.
# 2. Use stock_tool for stock price questions.
# 3. Never invent weather observations or stock prices.
# 4. Ask a clarifying question if required information is missing.
# 5. For Indian stocks, use Yahoo Finance symbols such as TCS.NS
#    when appropriate.
# 6. Clearly explain tool errors instead of inventing results.
# 7. For stock prices, distinguish the latest closing price
#    from a live intraday price.
# 8. For unrelated questions, answer normally without calling tools.
# """

# def build_agent():
#     api_key = os.getenv("GOOGLE_API_KEY")

#     if not api_key:
#         raise ValueError(
#             "GOOGLE_API_KEY is missing. Check your .env file."
#         )

#     llm = ChatGoogleGenerativeAI(
#         model=MODEL_NAME,
#         google_api_key=api_key,
#         temperature=0,
#     )

#     return create_agent(
#         model=llm,
#         tools=TOOLS,
#         system_prompt=SYSTEM_PROMPT,
#     )


# def ask_agent(agent, query: str) -> str:
#     result = agent.invoke({
#         "messages": [
#             {"role": "user", "content": query}
#         ]
#     })

#     last_message = result["messages"][-1]
#     return last_message.content

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from agent.tools_registry import TOOLS

load_dotenv()

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite",
)

SYSTEM_PROMPT = """
You are a reliable AI assistant with weather and stock-price tools.

TOOL USAGE:
1. Use weather_tool whenever the user asks about current weather.
2. Use stock_tool whenever the user asks about stock prices.
3. Use the actual tool output as the source of factual data.
4. Never invent, estimate, or fabricate tool results.
5. If a tool fails, clearly explain the failure.

RESPONSE QUALITY:
1. Convert tool output into a clear, natural-language answer.
2. Do not expose raw JSON, Python objects, metadata,
   signatures, or internal tool execution details.
3. Use headings and bullet points when they improve readability.
4. Include units and explain relevant financial terminology.
5. Keep simple answers concise and useful.

WEATHER:
- Include temperature, feels-like temperature, conditions,
  humidity, and wind speed when available.
- Mention the location.
- Do not claim a timestamp or observation time unless provided
  by the tool.

STOCKS:
- Use appropriate ticker symbols, such as TCS.NS for TCS
  on the National Stock Exchange of India.
- Distinguish live prices from delayed prices and closing prices.
- Include currency, market status, and timestamp when available.
- Never present a closing price as a live price.

GENERAL:
- Ask a clarifying question if essential information is missing.
- Answer unrelated questions normally without calling tools.
"""


def build_agent():
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is missing. Check your .env file."
        )

    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=api_key,
        temperature=0,
    )

    return create_agent(
        model=llm,
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )


def ask_agent(agent, query: str) -> str:
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    })

    last_message = result["messages"][-1]
    content = last_message.content

    # Gemini/LangChain can return structured content blocks.
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, str):
                text_parts.append(block)

            elif isinstance(block, dict):
                if block.get("type") == "text":
                    text = block.get("text", "")
                    if text:
                        text_parts.append(text)

        if text_parts:
            return "\n".join(text_parts)

    return str(content)
