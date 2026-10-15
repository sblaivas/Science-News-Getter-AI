#Import to hit the API
import requests
#Import to read the env veriables
import os
#to load .env file
from dotenv import load_dotenv
from datetime import datetime, timedelta

#call function so .env becomes assessible 
load_dotenv()
#Read API
newsapi_key = os.getenv("NEWSAPI_KEY")

def search_newsapi(query):

    #URL string for NewsAPI' endpoint
    url = "https://newsapi.org/v2/everything"

    # Yesterday's date as YYYY-MM-DD, so we only get recent articles
    #note: widened to two days now
    yesterday = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")

    #Python dictionary where each key matches a parameter name NewsAPI expects,
    params = {
    "apiKey": newsapi_key,
    "q": query,
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 10,
    "searchIn": "title,description",
    "from": yesterday,
    "domains": "sciencealert.com,sciencedaily.com,phys.org,newscientist.com,space.com,nasa.gov,spacenews.com,arstechnica.com,theverge.com,techcrunch.com,wired.com,engadget.com,zdnet.com,technologyreview.com",
    
    }   
    #send the request
    response = requests.get(url, params=params)
    #check if status worked
    if response.status_code == 200:
        data = response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None
    
    #add articles to here
    article_search = []
    #loop thorough articles and return title, description, source, and url 
    for article in data["articles"]:
        title = article["title"]
        description = article["description"]
        url = article["url"]
        source = article["source"]["name"]
        article_search.append({"title": title, "description": description, "url": url, "source": source})
    return article_search

if __name__ == "__main__":
    print(search_newsapi("space"))




