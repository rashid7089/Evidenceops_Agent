from __future__ import annotations

from app.agents.research_agent import build_agent
from app.models import ResearchResult
import inspect
from pathlib import Path
import json 

async def run_research(question: str, approved_to_save: bool = False) -> str:
    agent = build_agent(approved_to_save)

    approval_instruction = (
        "CRITICAL: The human has granted explicit file write authorization. "
        "You MUST immediately call your 'save_report' tool to write this finalized content "
        "to disk. Do not just print text; execute the tool now."
    ) if approved_to_save else "Do not call save_report. Return a draft and request approval."
    prompt = f"""
Research objective: {question}

Execution constraint: {approval_instruction}
Use the available tools and produce an evidence-grounded response.
"""
    result = await agent.run(user_msg=prompt)
    tools_used = [tc.tool_name for tc in result.tool_calls]
    tool_calls = []

    for tc in result.tool_calls:
        call_record = {
            "tool_name": tc.tool_name,
            "tool_kwargs": tc.tool_kwargs,
        }

        raw_output = tc.tool_output.raw_output

        # If this tool came from knowledge_base_search, it has source_nodes
        if hasattr(raw_output, "source_nodes"):
            call_record["sources"] = [
                {
                    "file_path": node.metadata.get("file_path"),
                    "file_name": node.metadata.get("file_name"),
                    "score": node.score,
                    "text": node.text,
                }
                for node in raw_output.source_nodes
            ]

        tool_calls.append(call_record)


    record = {
        "question": question,
        "response_text": str(result.response),
        "tools_used": [tc.tool_name for tc in result.tool_calls],
        "tool_calls": tool_calls
    }
    Path("eval_runs").mkdir(exist_ok=True)
    # run_file = Path("eval_runs/run_001.json")
    Path("eval_runs/run_002.json").write_text(
        json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return ResearchResult(
        report_id="314",
        result=str(result),
        tools_used=tools_used,
        tool_calls=tool_calls,
        approved_to_save=approved_to_save,
    )
    # return str(result)

