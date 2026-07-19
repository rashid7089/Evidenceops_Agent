import asyncio
from app.orchestrator import run_research
from enum import Enum
# import uvicorn
from app.statusEnum import Status




async def main():
    print("Welcome to EvidenceOps CLI")
    
    current_question = ""
    awaiting_approval = False

    current_status = Status.Waiting_User_Input.value

    def update_status(status):
        current_status = status.value
        print(f"[STATUS]: {current_status}\n")

    while True:
        update_status(Status.Waiting_User_Input)
        user_input = input("\nResearch Question: ").strip()
        

        if user_input.strip() == '': continue
        if user_input.lower() in ["exit", "quit"]:
            break
            
        if awaiting_approval and user_input.lower() == "yes":
            update_status(Status.Approved)
            print("🚀 Human approval received! Elevating capabilities and saving...")
            response = await run_research(current_question, approved_to_save=True)
            print(response)
            awaiting_approval = False

        else:
            current_question = user_input
            update_status(Status.Draft)
            response = await run_research(current_question, approved_to_save=False)
            print(response)
            
            awaiting_approval = True
            update_status(Status.Awaiting_approval)
            print("\n[SYSTEM] Type 'yes' to approve saving this report to disk, or ask a new question.")


asyncio.run(main())
