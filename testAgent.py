import asyncio
from app.agents.research_agent import build_agent

async def main():
    print("🤖 Initializing EvidenceOps Agent and mounting tools...")
    agent = build_agent()
    
    # A complex prompt that forces the agent to use compare_sources
    test_prompt = (
        "Compare the recommended controls for high-impact AI agents "
        "with the controls for tool safety based on our internal documents."
    )
    
    print(f"\n🚀 Sending Task: '{test_prompt}'")
    print("🧠 Thinking and selecting tools (this may take a moment)...")
    
    response = await agent.run(user_msg=test_prompt)
    
    print("\n================ AGENT FINAL RESPONSE ================")
    print(response)
    print("======================================================")

if __name__ == "__main__":
    asyncio.run(main())