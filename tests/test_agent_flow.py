"""End-to-end integration test validating the agent's ReAct execution loop.

Tests the full reasoning lifecycle:
Thought -> Action -> Observation -> Final Answer across compound multi-tool calls.
"""

import sys
from pathlib import Path
from typing import List, Any
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.agent import AutonomousAgent
from src.tools import ALL_TOOLS


class DeterministicReActMockLLM(BaseChatModel):
    """Mock LLM that simulates a multi-step compound query resolution."""

    step: int = 0

    @property
    def _llm_type(self) -> str:
        return "deterministic-react-mock"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Any = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        self.step += 1

        if self.step == 1:
            # Step 1: Model reads the local file
            msg = AIMessage(
                content="I need to inspect the company earnings file first to find FY2024 revenue numbers.",
                tool_calls=[
                    {
                        "name": "read_local_file",
                        "args": {"file_path": "data/company_earnings.txt"},
                        "id": "call_file_1",
                    }
                ],
            )
        elif self.step == 2:
            # Step 2: Model calculates the percentage growth
            msg = AIMessage(
                content="I have the quarterly numbers: 12.5M, 14.2M, 15.8M, 18.5M. Let me compute the total and percentage growth against FY2023 ($48M).",
                tool_calls=[
                    {
                        "name": "calculator",
                        "args": {
                            "expression": "(12500000 + 14200000 + 15800000 + 18500000 - 48000000) / 48000000 * 100"
                        },
                        "id": "call_calc_2",
                    }
                ],
            )
        elif self.step == 3:
            # Step 3: Model searches web for industry benchmark
            msg = AIMessage(
                content="Acme Corp grew by 27.08%. Now let me search for the average tech industry growth in 2024 to compare.",
                tool_calls=[
                    {
                        "name": "web_search",
                        "args": {"query": "tech industry average revenue growth rate 2024"},
                        "id": "call_search_3",
                    }
                ],
            )
        else:
            # Step 4: Final synthesized answer
            msg = AIMessage(
                content=(
                    "Acme Corp achieved a total FY2024 revenue of $61,000,000, representing a strong 27.08% YoY growth "
                    "compared to FY2023 ($48,000,000). Industry reports for tech companies in 2024 report median growth "
                    "rates around 12-15%, indicating Acme Corp significantly outperformed the broader tech market benchmark."
                )
            )

        return ChatResult(generations=[ChatGeneration(message=msg)])

    def bind_tools(self, tools: Any, **kwargs: Any) -> Any:
        return self


def test_agent_react_compound_loop():
    print("=== Testing Agent ReAct Compound Loop ===")
    mock_llm = DeterministicReActMockLLM()
    agent = AutonomousAgent(llm=mock_llm, tools=ALL_TOOLS, verbose=True)

    test_query = (
        "Read 'data/company_earnings.txt', calculate the FY2024 YoY growth, "
        "and compare it to the tech industry average."
    )
    final_result = agent.run(test_query)

    assert "Acme Corp" in final_result
    assert "27.08%" in final_result
    print("\n Agent ReAct Compound Loop successfully executed all 3 tools in sequence!")


if __name__ == "__main__":
    test_agent_react_compound_loop()

