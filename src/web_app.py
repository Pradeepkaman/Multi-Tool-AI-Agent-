"""Web application interface for the Multi-Tool Autonomous AI Agent.

Provides a professional Bootstrap 5 + Google Material Design front-end
strictly utilizing a refined three-color design palette.
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import get_llm
from src.agent import AutonomousAgent
from src.tools import ALL_TOOLS, TOOLS_BY_NAME

app = Flask(
    __name__,
    template_folder=str(PROJECT_ROOT / "templates"),
    static_folder=str(PROJECT_ROOT / "static"),
)


@app.route("/")
def index():
    """Renders the main agent interface."""
    return render_template("index.html")


@app.route("/api/tools", methods=["GET"])
def get_tools():
    """Returns list of registered tools with descriptions."""
    tools_info = [
        {
            "name": tool.name,
            "description": tool.description,
            "category": "web" if "search" in tool.name else ("math" if "calculator" in tool.name else "file"),
            "badge": "DuckDuckGo" if "search" in tool.name else ("Python Math" if "calculator" in tool.name else "Workspace")
        }
        for tool in ALL_TOOLS
    ]
    return jsonify({"success": True, "tools": tools_info})


@app.route("/api/files", methods=["GET"])
def list_data_files():
    """Lists files available in the data directory."""
    data_dir = PROJECT_ROOT / "data"
    files = []
    if data_dir.exists():
        for file in data_dir.glob("*"):
            if file.is_file():
                try:
                    content_preview = file.read_text(encoding="utf-8")[:400]
                except Exception:
                    content_preview = "[Binary or unreadable file]"
                files.append({
                    "name": file.name,
                    "path": f"data/{file.name}",
                    "size_bytes": file.stat().st_size,
                    "preview": content_preview,
                })
    return jsonify({"success": True, "files": files})


@app.route("/api/query", methods=["POST"])
def run_agent_query():
    """Executes a compound query through the autonomous agent."""
    payload = request.get_json() or {}
    query = payload.get("query", "").strip()
    provider = payload.get("provider", "gemini")
    model = payload.get("model")
    mode = payload.get("mode", "live")  # 'live' or 'mock'

    if not query:
        return jsonify({"success": False, "error": "Query cannot be empty."}), 400

    try:
        if mode == "mock" or provider == "mock":
            llm = get_llm(provider="mock")
        else:
            llm = get_llm(provider=provider, model_name=model)

        agent = AutonomousAgent(llm=llm, tools=ALL_TOOLS, verbose=False)
        result = agent.run_with_trace(query)
        return jsonify({"success": True, "data": result})

    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@app.route("/api/tool/execute", methods=["POST"])
def direct_tool_execute():
    """Allows testing an individual tool directly from the UI playground."""
    payload = request.get_json() or {}
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", "")

    if tool_name not in TOOLS_BY_NAME:
        return jsonify({"success": False, "error": f"Tool '{tool_name}' not found."}), 404

    target_tool = TOOLS_BY_NAME[tool_name]
    try:
        if tool_name == "web_search":
            result = target_tool.invoke({"query": str(tool_input)})
        elif tool_name == "calculator":
            result = target_tool.invoke({"expression": str(tool_input)})
        elif tool_name == "read_local_file":
            result = target_tool.invoke({"file_path": str(tool_input)})
        else:
            result = target_tool.invoke(tool_input)

        return jsonify({"success": True, "output": str(result)})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


def run_server(host="127.0.0.1", port=5000, debug=True):
    print("=" * 60)
    print(" 🚀 Multi-Tool Autonomous AI Agent Web Server")
    print(f" 🌐 UI Live at: http://{host}:{port}")
    print("=" * 60)
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_server()
