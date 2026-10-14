#Import to hit the API
import requests
#Import to read the env veriables
import os
#to load .env file
from dotenv import load_dotenv

#call function so .env becomes assessible 
load_dotenv()
#Read API
newsapi_key = os.getenv("NEWSAPI_KEY")

def search_newsapi(query, category="science"):
    #URL string for NewsAPI's top-headlines endpoint
    url = "https://newsapi.org/v2/everything"

    #Python dictionary where each key matches a parameter name NewsAPI expects,
    params = {
    "apiKey": newsapi_key,
    "q": query,
    "language": "en",
    "sortBy": "publishedAt"
    }   
    #match the request
    response = requests.get(url, params=params)
    #check if status worked
    if response.status_code == 200:
        data = response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

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
    print(search_newsapi("black holes"))




