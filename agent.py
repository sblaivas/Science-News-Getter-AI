import anthropic
import os
from dotenv import load_dotenv
from fetch_arxiv import fetch_arxiv
from search_newsapi import search_newsapi

load_dotenv()
client = anthropic.Anthropic()

tools = [
    {
        "name": "search_newsapi",
        "description": "Searches NewsAPI for recent news articles on science, space, and technology. Wrap multi-word phrases in double quotes; use OR to combine topics.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search topic, e.g. 'black holes' or 'climate change'"
                }
            
            },
            "required": ["query"]
        }
    },
    {
    "name": "fetch_arxiv",
    "description": "Searches arXiv for research paper abstracts in space, physics, mathematics, computer science, quantitative biology, statistics, and economics. Use this for deeper, research-level topics rather than general news.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search topic, e.g. 'black holes' or 'quantum computing'"
            },
            "max_results": {
                "type": "integer",
                "description": "How many papers to return, defaults to 10"
            }
        },
        "required": ["query"]
                    }
    }
]
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens = 4000,
    tools=tools,
    messages=[
        {"role": "user", "content": "Search for today's news in three areas: science, space, and technology. Search each area separately using search_newsapi. Use news articles, not research papers. From the results, pick the single most important article in each area. Return exactly 3 articles: one science, one space, one tech. For each, give the headline, a 2-sentence summary, and the link."}
    ]
)

for block in response.content:
    if block.type == "tool_use":
        if block.name == "search_newsapi":
                    result = search_newsapi(
                        query=block.input["query"],
                    
                    )
                    print("Called search_newsapi, got:", result)

        elif block.name == "fetch_arxiv":
            result = fetch_arxiv(
            query=block.input["query"],
            max_results=block.input.get("max_results", 10)
                                )
            print("Called fetch_arxiv, got:", result)

    elif block.type == "text":
        print(block.text)