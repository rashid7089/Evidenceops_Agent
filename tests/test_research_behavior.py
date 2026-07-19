from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

from app.orchestrator import run_research
from app.services.index_service import load_query_engine
from app.tools.research_tools import compare_sources, record_audit_event, save_report


# ---------- Tool safety tests ----------


def test_save_report_sanitizes_filename(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    save_report("Report With / Weird * Chars!", "# Content")
    expected = tmp_path / "reports" / "report_with__weird__chars.md"
    assert expected.exists()


def test_save_report_stays_inside_reports_directory(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    save_report("../../../etc/passwd", "# Content")
    reports_dir = tmp_path / "reports"
    assert reports_dir.exists()
    saved_files = list(reports_dir.glob("*.md"))
    assert len(saved_files) == 1
    assert saved_files[0].resolve().is_relative_to(reports_dir.resolve())


def test_record_audit_event_writes_valid_json(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    record_audit_event("test_action", "test detail")
    log_path = tmp_path / "reports" / "audit_log.jsonl"
    lines = log_path.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 1
    event = json.loads(lines[0])
    assert event["action"] == "test_action"
    assert event["detail"] == "test detail"
    assert "timestamp" in event


# ---------- Retrieval and agent behavior tests ----------


def test_load_query_engine_returns_engine() -> None:
    engine = load_query_engine()
    assert engine is not None
    assert hasattr(engine, "query")


def test_agent_uses_knowledge_base_search() -> None:
    result = asyncio.run(run_research("Why should high-impact actions require approval?"))
    assert "knowledge_base_search" in result.tools_used


def test_agent_does_not_save_without_approval() -> None:
    result = asyncio.run(run_research("Why should high-impact actions require approval?"))
    assert "save_report" not in result.tools_used
    assert result.approved_to_save is False


def test_compare_sources_returns_text() -> None:
    engine = load_query_engine()
    text = compare_sources("high-impact agents", "low-impact agents", engine)
    assert isinstance(text, str)
    assert "OVERLAP" in text
    assert "DIFFERENCES" in text
