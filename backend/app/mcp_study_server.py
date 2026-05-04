import os
from dotenv import load_dotenv
from openai import OpenAI
from mcp.server.fastmcp import FastMCP

load_dotenv()

AI_API_KEY = os.getenv("OPENAI_API_KEY")

if not AI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in .env file")

client = OpenAI(api_key=AI_API_KEY)

mcp = FastMCP("Study AI MCP Server")


@mcp.tool()
def generate_study_material(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a study assistant. Return ONLY valid JSON. No markdown.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content or '{"error": "Empty AI response"}'


if __name__ == "__main__":
    mcp.run()
