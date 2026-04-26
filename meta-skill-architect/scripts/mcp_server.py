#!/usr/bin/env python3
"""
mcp_server.py - Model Context Protocol Server for prompt_v22

Exposes the prompt_v22 skill to other agents following the MCP stdio protocol.
This is the standard pattern for agents running as subprocesses.

Usage:
    python scripts/mcp_server.py

The server communicates via stdio using JSON-RPC 2.0 format.
"""

import json
import sys
import datetime
import os
from pathlib import Path


def get_skill_metadata() -> dict:
    """Return skill metadata."""
    return {
        "name": "prompt_v22",
        "version": "2.2.0",
        "description": "Meta-Skill Architect for safe operational contract generation",
        "author": "prompt_v22",
        "runtimes": ["Claude", "Gemini", "GPT", "Opencode", "Kilocode"],
    }


def execute_skill(user_input: str, context: dict = None) -> dict:
    """
    Execute the prompt_v22 skill with user input.

    In a full implementation, this would:
    1. Load system.md and task.md
    2. Combine with user_input
    3. Send to the underlying LLM
    4. Return the generated artifact
    """
    # For now, return a simulated response
    return {
        "status": "success",
        "timestamp": datetime.datetime.now().isoformat(),
        "artifact": f"""## PASO 1 — Intención
Procesando petición del usuario: {user_input[:30]}...

[Resultado simulado - completar con implementación real]
""",
    }


def handle_request(request_str: str) -> str:
    """Process incoming RPC request following MCP format."""
    try:
        request = json.loads(request_str)
        method = request.get("method")
        request_id = request.get("id", 1)

        if method == "get_skill_metadata":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": get_skill_metadata(),
            }
            return json.dumps(response)

        elif method == "execute":
            params = request.get("params", {})
            user_input = params.get("input", "")
            context = params.get("context", {})

            result = execute_skill(user_input, context)

            response = {"jsonrpc": "2.0", "id": request_id, "result": result}
            return json.dumps(response)

        elif method == "list_methods":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "methods": ["get_skill_metadata", "execute", "list_methods"]
                },
            }
            return json.dumps(response)

        else:
            error_response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not supported: {method}"},
            }
            return json.dumps(error_response)

    except json.JSONDecodeError:
        error_response = {
            "jsonrpc": "2.0",
            "id": 1,
            "error": {
                "code": -32700,
                "message": "Invalid JSON. Expected MCP JSON-RPC format.",
            },
        }
        return json.dumps(error_response)

    except Exception as e:
        error_response = {
            "jsonrpc": "2.0",
            "id": 1,
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
        }
        return json.dumps(error_response)


def main():
    """Main server loop - reads from stdin, writes to stdout."""
    base_dir = Path(__file__).parent.parent
    system_md = base_dir / "system.md"
    task_md = base_dir / "task.md"

    # Check for required files
    if not system_md.exists() or not task_md.exists():
        print(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 0,
                    "error": {
                        "code": -32000,
                        "message": "Skill files not found. Ensure system.md and task.md exist.",
                    },
                }
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    # Send ready event
    print(
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 0,
                "result": {
                    "event": "ready",
                    "server": "prompt_v22_mcp",
                    "version": "2.2.0",
                },
            }
        ),
        flush=True,
    )

    # Main event loop
    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        if line.lower() == "exit" or line.lower() == "quit":
            print(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": 0,
                        "result": {"message": "Server shutting down"},
                    }
                ),
                flush=True,
            )
            break

        # Handle RPC request
        response = handle_request(line)
        print(response, flush=True)


if __name__ == "__main__":
    main()
