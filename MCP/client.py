from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import asyncio

async def main():
    client = MultiServerMCPClient(
        {
            "math" : {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio"
            },

            "weather" : {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http"
            }
        }
    )

    import os
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools=await client.get_tools()
    model=ChatGroq(model="openai/gpt-oss-120b")
    agent=create_agent(model, tools)

    math_result=await agent.ainvoke({"messages":[{"role":"user","content":"What is the weather of Matara now?"}]})

    print("Math Result:", math_result["messages"][-1].content)

asyncio.run(main())

