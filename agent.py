import anthropic
from dotenv import load_dotenv
from fetch_arxiv import fetch_arxiv
from search_newsapi import search_newsapi
from send_email import send_email                
from datetime import date  

load_dotenv()
client = anthropic.Anthropic()

#Since Claude can’t run the Python functions and only sees a description of them, 
# the tools list will be that description.
#First we will have the name claude will user when asking for this tool, 
# Second, telling Claude what the tool does and when to use it, which claude will reads this to decide which tool to pick and how to write the query,
#and then what input the tools take

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
#the conversation so far. Each round adds Claudes turn and our tool results.
messages = [
    {"role": "user", "content": (
        "Search for today's news in three areas: science, space, and technology. " 
        "Search each area separately using search_newsapi. Use news articles, not research papers. " 
        "From the results, pick the single most important article in each area. " 
        "Return exactly 3 articles: one science, one space, one tech. "
        "For each, give the headline, a 2-sentence summary, and the link. "
        "Format it as plain text for an email: no markdown, no emojis, and put each link on its own line. "
        "If a search returns no results, try at most one different query for that area, then move on. "
        )}
]
#we want to keep talking to Claude until it stops asking for tools
while True:
#send request to claude and wait for  reply
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens = 4000,
        tools=tools,
        messages=messages,
    )
    #save claudes reply into the conversation
    messages.append({"role": "assistant", "content": response.content})
    #if Claude isn't asking for a tool, it's done, so we will then  print the answer and stop
    if response.stop_reason != "tool_use":
        #start with empty text
        briefing = ""
        for block in response.content:
            if block.type == "text":
                briefing += block.text
        #still show it in the terminal for debug purpose
        print(briefing)                 
        #email it, with today date in the subject
        send_email(f"Science Briefing: {date.today()}", briefing)  
        print("Email sent!") 
        break

    #empty list so we can store the rounds tool results
    tool_results = []
    #loop through each block in the reply
    for block in response.content:
        #will only handle tool requests
        if block.type == "tool_use":
            #if claude asks for the newsapi then run that function, otherwise run the fetch function
            if block.name == "search_newsapi":
                result = search_newsapi(query=block.input["query"])
            elif block.name == "fetch_arxiv":
                result = fetch_arxiv(
                    query=block.input["query"],
                    max_results=block.input.get("max_results", 10),
                )
            #show which tool ran and with what input
            print(f"Called {block.name} with {block.input}")
            #put the ansewer and the format expected
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result),
            })
    #send all the ansewers to claude and run again
    messages.append({"role": "user", "content": tool_results})