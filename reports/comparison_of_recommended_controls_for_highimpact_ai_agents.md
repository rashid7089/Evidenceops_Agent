# Comparison of Recommended Controls for High-Impact AI Agents

## Overview

This report compares the recommended safety and security controls for high-impact AI agents, based on evidence retrieved from the indexed knowledge base. Three distinct categories of controls were identified.

---

## 1. Human Approval Gates (Governance Control)

**Recommendation:** High-impact agents require explicit human approval gates before executing persistent actions.

- **Scope:** Applies to any operation that has lasting effects (e.g., writing files, sending emails, modifying databases, executing system commands).
- **Mechanism:** The agent must pause and request human authorization before proceeding with the action.
- **Rationale:** Prevents unintended or harmful persistent changes by ensuring a human remains in the loop for consequential decisions.

---

## 2. Tool Safety Controls (Technical Control)

**Recommendation:** Agents must enforce strict type validation and restrict access to approved directories to prevent path traversal vulnerabilities.

- **Scope:** Applies to all tool invocations, especially file system operations.
- **Mechanism:**
  - **Strict type validation:** Ensure inputs match expected types (e.g., string, integer) before processing.
  - **Restricted directories:** Limit file read/write operations to a predefined set of approved directories.
- **Rationale:** Prevents path traversal attacks where an agent could be tricked into accessing or modifying files outside its intended scope.

---

## 3. Data Trust Controls (Adversarial Defense)

**Recommendation:** Retrieved content must be treated as untrusted data rather than direct operational instructions.

- **Scope:** Applies to any content fetched from external sources (e.g., web pages, APIs, databases, user-provided documents).
- **Mechanism:** Do not execute or directly act upon retrieved content without validation, sanitization, or human review.
- **Rationale:** Mitigates prompt injection, indirect prompt injection, and other adversarial attacks where external content could manipulate agent behavior.

---

## Comparison Matrix

| Control Category | Type | Primary Threat | Human Involvement | Implementation Complexity |
|---|---|---|---|---|
| Human Approval Gates | Governance / Procedural | Unauthorized persistent actions | Required (explicit) | Low (process change) |
| Tool Safety Controls | Technical | Path traversal, input injection | Not required | Medium (code changes) |
| Data Trust Controls | Adversarial Defense | Prompt injection, data poisoning | Optional (recommended for high-risk) | Medium (architecture changes) |

---

## Overlaps

All three controls share the common goal of **preventing unauthorized or harmful agent actions**. They are complementary rather than mutually exclusive:

- Human approval gates and data trust controls both involve human judgment (explicitly or implicitly).
- Tool safety controls and data trust controls both rely on input validation principles (validating types vs. validating content trustworthiness).

## Differences

| Dimension | Human Approval Gates | Tool Safety Controls | Data Trust Controls |
|---|---|---|---|
| **When applied** | Before execution of persistent actions | At tool invocation time | After content retrieval, before use |
| **What it protects** | Decision authority | File system integrity | Agent behavior integrity |
| **Automation level** | Manual (human-in-the-loop) | Automated (code-enforced) | Automated + optional human review |
| **Failure mode if absent** | Agent acts without oversight | Agent accesses restricted files | Agent follows adversarial instructions |

---

## Evidence Limitations

1. **Scope of "persistent actions"** is not exhaustively defined in the source material — examples are implied but not enumerated.
2. **No quantitative data** (e.g., effectiveness rates, incident reduction metrics) is available for any of the controls.
3. **No specific frameworks or standards** (e.g., NIST, OWASP, ISO) are referenced in the source material.
4. **Implementation guidance** (e.g., code examples, architecture diagrams) is not provided.
5. **No information on edge cases** or failure modes of the controls themselves (e.g., what happens if human approval is unavailable).

---

## Confidence Assessment

**Confidence: Moderate**

The three control categories are consistently mentioned across multiple knowledge base entries, suggesting they are established recommendations. However, the source material is limited in depth and does not reference authoritative external standards or empirical validation.

---

## Recommended Next Actions

1. **Cross-reference** these controls against established frameworks (e.g., OWASP AI Security, NIST AI RMF, EU AI Act requirements).
2. **Develop implementation playbooks** for each control category with code examples and testing procedures.
3. **Conduct a threat modeling exercise** to identify gaps not covered by these three controls.
4. **Define "persistent actions"** explicitly for the specific deployment context.
5. **Establish testing and validation procedures** to verify each control is working as intended.

---

*Report generated by EvidenceOps based on knowledge base search results.*
