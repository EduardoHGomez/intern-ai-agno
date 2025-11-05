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
            # Enable both search and get_contents
            enable_search=True,
            enable_get_contents=True,
            enable_answer=True,
            enable_find_similar=True,
            enable_research=False,
            
            # Search configuration
            num_results=5,
            
            # Contents configuration
            text_length_limit=2000,
            include_domains=None,  # Optional: ["arxiv.org", "github.com"]
            exclude_domains=None,
            
            # Show results in agent response
            show_results=True,
        )
    ],
    instructions=[
        "You are a web search and content retrieval specialist using Exa.",
        "When users ask you to search or find information:",
        "1. Use search() to find relevant URLs and get summaries",
        "2. Use get_contents() when you need full page content from specific URLs",
        "3. Always provide clear source attribution with URLs",
        "4. Summarize findings in a structured, easy-to-read format",
        "5. For research queries, combine search results with content retrieval",
        "When searching:",
        "- Use 'auto' search type for best results (default)",
        "- Use 'neural' for semantic/conceptual searches",
        "- Use 'keyword' for exact term matching",
        "Format your responses with:",
        "- Clear headings for different sources",
        "- Bullet points for key findings",
        "- Direct quotes when relevant (with attribution)",
        "- Links to original sources",
    ],
    markdown=True,
)