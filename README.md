# Building AI Agent Guardrails From Scratch

A small, framework-free Python implementation of **AI agent guardrails**.

This project demonstrates how to put enforceable boundaries between an AI agent and the tools it can execute.

The goal is not to make the agent "trustworthy" through prompting alone.

Instead:

```text
Agent → Guardrail Engine → Decision → Tool
```

The agent can **request an action**, but the guardrail decides whether that action is allowed to execute.

---

## Architecture

```text
                         ┌──────────────────┐
                         │       USER       │
                         └────────┬─────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │    INPUT / REQUEST     │
                     └───────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │         AGENT          │
                     │                        │
                     │    LLM / REASONING     │
                     │          │             │
                     │      Tool Request      │
                     └───────────┬────────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────────┐
              │           GUARDRAIL ENGINE              │
              │                                        │
              │  ┌────────────┐  ┌─────────────────┐  │
              │  │ Tool       │  │ User            │  │
              │  │ Policy     │  │ Permission      │  │
              │  └────────────┘  └─────────────────┘  │
              │                                        │
              │  ┌────────────┐  ┌─────────────────┐  │
              │  │ Argument   │  │ Path / Schema   │  │
              │  │ Validation │  │ Validation      │  │
              │  └────────────┘  └─────────────────┘  │
              │                                        │
              │  ┌────────────┐  ┌─────────────────┐  │
              │  │ Risk       │  │ Runtime         │  │
              │  │ Assessment │  │ Limits          │  │
              │  └────────────┘  └─────────────────┘  │
              └────────────────────┬───────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
                 ┌──────┐      ┌───────┐      ┌─────────┐
                 │ALLOW │      │ BLOCK │      │ APPROVAL│
                 └──┬───┘      └───────┘      └────┬────┘
                    │                                │
                    │                         ┌──────▼──────┐
                    │                         │    HUMAN     │
                    │                         │   APPROVAL   │
                    │                         └──────┬───────┘
                    │                                │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │       TOOL       │
                            │                  │
                            │ Files / DB / API │
                            │ Email / Browser  │
                            └────────┬─────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │  OUTPUT GUARD    │
                            │                  │
                            │ Secret Redaction │
                            │ Output Checks    │
                            └────────┬─────────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │  OBSERVATION │
                              └──────┬───────┘
                                     │
                                     └──────► AGENT
```

---

## What Are Agent Guardrails?

An AI agent can do more than generate text.

An agent can potentially:

* Read files
* Write files
* Delete files
* Query databases
* Call APIs
* Send emails
* Execute code
* Modify external systems

That creates an important architectural question:

> **If the agent decides to perform an action, who decides whether that action is actually allowed?**

That's the role of a guardrail.

Instead of:

```text
LLM → Tool
```

we use:

```text
LLM → Tool Request → Guardrail → Tool
```

The LLM proposes an action.

The guardrail evaluates it.

Only then can the tool execute.

---

## Project Structure

```text
agent-guardrails/
│
├── main.py
│
├── agent.py
├── guardrails.py
├── policies.py
├── tools.py
├── models.py
├── permissions.py
├── validators.py
├── risk.py
├── approval.py
├── output_guard.py
├── audit.py
│
└── requirements.txt
```

### `main.py`

Application entry point.

It creates:

* User
* Guardrail engine
* Agent

It also contains example tool calls demonstrating:

* Allowed actions
* Blocked actions
* Human approval
* Explicitly blocked tools

---

### `agent.py`

Contains the agent runtime.

The important architectural rule is:

```text
Agent
  ↓
ToolCall
  ↓
GuardrailEngine
```

The agent does **not** directly execute the tool.

---

### `guardrails.py`

The central guardrail engine.

It performs checks such as:

1. Does the tool exist?
2. Does the tool have a policy?
3. Is the tool explicitly blocked?
4. Does the user have permission?
5. Are the arguments valid?
6. Is the path safe?
7. What is the risk level?
8. Does the action require human approval?
9. Is the runtime within limits?
10. Should the tool execute?

---

### `policies.py`

Defines policies for individual tools.

Example:

```python
TOOL_POLICY = {
    "read_file": {
        "risk": "LOW",
        "approval": False,
    },

    "write_file": {
        "risk": "MEDIUM",
        "approval": False,
    },

    "delete_file": {
        "risk": "HIGH",
        "approval": True,
    },

    "get_secret": {
        "risk": "CRITICAL",
        "blocked": True,
    },
}
```

This separates **what a tool does** from **what the agent is allowed to do with that tool**.

---

### `tools.py`

Contains the actual capabilities available to the agent.

The demo includes:

```text
read_file
write_file
delete_file
get_secret
```

In a real system, these could represent:

```text
Database
REST API
GitHub
Email
Filesystem
Browser
Cloud infrastructure
```

---

### `models.py`

Contains the shared data structures:

```python
ToolCall
GuardrailResult
Decision
User
```

For example:

```python
ToolCall(
    name="delete_file",
    arguments={
        "path": "/safe/old_report.txt"
    }
)
```

---

### `permissions.py`

Handles user-level authorization.

A tool can be available to the agent but still unavailable to a particular user.

```text
Tool exists
    ↓
Does this user have permission?
    ↓
YES / NO
```

---

### `validators.py`

Validates tool arguments.

For example, a file operation can enforce:

```text
Allowed:
/safe/report.txt

Blocked:
/etc/passwd

Blocked:
/safe/../../secret.txt
```

This demonstrates why **tool authorization alone isn't enough**.

You might allow `delete_file`, while still restricting which files can actually be deleted.

---

### `risk.py`

Assigns a risk level to an action.

Example:

```text
read_file       → LOW
write_file      → MEDIUM
delete_file     → HIGH
get_secret      → CRITICAL
```

Risk can later become much more sophisticated by considering:

```text
Tool
+
Arguments
+
User
+
Target resource
+
Context
+
Previous actions
```

---

### `approval.py`

Implements human-in-the-loop approval.

For example:

```text
Agent:
Delete /safe/old_report.txt

Guardrail:
HIGH RISK

Human:
Approve? yes/no
```

Only after approval does execution continue.

---

### `output_guard.py`

Guards the result after the tool executes.

For example, if a tool accidentally returns:

```text
api_key=sk-super-secret-key-123
```

the output guard can transform it into:

```text
api_key=[REDACTED]
```

This demonstrates an important point:

> Guardrails aren't only about controlling what goes **into** a tool. They can also control what comes **out**.

---

### `audit.py`

Records important agent and guardrail events.

Example:

```text
TOOL_REQUEST
RISK_ASSESSMENT
GUARDRAIL_DECISION
HUMAN_APPROVED
TOOL_EXECUTED
OUTPUT_VALIDATED
```

Audit logs make the system observable and easier to debug.

---

# Guardrail Decision Flow

Every tool request follows this basic flow:

```text
                 Tool Request
                      │
                      ▼
                Tool exists?
                 │       │
                NO      YES
                 │       │
               BLOCK     ▼
                    Policy exists?
                         │
                         ▼
                  User authorized?
                         │
                         ▼
                  Arguments valid?
                         │
                         ▼
                    Path valid?
                         │
                         ▼
                     Risk check
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
            ALLOW      BLOCK     APPROVAL
              │                     │
              │                  HUMAN
              │                  DECISION
              │                     │
              └──────────┬──────────┘
                         ▼
                       TOOL
                         │
                         ▼
                  OUTPUT GUARD
                         │
                         ▼
                    SAFE RESULT
```

---

# Example 1 — Allowed Action

The agent requests:

```python
ToolCall(
    name="read_file",
    arguments={
        "path": "/safe/report.txt"
    }
)
```

The guardrail checks:

```text
Tool exists       ✓
Policy exists     ✓
Permission        ✓
Arguments         ✓
Path              ✓
Risk = LOW        ✓

                ↓

               ALLOW
```

The tool executes.

---

# Example 2 — Blocked Action

The agent requests:

```python
ToolCall(
    name="delete_file",
    arguments={
        "path": "/etc/passwd"
    }
)
```

The tool exists.

The user has permission to use `delete_file`.

But:

```text
Path validation
       ↓
/etc/passwd
       ↓
Outside /safe
       ↓
BLOCK
```

The tool is never executed.

---

# Example 3 — Human Approval

The agent requests:

```python
ToolCall(
    name="delete_file",
    arguments={
        "path": "/safe/old_report.txt"
    }
)
```

The request passes validation.

However:

```text
delete_file
     ↓
HIGH RISK
     ↓
APPROVAL REQUIRED
     ↓
HUMAN
```

The user can approve or reject the action.

---

# Example 4 — Explicitly Blocked Tool

The agent requests:

```python
ToolCall(
    name="get_secret",
    arguments={}
)
```

The policy explicitly blocks this capability:

```python
"get_secret": {
    "risk": "CRITICAL",
    "blocked": True,
}
```

Therefore:

```text
Agent
  ↓
get_secret
  ↓
Policy
  ↓
BLOCK
```

The underlying tool is never executed.

---

# Why Not Just Use a System Prompt?

You could tell the model:

```text
Never delete files.
Never expose secrets.
Always ask for permission.
```

But that is not the same as an execution boundary.

A stronger architecture is:

```text
              LLM
               │
               │ "I want to delete this file"
               ▼
        ┌───────────────┐
        │   GUARDRAIL   │
        │               │
        │ Policy        │
        │ Permission    │
        │ Validation    │
        │ Risk          │
        └───────┬───────┘
                │
          ALLOW / BLOCK
                │
                ▼
              TOOL
```

The model proposes.

The guardrail enforces.

The tool executes.

---

# Running the Project

No external dependencies are required.

```bash
python main.py
```

You should see the agent execute an allowed read operation, block an unsafe delete operation, request human approval for a high-risk delete, and block the explicitly forbidden secret-reading tool.

---

# Key Design Principle

The most important idea in this project is:

```text
REASONING ≠ AUTHORIZATION
```

The LLM can determine:

> "I should delete this file."

But it should not automatically have the authority to do it.

The architecture becomes:

```text
             LLM
              │
          WHAT SHOULD
          I DO NEXT?
              │
              ▼
        ┌─────────────┐
        │ GUARDRAILS  │
        │             │
        │ CAN I?      │
        │ SHOULD I?   │
        │ IS IT SAFE? │
        └──────┬──────┘
               │
               ▼
             TOOL
```

This separation between **reasoning** and **execution authority** is the foundation of a guardrailed agent architecture.

---

## Possible Extensions

This project intentionally starts small.

It can be extended with:

* LLM-powered input safety checks
* Prompt-injection detection
* JSON Schema validation
* RBAC
* OAuth scopes
* Database permissions
* Network restrictions
* Rate limiting
* Token budgets
* Maximum agent steps
* Tool-specific sandboxes
* Secret scanning
* PII detection
* Content policy checks
* Persistent audit logs
* Policy configuration files
* Human approval UI
* Multi-agent permissions
* Docker sandboxing
* MCP tool authorization

The goal is to understand the **architecture first**, then introduce more sophisticated guardrail mechanisms.

---

## Mental Model

Think of the agent as an employee.

```text
Agent
  ↓
"I want to perform this action."

Guardrail
  ↓
"Are you allowed?"

Policy
  ↓
"Is this action permitted?"

Risk Engine
  ↓
"How dangerous is it?"

Human
  ↓
"Do I approve this?"

Tool
  ↓
"Execute."
```

The agent gets autonomy **inside boundaries**, rather than unrestricted control over the tools.
