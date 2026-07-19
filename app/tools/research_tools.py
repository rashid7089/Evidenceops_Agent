from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from llama_index.core.tools import FunctionTool, QueryEngineTool

from app.services.index_service import load_query_engine


def save_report(title: str, content: str) -> str:
    # Saving is local and intentionally restricted to the reports directory.
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    safe_name = "".join(ch for ch in title.lower().replace(" ", "_") if ch.isalnum() or ch == "_")
    path = reports_dir / f"{safe_name[:60] or 'report'}.md"
    path.write_text(content, encoding="utf-8")
    return f"Report saved to {path}"


def record_audit_event(action: str, detail: str) -> str:
    # Every consequential action should leave an auditable trace.
    log_path = Path("reports/audit_log.jsonl")
    log_path.parent.mkdir(exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "detail": detail,
    }
    with log_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")
    return "Audit event recorded."

def compare_sources(topic1, topic2, query_engine):
    # queries the knowledge base twice
    response1 = query_engine.query(topic1)
    response2 = query_engine.query(topic2)

    combined_evidence = f"""
    SOURCE MATERIAL FOR {topic1}:
    {response1}

    SOURCE MATERIAL FOR {topic2}:
    {response2}

    Evalution Direction:
    1. OVERLAP: Shared controls or features.
    2. DIFFERENCES: Key differences unique to each topic.
    3. EVIDENCE LIMITATIONS: Any gaps where information is missing.

    """

    return combined_evidence

    

def build_tools(approved_to_save: bool):
    query_engine = load_query_engine()

    knowledge_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        name="knowledge_base_search",
        description=(
            "Search the indexed bootcamp knowledge base. Use it before making factual claims "
            "and return source-grounded findings."
        ),
    )

    save_tool = FunctionTool.from_defaults(
        fn=save_report,
        name="save_report",
        description="Save an approved Markdown report to the local reports directory.",
    )

    audit_tool = FunctionTool.from_defaults(
        fn=record_audit_event,
        name="record_audit_event",
        description="Record a concise audit event for important agent actions.",
    )

    compare_sources_tool = FunctionTool.from_defaults(
        fn=lambda topic_a, topic_b: compare_sources(topic_a, topic_b, query_engine),
        name="compare_sources",
        description="Compare 2 Sources topics, their differences, overlaps, and limitations.",
    )

    tools = [knowledge_tool, audit_tool, compare_sources_tool]
    
    if approved_to_save:
        tools.append(save_tool)

    return tools