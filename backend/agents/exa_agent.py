import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.tools.exa import ExaTools

load_dotenv()
EXA_API_KEY = os.getenv("EXA_API_KEY")
# agents/exa_agent.py
import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.tools.exa import ExaTools

load_dotenv()
EXA_API_KEY = os.getenv("EXA_API_KEY")

ExaAgent = Agent(
    name="Exa Search Agent",
    tools=[
        ExaTools(
            api_key=EXA_API_KEY,
            # Keep the surface area small to avoid extra round-trips
            enable_search=True,
            enable_get_contents=True,   # keep, but we’ll gate its usage below
            enable_answer=False,        # disable to avoid an extra API call layer
            enable_find_similar=False,  # disable; it often triggers extra calls

            # Keep the result set tight
            num_results=3,

            # Reduce token bloat
            text_length_limit=800,      # was 2000
            include_domains=None,
            exclude_domains=None,

            # Don't dump raw results into the model by default
            show_results=False,
        )
    ],
    instructions=[
        "You are a web search specialist using Exa.",
        "STRICT RULES TO REDUCE LATENCY:",
        "• Call search() at most once per user request.",
        "• Only call get_contents() for the top 1–2 URLs if the query needs verification or quotations.",
        "• Never call get_contents() for all results.",
        "• Summarize succinctly; cite the URLs instead of pasting content.",
    ],
    markdown=True,
    # Keep history out of the prompt to avoid huge contexts on Exa flows
    add_history_to_context=False,
)
