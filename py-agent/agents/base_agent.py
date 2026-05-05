"""Base agent class providing a LangChain ReAct agent with tool support."""

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent

_SUPPORTED_VENDORS = ("claude", "gemini", "openai")


def _build_llm(
    vendor: str,
    api_key: str,
    model: str,
    max_tokens: int = 8192,
) -> BaseChatModel:
    """Create a chat LLM for the given vendor using the provided API key."""
    vendor = vendor.lower()
    if vendor == "claude":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            api_key=api_key,
            model=model,
            max_tokens=max_tokens,
        )
    if vendor == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model,
            max_output_tokens=max_tokens,
        )
    if vendor == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=api_key,
            model=model,
            max_tokens=max_tokens,
        )
    raise ValueError(
        f"Unsupported AI_VENDOR '{vendor}'. Must be one of: {', '.join(_SUPPORTED_VENDORS)}"
    )


class BaseRavitaAgent:
    """Wraps a LangChain ReAct agent with a system prompt and optional tools."""

    def __init__(
        self,
        vendor: str,
        api_key: str,
        model: str,
        system_prompt: str,
        tools: list[BaseTool] | None = None,
        verbose: bool = False,
        name: str = "Agent",
        max_tokens: int = 8192,
    ) -> None:
        self.name = name
        self.verbose = verbose
        self.system_prompt = system_prompt
        self._tools = tools or []

        llm = _build_llm(
            vendor=vendor,
            api_key=api_key,
            model=model,
            max_tokens=max_tokens,
        )

        self._agent = create_react_agent(
            model=llm,
            tools=self._tools,
            prompt=system_prompt,
        )

    def invoke(self, message: str, history: list[dict[str, Any]] | None = None) -> str:
        """Send *message* to the agent and return its text reply.

        Args:
            message: The user's input message.
            history: Optional list of prior messages for multi-turn context.
        """
        messages: list[Any] = []
        for item in history or []:
            role = item.get("role", "user")
            content = item.get("content", "")
            if role == "user":
                messages.append(HumanMessage(content=content))
            else:
                messages.append(AIMessage(content=content))

        messages.append(HumanMessage(content=message))

        if self.verbose:
            print(f"[{self.__class__.__name__}] invoking with {len(messages)} message(s)")

        result = self._agent.invoke({"messages": messages})
        final_messages = result.get("messages", [])

        for msg in reversed(final_messages):
            if isinstance(msg, AIMessage) and msg.content:
                if isinstance(msg.content, str):
                    return msg.content
                if isinstance(msg.content, list):
                    texts = [b["text"] for b in msg.content if isinstance(b, dict) and b.get("type") == "text"]
                    if texts:
                        return "\n".join(texts)

        return "(no response)"
