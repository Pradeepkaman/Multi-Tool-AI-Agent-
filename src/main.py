"""Interactive Console Interface for the Multi-Tool Autonomous AI Agent."""

import argparse
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import get_llm
from src.agent import AutonomousAgent
from src.tools import ALL_TOOLS

console = Console()

BANNER = """
[bold cyan]╔════════════════════════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║[/bold cyan]           [bold white]Multi-Tool Autonomous AI Agent (Task 3)[/bold white]              [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]   [dim]Equipped with Web Search, Math Calculator & File Reader[/dim]      [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]       [dim]Reasoning Chain: Thought → Action → Observation → Answer[/dim]  [bold cyan]║[/bold cyan]
[bold cyan]╚════════════════════════════════════════════════════════════════╝[/bold cyan]
"""


def show_tools_table():
    """Displays available agent tools."""
    table = Table(title="🛠️ Registered Agent Tools", border_style="cyan")
    table.add_column("Tool Name", style="bold green", width=18)
    table.add_column("Capability", style="white")
    table.add_column("Provider / Library", style="dim", width=22)

    table.add_row(
        "web_search",
        "Searches the public web for real-time information, facts, and live data.",
        "DuckDuckGo (Free / No Key)",
    )
    table.add_row(
        "calculator",
        "Safely evaluates arithmetic expressions, percentages, and math formulas.",
        "Python Math Engine",
    )
    table.add_row(
        "read_local_file",
        "Reads workspace files (notes, text, reports, markdown, JSON, CSV).",
        "Local File System",
    )

    console.print(table)


def run_benchmark(agent: AutonomousAgent):
    """Runs a multi-tool compound query that demonstrates all three tools in action."""
    compound_query = (
        "Read the file 'data/company_earnings.txt' to find Acme Corp's total revenue for FY2024 "
        "(by summing all 4 quarters). Then calculate the year-over-year revenue growth percentage "
        "compared to FY2023 revenue of $48,000,000 using the calculator. Finally, search DuckDuckGo "
        "for the typical annual revenue growth rate for tech companies in 2024 and compare the two."
    )

    console.print(
        Panel(
            f"[bold yellow]Compound Benchmark Query:[/bold yellow]\n{compound_query}",
            title="🧪 Multi-Step Compound Test",
            border_style="yellow",
        )
    )
    agent.run(compound_query)


def interactive_loop(agent: AutonomousAgent):
    """Starts the interactive console REPL."""
    console.print(BANNER)
    console.print("[dim]Type your research question, or type [bold cyan]help[/bold cyan], [bold cyan]tools[/bold cyan], [bold cyan]benchmark[/bold cyan], or [bold cyan]exit[/bold cyan].[/dim]\n")

    while True:
        try:
            user_input = Prompt.ask("[bold green]Agent Query[/bold green]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Exiting agent. Goodbye![/yellow]")
            break

        cleaned = user_input.strip()
        if not cleaned:
            continue

        lower_cmd = cleaned.lower()
        if lower_cmd in ("exit", "quit", "q"):
            console.print("[yellow]Exiting agent. Goodbye![/yellow]")
            break
        elif lower_cmd == "help":
            console.print("\n[bold]Available Commands:[/bold]")
            console.print("  [cyan]tools[/cyan]      - Show list of registered tools")
            console.print("  [cyan]benchmark[/cyan]  - Run the multi-tool compound research benchmark")
            console.print("  [cyan]clear[/cyan]      - Clear terminal screen")
            console.print("  [cyan]exit[/cyan]       - Quit the console agent\n")
            continue
        elif lower_cmd == "tools":
            show_tools_table()
            continue
        elif lower_cmd == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            console.print(BANNER)
            continue
        elif lower_cmd == "benchmark":
            run_benchmark(agent)
            continue

        # Execute query through agent
        try:
            agent.run(cleaned)
        except Exception as exc:
            console.print(
                Panel(
                    f"[bold red]Execution Error:[/bold red] {str(exc)}\n\n"
                    "Tip: Verify that your API key is valid in the `.env` file.",
                    title="⚠️ Error",
                    border_style="red",
                )
            )


def main():
    parser = argparse.ArgumentParser(description="Multi-Tool Autonomous AI Agent Console")
    parser.add_argument("--query", "-q", type=str, help="Run a single query and exit")
    parser.add_argument("--benchmark", "-b", action="store_true", help="Run the compound test benchmark and exit")
    parser.add_argument("--mock", action="store_true", help="Run in mock/offline mode (no API key required)")
    parser.add_argument("--provider", "-p", type=str, help="LLM Provider (gemini, openai, groq, mock)")
    parser.add_argument("--model", "-m", type=str, help="Model name (e.g. gemini-2.5-flash, gpt-4o-mini)")
    parser.add_argument("--quiet", action="store_true", help="Hide reasoning chain and show only final answer")
    parser.add_argument("--max-steps", type=int, default=10, help="Maximum reasoning steps (default: 10)")
    args = parser.parse_args()

    # Initialize LLM
    try:
        provider = "mock" if args.mock else args.provider
        llm = get_llm(provider=provider, model_name=args.model)
    except Exception as exc:
        console.print(
            Panel(
                f"[bold red]Configuration Error:[/bold red] {str(exc)}\n\n"
                "Please make sure your API key is configured in [bold cyan].env[/bold cyan]:\n"
                "  1. Copy [bold].env.example[/bold] to [bold].env[/bold]\n"
                "  2. Add your valid [bold green]GEMINI_API_KEY[/bold green] or [bold green]OPENAI_API_KEY[/bold green]",
                title="⚠️ Setup Required",
                border_style="red",
            )
        )
        sys.exit(1)

    agent = AutonomousAgent(
        llm=llm,
        tools=ALL_TOOLS,
        max_iterations=args.max_steps,
        verbose=not args.quiet,
    )

    if args.benchmark:
        run_benchmark(agent)
    elif args.query:
        agent.run(args.query)
    else:
        interactive_loop(agent)


if __name__ == "__main__":
    main()
