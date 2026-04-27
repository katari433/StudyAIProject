from fastapi import HTTPException
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def call_mcp_ai_service(prompt: str) -> str:
    server_params = StdioServerParameters(
        command="python3",
        args=["mcp_study_server.py"],
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "generate_study_material",
                    arguments={"prompt": prompt}
                )

                return result.content[0].text

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"MCP AI service error: {str(e)}"
        )


